# RL Dynamic Pricing Optimizer

A portfolio-ready reinforcement learning project that learns pricing decisions in a **simulated retail environment**. A Deep Q-Network (DQN) agent chooses among safe price multipliers to optimize cumulative profit while accounting for demand, inventory, competitor pricing, and price-change penalties.

> This is a research/demo simulator, not a system validated for real-world pricing decisions. All reported outcomes must come from your own evaluation runs.

## Features

- Custom Gymnasium environment with bounded actions and normalized observations
- DQN training with Stable-Baselines3 and a fixed random seed
- Evaluation against fixed-price and randomized baselines
- FastAPI inference API with input validation, health checks, model metadata, and structured responses
- Streamlit dashboard for interactive recommendations and episode simulations
- Unit tests and Render Blueprint configuration
- API designed to fail clearly if the trained model artifact is missing

## Architecture

```text
Gymnasium pricing simulator -> DQN training -> saved model artifact
                                               |
Browser -> Streamlit dashboard -> FastAPI -> DQN policy
                                      |
                               validated JSON response
```

## Local setup

Python 3.11 is recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python train.py --timesteps 50000 --eval-episodes 30
```

Training writes `models/pricing_dqn.zip` and `models/evaluation.json`.

Run the API in one terminal:

```bash
uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API docs.

Run the dashboard in another terminal:

```bash
# Windows PowerShell:
$env:API_URL="http://127.0.0.1:8000"
streamlit run dashboard.py
# macOS/Linux:
# API_URL=http://127.0.0.1:8000 streamlit run dashboard.py
```

Run tests:

```bash
pytest -q
```

## API example

`POST /recommend`

```json
{
  "unit_cost": 25,
  "current_price": 40,
  "competitor_price": 39,
  "demand_index": 1.0,
  "inventory": 120,
  "max_price_change_pct": 20
}
```

The response includes the recommended price, action multiplier, estimated simulated demand, estimated units sold, and estimated profit. These are simulator-based estimates, not guaranteed real-world outcomes.

## Deploy to Render

1. Push this repository to GitHub.
2. In Render, choose **New + → Blueprint** and select the repository containing `render.yaml`.
3. Review the two services: `rl-pricing-api` and `rl-pricing-dashboard`.
4. Deploy. The API build command trains the model artifact; this may take several minutes.
5. Once the API is live, Render should inject its URL into the dashboard service using `fromService`. If the dashboard fails to connect, set `API_URL` to the public API URL in the dashboard environment settings and redeploy.
6. Check `https://YOUR-API.onrender.com/health`, then open the dashboard URL.

Render free instances may sleep when idle and have limited CPU/RAM. If build-time training exceeds limits, train locally, commit the generated `models/pricing_dqn.zip` artifact, and change the API build command to install dependencies only. Avoid committing large model files unless needed and permitted by your repository policy.

## Production-minded design choices

- Input bounds and domain validation via Pydantic
- Safe action space and maximum price-change constraint
- Deterministic inference by default
- Health endpoint and model readiness reporting
- Reproducible seed, separate evaluation episodes, baseline comparisons
- Unit tests for environment and request validation
- Explicit distinction between simulated metrics and real business outcomes

## Resume bullet (use only after completing and measuring the project)

**RL Dynamic Pricing Optimizer:** Built a DQN-based pricing agent using Gymnasium and Stable-Baselines3; deployed a validated FastAPI inference service and Streamlit dashboard on Render, evaluating cumulative profit against fixed-price and randomized baselines in a simulated retail environment.

Add measured results only after running evaluation, e.g. “improved simulated episode profit by X% over the fixed-price baseline across N evaluation episodes.” Do not claim a percentage before measuring it.

## Suggested next steps

- Log API requests and outcomes to a database
- Add model/version tracking and drift monitoring
- Evaluate robustness across different demand elasticity and competitor-price scenarios
- Add a human approval gate before any real price change
