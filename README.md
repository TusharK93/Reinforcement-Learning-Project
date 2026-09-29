# RL Dynamic Pricing Optimizer

<<<<<<< HEAD
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
=======
An intelligent dynamic pricing system that uses Reinforcement Learning (RL) to recommend product prices based on business conditions such as production cost, competitor pricing, demand, and inventory.

The project exposes a REST API built with FastAPI and is designed for deployment on Render.

## Overview

Traditional pricing strategies often rely on fixed prices or manually defined rules. This project explores how Reinforcement Learning can support adaptive pricing decisions by evaluating different business conditions and selecting pricing actions.

The system accepts pricing-related inputs and returns a recommended price along with estimated demand, sales, revenue, and profit.

## Key Features

- **Reinforcement Learning:** Uses a pricing policy to select pricing actions.
- **Dynamic Pricing:** Recommends prices based on supplied business conditions.
- **FastAPI REST API:** Provides endpoints for pricing recommendations.
- **Demand and Inventory Awareness:** Incorporates demand indicators and inventory levels into pricing requests.
- **Pricing Constraints:** Supports a configurable maximum percentage price change.
- **API Validation:** Validates incoming requests using FastAPI and Pydantic.
- **Interactive API Documentation:** Tests endpoints through Swagger UI.
- **Deployment Ready:** Configured for deployment as a web service on Render.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Reinforcement Learning | Pricing decision-making |
| FastAPI | REST API development |
| Pydantic | Request validation |
| Uvicorn | ASGI server |
| Gymnasium | Reinforcement Learning environments, if used in the implementation |
| Stable-Baselines3 | RL algorithms, if used in the implementation |
| Render | Cloud deployment |
| Git and GitHub | Version control and project hosting |

## How It Works

1. **Input collection:** Receives product cost, current price, competitor price, demand index, inventory, and maximum price adjustment.
2. **State representation:** Uses the relevant business variables as inputs to the pricing decision logic.
3. **Action selection:** The pricing policy selects an available pricing action.
4. **Price recommendation:** The selected action is converted into a recommended selling price.
5. **Performance estimation:** The API returns estimated demand, units sold, revenue, and profit.
6. **API response:** The results are returned as JSON for integration with other applications.

The quality of the recommendations depends on the environment design, reward function, training process, and model evaluation.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns API information |
| GET | `/health` | Checks API health and model status |
| POST | `/recommend` | Generates a pricing recommendation |
| GET | `/docs` | Opens interactive Swagger documentation |

## Getting Started

### 1. Clone the repository

```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/TusharK93/Reinforcement-Learning-Project.git)
cd YOUR_REPOSITORY
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Make sure `requirements.txt` contains the packages required by your implementation.

### 4. Start the API locally

From the project root directory, run:
>>>>>>> 1d2c89d014e8c4f7e84cc28cd0fd321decdc7483

```bash
uvicorn api.main:app --reload
```

<<<<<<< HEAD
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
=======
The API should be available at:

- API home: http://127.0.0.1:8000/
- Health check: http://127.0.0.1:8000/health
- Swagger documentation: http://127.0.0.1:8000/docs

Keep the terminal running while testing the API.

## Example API Request

Open `http://127.0.0.1:8000/docs`, expand `POST /recommend`, select **Try it out**, and submit the following JSON.

```json
{
  "unit_cost": 23,
  "current_price": 453,
  "competitor_price": 440,
  "demand_index": 1.2,
  "inventory": 100,
>>>>>>> 1d2c89d014e8c4f7e84cc28cd0fd321decdc7483
  "max_price_change_pct": 20
}
```

<<<<<<< HEAD
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
=======
### Input Parameters

| Parameter | Description |
|---|---|
| `unit_cost` | Cost per product unit |
| `current_price` | Current selling price |
| `competitor_price` | Competitor's selling price |
| `demand_index` | Demand indicator |
| `inventory` | Available stock |
| `max_price_change_pct` | Maximum permitted percentage price adjustment |

The example uses the demand-index limit confirmed by the current API validation error. Check your API schema for any additional constraints.

## Example Response Structure

The endpoint documents a response containing fields similar to the following:

```json
{
  "recommended_price": 0,
  "action_multiplier": 0,
  "estimated_demand": 0,
  "estimated_units_sold": 0,
  "estimated_revenue": 0,
  "estimated_profit": 0,
  "model": "string",
  "disclaimer": "string"
}
```

These values illustrate the response schema only. Actual values depend on the pricing policy and implementation.

## Deploy on Render

### 1. Push the project to GitHub

```bash
git add .
git commit -m "Add RL dynamic pricing optimizer"
git push
```

### 2. Create a Render Web Service

1. Sign in to [Render](https://dashboard.render.com/).
2. Select **New + → Web Service**.
3. Connect your GitHub repository.
4. Select the branch to deploy.

### 3. Configure the service

| Setting | Value |
|---|---|
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn api.main:app --host 0.0.0.0 --port $PORT` |

If you already have a `render.yaml`, use its service configuration where appropriate.

### 4. Verify the deployment

After deployment, use your assigned Render URL:

- `https://YOUR-SERVICE.onrender.com/`
- `https://YOUR-SERVICE.onrender.com/health`
- `https://YOUR-SERVICE.onrender.com/docs`

Replace `YOUR-SERVICE` with the actual service hostname.

Test `POST /recommend` through the public Swagger documentation to verify that pricing recommendations work in the deployed environment.

**Deployment note:** Ensure any trained model files are included or otherwise made available to the deployed service, and that the application loads them correctly at startup.

## Project Structure

The following is an illustrative structure. Adjust it to match the files in your repository.

```text
rl_dynamic_pricing/
├── api/
│   └── main.py
├── models/
│   └── trained model artifacts
├── tests/
│   └── test_env.py
├── train.py
├── pricing_env.py
├── requirements.txt
├── render.yaml
├── .gitignore
└── README.md
```

## Testing and Evaluation

Recommended evaluation tasks include:

- Compare the learned policy with a fixed-price baseline.
- Measure total revenue and profit across simulated episodes.
- Evaluate pricing behavior under different demand and inventory conditions.
- Verify that price changes remain within configured limits.
- Test API validation and error handling.
- Track cumulative rewards during training.

Report numerical performance improvements only after running the experiments and verifying the results.

## Future Improvements

- Build a Streamlit dashboard for interactive pricing analysis.
- Add demand forecasting and competitor-price data integrations.
- Compare multiple RL algorithms and baseline pricing strategies.
- Add automated tests and continuous integration.
- Track model performance and pricing decisions.
- Implement experiment logging and reproducible training.

## Disclaimer

This project is an experimental pricing decision-support system. Its estimates are not guaranteed to match real-world market outcomes. Recommendations depend on the model, assumptions, simulated environment, and quality of input data.

## Author

**Your Name**

GitHub: https://github.com/TusharK93

LinkedIn: Add your LinkedIn profile URL.

---

If you find this project useful, consider giving the repository a star.
>>>>>>> 1d2c89d014e8c4f7e84cc28cd0fd321decdc7483
