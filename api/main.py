from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator
from stable_baselines3 import DQN

from pricing_env import PricingEnv

MODEL_PATH = Path(os.getenv("MODEL_PATH", "models/pricing_dqn.zip"))
app = FastAPI(
    title="RL Dynamic Pricing Optimizer",
    version="1.0.0",
    description="DQN pricing recommendations in a synthetic retail simulator.",
)
_model = None


class PricingRequest(BaseModel):
    unit_cost: float = Field(gt=0, le=10000, description="Unit cost in currency units")
    current_price: float = Field(gt=0, le=10000)
    competitor_price: float = Field(gt=0, le=10000)
    demand_index: float = Field(ge=0.2, le=2.0, default=1.0)
    inventory: int = Field(ge=0, le=1_000_000, default=100)
    max_price_change_pct: float = Field(gt=0, le=30, default=20)

    @model_validator(mode="after")
    def price_above_cost(self):
        if self.current_price < self.unit_cost:
            raise ValueError("current_price should be greater than or equal to unit_cost")
        return self


class PricingResponse(BaseModel):
    recommended_price: float
    action_multiplier: float
    estimated_demand: int
    estimated_units_sold: int
    estimated_revenue: float
    estimated_profit: float
    model: str
    disclaimer: str


@app.on_event("startup")
def load_model():
    global _model
    if MODEL_PATH.exists():
        _model = DQN.load(str(MODEL_PATH), device="cpu")


@app.get("/")
def root():
    return {
        "name": "RL Dynamic Pricing Optimizer",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    ready = _model is not None
    return {"status": "ok" if ready else "model_not_ready", "model_loaded": ready}


@app.post("/recommend", response_model=PricingResponse)
def recommend(request: PricingRequest):
    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Trained model is not available. Run `python train.py` and ensure models/pricing_dqn.zip exists.",
        )

    reference_price = 50.0
    obs = np.array([
        np.clip(request.demand_index, 0.2, 2.0),
        np.clip(request.inventory / 250.0, 0.0, 1.0),
        np.clip(request.competitor_price / reference_price, 0.4, 1.6),
        np.clip(request.current_price / reference_price, 0.4, 1.6),
        np.clip(request.unit_cost / reference_price, 0.05, 0.8),
    ], dtype=np.float32)

    action, _ = _model.predict(obs, deterministic=True)
    multiplier = float(PricingEnv.ACTION_MULTIPLIERS[int(action)])
    raw_price = reference_price * multiplier
    max_change = request.max_price_change_pct / 100.0
    lower = request.current_price * (1 - max_change)
    upper = request.current_price * (1 + max_change)
    recommended = float(np.clip(raw_price, max(lower, request.unit_cost), upper))
    relative_price = recommended / request.competitor_price
    expected = 28.0 * request.demand_index * np.exp(-2.0 * (relative_price - 1.0))
    estimated_demand = max(0, int(round(expected)))
    units = min(estimated_demand, request.inventory)
    revenue = units * recommended
    profit = units * (recommended - request.unit_cost)

    return PricingResponse(
        recommended_price=round(recommended, 2),
        action_multiplier=round(multiplier, 2),
        estimated_demand=estimated_demand,
        estimated_units_sold=units,
        estimated_revenue=round(revenue, 2),
        estimated_profit=round(profit, 2),
        model="DQN (Stable-Baselines3)",
        disclaimer="Estimates come from a synthetic demand model; validate offline before any real-world use.",
    )
