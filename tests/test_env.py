import numpy as np
import pytest

from pricing_env import PricingEnv
from api.main import PricingRequest


def test_env_observation_and_step():
    env = PricingEnv(seed=7)
    obs, info = env.reset(seed=7)
    assert env.observation_space.contains(obs)
    next_obs, reward, terminated, truncated, info = env.step(2)
    assert env.observation_space.contains(next_obs)
    assert np.isfinite(reward)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert info["units_sold"] >= 0


def test_invalid_action_rejected():
    env = PricingEnv(seed=1)
    with pytest.raises(ValueError):
        env.step(999)


def test_request_rejects_price_below_cost():
    with pytest.raises(Exception):
        PricingRequest(unit_cost=50, current_price=40, competitor_price=42)


def test_request_validates_change_limit():
    with pytest.raises(Exception):
        PricingRequest(
            unit_cost=20, current_price=40, competitor_price=42,
            max_price_change_pct=90
        )
