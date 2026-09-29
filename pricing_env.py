from __future__ import annotations

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class PricingEnv(gym.Env):
    """A synthetic, episodic retail pricing environment.

    Observation (normalized): demand index, inventory ratio, competitor price
    relative to reference price, current price relative to reference price,
    and unit cost relative to reference price.
    Actions select a price multiplier from a bounded discrete set.
    """

    metadata = {"render_modes": []}
    ACTION_MULTIPLIERS = np.array([0.80, 0.90, 1.00, 1.10, 1.20], dtype=np.float32)

    def __init__(self, horizon: int = 30, seed: int | None = None):
        super().__init__()
        self.horizon = int(horizon)
        self.reference_price = 50.0
        self.max_inventory = 250
        self.action_space = spaces.Discrete(len(self.ACTION_MULTIPLIERS))
        self.observation_space = spaces.Box(
            low=np.array([0.2, 0.0, 0.4, 0.4, 0.05], dtype=np.float32),
            high=np.array([2.0, 1.0, 1.6, 1.6, 0.8], dtype=np.float32),
            dtype=np.float32,
        )
        self.np_random = None
        self._seed = seed
        self.reset(seed=seed)

    def _observation(self) -> np.ndarray:
        return np.array([
            np.clip(self.demand_index, 0.2, 2.0),
            self.inventory / self.max_inventory,
            np.clip(self.competitor_price / self.reference_price, 0.4, 1.6),
            np.clip(self.current_price / self.reference_price, 0.4, 1.6),
            np.clip(self.unit_cost / self.reference_price, 0.05, 0.8),
        ], dtype=np.float32)

    def reset(self, *, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)
        self.day = 0
        self.inventory = int(self.np_random.integers(140, self.max_inventory + 1))
        self.unit_cost = float(self.np_random.uniform(18, 32))
        self.current_price = float(self.np_random.uniform(38, 62))
        self.competitor_price = float(self.np_random.uniform(38, 62))
        self.demand_index = float(self.np_random.uniform(0.75, 1.25))
        self.previous_price = self.current_price
        return self._observation(), {"day": self.day}

    def step(self, action: int):
        if not self.action_space.contains(action):
            raise ValueError(f"Invalid action: {action}")

        self.day += 1
        self.previous_price = self.current_price
        multiplier = float(self.ACTION_MULTIPLIERS[int(action)])
        proposed_price = self.reference_price * multiplier

        # Limit price movement relative to the prior day's price.
        lower = self.previous_price * 0.80
        upper = self.previous_price * 1.20
        self.current_price = float(np.clip(proposed_price, lower, upper))

        # Demand responds to price vs. competitor and unit reference price.
        relative_price = self.current_price / max(self.competitor_price, 1.0)
        price_effect = np.exp(-2.0 * (relative_price - 1.0))
        expected_demand = 28.0 * self.demand_index * price_effect
        demand = max(0, int(self.np_random.poisson(max(expected_demand, 0.1))))
        units_sold = min(demand, self.inventory)
        revenue = units_sold * self.current_price
        gross_profit = units_sold * (self.current_price - self.unit_cost)
        stockout_penalty = 2.0 * max(demand - self.inventory, 0)
        price_change_penalty = 0.15 * abs(self.current_price - self.previous_price)
        reward = gross_profit - stockout_penalty - price_change_penalty

        self.inventory -= units_sold
        # Replenishment is deliberately simple and bounded.
        if self.inventory < 60:
            self.inventory = min(self.max_inventory, self.inventory + int(self.np_random.integers(35, 76)))
        self.demand_index = float(np.clip(
            self.demand_index + self.np_random.normal(0, 0.08), 0.45, 1.65
        ))
        self.competitor_price = float(np.clip(
            self.competitor_price + self.np_random.normal(0, 2.0), 30, 75
        ))

        terminated = self.day >= self.horizon
        truncated = False
        info = {
            "day": self.day,
            "price": round(self.current_price, 2),
            "units_sold": int(units_sold),
            "demand": int(demand),
            "revenue": round(float(revenue), 2),
            "profit": round(float(gross_profit), 2),
            "inventory": int(self.inventory),
            "competitor_price": round(self.competitor_price, 2),
        }
        return self._observation(), float(reward), terminated, truncated, info
