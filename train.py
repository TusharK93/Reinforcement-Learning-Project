from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

from pricing_env import PricingEnv

MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "pricing_dqn"


def run_baseline(kind: str, episodes: int, seed: int = 2026) -> dict:
    env = PricingEnv(seed=seed)
    episode_rewards, episode_profits = [], []
    for episode in range(episodes):
        obs, _ = env.reset(seed=seed + episode)
        done = False
        total_reward = 0.0
        total_profit = 0.0
        while not done:
            if kind == "fixed":
                # Closest action to reference price.
                action = 2
            else:
                action = int(env.action_space.sample())
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            total_reward += reward
            total_profit += info["profit"]
        episode_rewards.append(total_reward)
        episode_profits.append(total_profit)
    env.close()
    return {
        "mean_episode_reward": float(np.mean(episode_rewards)),
        "std_episode_reward": float(np.std(episode_rewards)),
        "mean_episode_profit": float(np.mean(episode_profits)),
        "episodes": episodes,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timesteps", type=int, default=50000)
    parser.add_argument("--eval-episodes", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.timesteps < 1000:
        parser.error("--timesteps should be at least 1000 for a useful training run")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    train_env = Monitor(PricingEnv(seed=args.seed))
    model = DQN(
        "MlpPolicy",
        train_env,
        learning_rate=1e-3,
        buffer_size=30000,
        learning_starts=1000,
        batch_size=64,
        gamma=0.98,
        train_freq=4,
        target_update_interval=500,
        exploration_fraction=0.30,
        exploration_final_eps=0.05,
        verbose=1,
        seed=args.seed,
        device="cpu",
    )
    model.learn(total_timesteps=args.timesteps, progress_bar=False)
    model.save(str(MODEL_PATH))
    train_env.close()

    eval_env = Monitor(PricingEnv(seed=args.seed + 1000))
    mean_reward, std_reward = evaluate_policy(
        model, eval_env, n_eval_episodes=args.eval_episodes, deterministic=True
    )
    learned = {
        "mean_episode_reward": float(mean_reward),
        "std_episode_reward": float(std_reward),
        "episodes": args.eval_episodes,
    }
    eval_env.close()
    results = {
        "algorithm": "DQN",
        "timesteps": args.timesteps,
        "seed": args.seed,
        "learned_agent": learned,
        "fixed_price_baseline": run_baseline("fixed", args.eval_episodes, args.seed + 2000),
        "random_baseline": run_baseline("random", args.eval_episodes, args.seed + 3000),
        "note": "Synthetic simulator metrics only; compare like-for-like profit and reward before making claims.",
    }
    (MODEL_DIR / "evaluation.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
