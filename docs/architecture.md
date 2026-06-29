# Architecture

## System Overview

The Urban Crash Safety Agent is a multi-tool AI agent built with
Google ADK patterns, powered by Groq (Llama 3.3 70B), and backed
by a trained XGBoost crash risk model and NetworkX road graph.

## Architecture Diagram



## Key Concepts Demonstrated

### 1. Agent Tools (Day 2)
Two Python functions are registered as callable tools:
- `find_safe_route`: NetworkX-based route finder with crash-weighted edges
- `score_crash_risk`: XGBoost model scoring collision probability at GPS coords

The LLM decides when to call each tool based on the user's query.
It never hardcodes routing logic, it delegates to the tools.

### 2. Agent Skills (Day 3)
Three SKILL.md files provide modular, on-demand instructions:
- `skills/route-finding/SKILL.md`: when and how to find routes
- `skills/crash-risk-scoring/SKILL.md`: how to interpret risk scores
- `skills/explain-results/SKILL.md`: how to communicate results clearly

Skills keep the system prompt lightweight. Only relevant skills
are loaded when the agent actually needs them.

### 3. MCP Server (Day 2)
`mcp/crash_mcp_server.py` exposes both tools as MCP-compatible endpoints.
Any MCP-compatible client (Antigravity, Claude Desktop, etc.) can connect
and use the crash risk and routing capabilities without custom integration.

### 4. Human-in-the-Loop Security (Day 4)
When `needs_human_review = True` (avg risk above 0.60), the agent:
- Clearly warns the user about high crash risk
- Explains which waypoints are dangerous and why
- Asks for explicit user confirmation before proceeding
- Never silently routes through a high-risk area

This implements the "Effective Trust" principle from Day 4:
trust is continuous and verified, not a one-time checkbox.

## Tech Stack

| Component | Technology |
|---|---|
| Agent framework | Google ADK patterns |
| LLM | Groq API, Llama 3.3 70B |
| Route finding | NetworkX |
| Risk scoring | XGBoost (F1: 0.848, AUC: 0.971) |
| Spatial data | GeoPandas, Shapely |
| MCP server | FastAPI + MCP SDK |
| Observability | OpenTelemetry |
| Testing | Python unittest |
| Data | NYC Open Data (500K+ collision records) |