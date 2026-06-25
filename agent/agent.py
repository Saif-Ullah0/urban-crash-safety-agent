
"""
Urban Crash Safety Agent - Main Agent
ADK-powered conversational agent for safe route recommendations
in NYC using crash risk scoring and NetworkX routing.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent.tools import crash_risk_tool, safe_route_tool

load_dotenv()

# ─── Agent Definition ───────

crash_safety_agent = Agent(
    name="urban_crash_safety_agent",
    model="gemini-2.5-flash",    
    description=(
        "An AI agent that helps users navigate NYC safely by analyzing "
        "crash risk along routes and recommending the safest path."
    ),
    instruction="""
    You are the Urban Crash Safety Agent, an expert in NYC road safety.
    
    Your job is to help users find the safest routes in New York City
    by analyzing historical crash data and scoring risk along their path.
    
    When a user asks about a route:
    1. Use the find_safe_route tool to get route options and risk scores
    2. Use the score_crash_risk tool if they ask about a specific location
    3. If the route has HIGH risk (needs_human_review = True), ALWAYS warn
       the user clearly and ask them to confirm before proceeding
    4. Explain your recommendations in plain, simple language
    5. Always mention the risk score and what it means
    
    You care deeply about user safety. Never recommend a high-risk route
    without a clear warning and user confirmation. This is your most
    important rule.
    
    Example interactions:
    - "What is the safest route from Times Square to Brooklyn Bridge?"
    - "Is it safe to drive through Midtown at night?"
    - "What is the crash risk near Central Park?"
    """,
    tools=[crash_risk_tool, safe_route_tool],
)


# ─── Session and Runner Setup ───

session_service = InMemorySessionService()

runner = Runner(
    agent=crash_safety_agent,
    app_name="urban_crash_safety_agent",
    session_service=session_service,
)


# ─── Human-in-the-Loop Check ───

def check_human_review(response: dict) -> bool:
    """
    Checks if agent response contains a high risk route
    that needs human confirmation before proceeding.
    """
    if isinstance(response, dict):
        return response.get("needs_human_review", False)
    return False


# ─── Main Conversation Loop ─

async def run_agent(user_message: str, session_id: str = "default") -> str:
    """
    Runs the agent with a user message and returns its response.
    Implements human-in-the-loop for high risk routes.
    
    Args:
        user_message: The user's question or request
        session_id: Conversation session ID for context memory
    
    Returns:
        Agent's response as a string
    """
    # Create session if it doesn't exist yet
    existing_sessions = await session_service.list_sessions(
        app_name="urban_crash_safety_agent",
        user_id="user_001",
    )
    session_ids = [s.id for s in existing_sessions.sessions]
    
    if session_id not in session_ids:
        await session_service.create_session(
            app_name="urban_crash_safety_agent",
            user_id="user_001",
            session_id=session_id,
        )

    content = types.Content(
        role="user",
        parts=[types.Part(text=user_message)]
    )

    final_response = ""

    async for event in runner.run_async(
        user_id="user_001",
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    return final_response

# ─── CLI Entry Point ────────

if __name__ == "__main__":
    import asyncio

    print("Urban Crash Safety Agent")
    print("=" * 40)
    print("Ask me about safe routes in NYC.")
    print("Type 'quit' to exit.\n")

    session_id = "cli_session_001"

    async def main():
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["quit", "exit"]:
                print("Stay safe out there!")
                break
            if not user_input:
                continue

            print("Agent: thinking...")
            response = await run_agent(user_input, session_id)
            print(f"Agent: {response}\n")

    asyncio.run(main())