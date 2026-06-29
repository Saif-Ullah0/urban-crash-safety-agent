File 4: Main README.md
Open README.md and replace everything with:
markdown# Urban Crash Safety Agent

An AI agent that helps users navigate New York City safely by analyzing
historical crash data and recommending the lowest-risk routes.

Built for the [5-Day AI Agents: Intensive Vibe Coding Course with Google](https://kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google)
capstone project. Track: **Agents for Good**.

## Demo

Ask the agent anything about NYC road safety:
You: What is the safest route from Times Square to Brooklyn Bridge?
Agent: The route from Times Square to Brooklyn Bridge has an average

risk score of 0.53 (Medium). Here is the breakdown by waypoint:

Times Square: 0.404 (Medium)
34th St & 5th Ave: 0.35 (Low)
Canal St & Centre St: 0.619 (Medium)
Brooklyn Bridge: 0.756 (High)

Brooklyn Bridge has a HIGH crash risk score. Please exercise caution

approaching this area. Do you want to proceed or see an alternative route?

## What It Does

- Finds the safest driving route between two NYC locations
- Scores crash risk at each waypoint using a trained XGBoost model
- Flags high-risk routes and asks for human confirmation before proceeding
- Explains risk scores in plain language anyone can understand

## Course Concepts Demonstrated

| Concept | Where | Description |
|---|---|---|
| Agent Tools | `agent/tools.py` | XGBoost + NetworkX as callable tools |
| MCP Server | `mcp/crash_mcp_server.py` | Tools exposed via MCP protocol |
| Agent Skills | `skills/` | Modular SKILL.md files for each capability |
| Human-in-the-loop | `agent/agent.py` | High risk routes flagged for confirmation |
| Antigravity | Video demo | Built and run using Antigravity IDE |

## Architecture
User query

│

▼

Groq LLM (Llama 3.3 70B) ← reasons about query

│

├── find_safe_route() ← NetworkX road graph

│

└── score_crash_risk() ← XGBoost (F1: 0.848, AUC: 0.971)

trained on 500K+ NYC collisions

│

▼

Human-in-the-loop check (avg risk > 0.60 → warn + confirm)

│

▼

Plain-English response to user

## Setup

### Requirements
- Python 3.10+
- Groq API key (free at console.groq.com)

### Installation

```bash
git clone https://github.com/Saif-Ullah0/urban-crash-safety-agent
cd urban-crash-safety-agent
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:
GROQ_API_KEY=your_groq_api_key_here

### Run the agent

```bash
python -m agent.agent
```

### Run tests

```bash
python tests/test_agent.py
```

Expected output: 7 passed, 0 failed.

## Project Structure
urban-crash-safety-agent/

├── agent/

│   ├── agent.py          # Main agent with Groq + tool calling

│   └── tools.py          # XGBoost risk scoring + NetworkX routing

├── skills/

│   ├── route-finding/    # SKILL.md: when and how to find routes

│   ├── crash-risk-scoring/ # SKILL.md: risk score interpretation

│   └── explain-results/  # SKILL.md: plain-language communication

├── mcp/

│   └── crash_mcp_server.py # MCP server exposing tools via protocol

├── tests/

│   └── test_agent.py     # 7 tests, all passing

├── docs/

│   └── architecture.md   # Full architecture documentation

├── data/

│   └── README.md         # Dataset info and model details

└── requirements.txt

## Data

Built on the NYC Motor Vehicle Collisions dataset (500,000+ records,
NYC Open Data). XGBoost model trained with SMOTE for class balance.
See `data/README.md` for full details and how to add the trained model.

## Author

Saif Ullah Arshad
BS Computer Science, Information Technology University Lahore
[GitHub](https://github.com/Saif-Ullah0) |
[LinkedIn](https://linkedin.com/in/saif-ullah-arshad-40797a265)