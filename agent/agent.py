"""
Urban Crash Safety Agent - Main Agent
Conversational agent for safe route recommendations in NYC
using crash risk scoring and NetworkX routing.
Powered by Groq (Llama 3.3 70B) for fast, free inference.
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq

from agent.tools import score_crash_risk, find_safe_route

load_dotenv()

# ─── Groq Client Setup ──

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ─── Tool Definitions for Groq ───────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_safe_route",
            "description": (
                "Finds the safest driving route between two NYC locations. "
                "Returns waypoints, risk scores, and flags high-risk routes "
                "for human review before proceeding."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Starting location in NYC"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Ending location in NYC"
                    }
                },
                "required": ["origin", "destination"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "score_crash_risk",
            "description": (
                "Scores the crash risk at a GPS coordinate in NYC. "
                "Uses XGBoost model trained on 500,000+ collision records. "
                "Returns risk score 0-1, risk level, and explanation."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "GPS latitude"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "GPS longitude"
                    }
                },
                "required": ["latitude", "longitude"]
            }
        }
    }
]

# ─── System Prompt ──────

SYSTEM_PROMPT = """
You are the Urban Crash Safety Agent, an expert in NYC road safety.

Your job is to help users find the safest routes in New York City
by analyzing historical crash data and scoring risk along their path.

When a user asks about a route:
1. Use the find_safe_route tool to get route options and risk scores
2. Use score_crash_risk if they ask about a specific location
3. If the route has HIGH risk (needs_human_review = True), ALWAYS warn
   the user clearly and ask them to confirm before proceeding
4. Explain your recommendations in plain, simple language
5. Always mention the risk score and what it means

You care deeply about user safety. Never recommend a high-risk route
without a clear warning and user confirmation.
"""

# ─── Tool Dispatcher ────

def dispatch_tool(tool_name: str, tool_args: dict) -> str:
    """
    Calls the appropriate tool function and returns result as JSON string.
    This is the human-in-the-loop checkpoint: high risk routes
    are flagged in the tool result, and the agent surfaces them to the user.
    """
    if tool_name == "find_safe_route":
        result = find_safe_route(**tool_args)
    elif tool_name == "score_crash_risk":
        result = score_crash_risk(**tool_args)
    else:
        result = {"error": f"Unknown tool: {tool_name}"}

    return json.dumps(result, indent=2)


# ─── Agent Runner ─

def run_agent(user_message: str, conversation_history: list) -> tuple[str, list]:
    """
    Runs one turn of the agent conversation.
    Handles tool calls automatically and returns the final response.

    Args:
        user_message: The user's input
        conversation_history: Full conversation so far (for session memory)

    Returns:
        Tuple of (agent_response, updated_history)
    """
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    # First call: agent decides what to do
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        max_tokens=2048,
    )

    response_message = response.choices[0].message

    # If agent wants to call tools, handle them
    if response_message.tool_calls:
        # Add agent's tool-calling message to history
        conversation_history.append({
            "role": "assistant",
            "content": response_message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in response_message.tool_calls
            ]
        })

        # Call each tool and collect results
        for tool_call in response_message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            tool_result = dispatch_tool(tool_name, tool_args)

            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

        # Second call: agent formulates final response using tool results
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=2048,
        )
        final_text = final_response.choices[0].message.content

    else:
        # No tool calls needed, direct response
        final_text = response_message.content

    # Add agent response to history
    conversation_history.append({
        "role": "assistant",
        "content": final_text
    })

    return final_text, conversation_history


# ─── CLI Entry Point ─────

if __name__ == "__main__":
    print("Urban Crash Safety Agent")
    print("=" * 40)
    print("Powered by Groq (Llama 3.3 70B)")
    print("Ask me about safe routes in NYC.")
    print("Type 'quit' to exit.\n")

    conversation_history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["quit", "exit"]:
            print("Stay safe out there!")
            break
        if not user_input:
            continue

        print("Agent: thinking...")
        response, conversation_history = run_agent(user_input, conversation_history)
        print(f"Agent: {response}\n")