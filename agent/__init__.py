
"""
Urban Crash Safety Agent
A multi-tool AI agent for safe route recommendations in NYC.
Demonstrates: Agent Tools, MCP Server, Agent Skills, Human-in-the-Loop.
"""

from agent.tools import score_crash_risk, find_safe_route
from agent.agent import run_agent

__all__ = ["score_crash_risk", "find_safe_route", "run_agent"]