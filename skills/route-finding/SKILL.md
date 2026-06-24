# Route Finding Skill

## Purpose
Find the safest driving route between two NYC locations using
NetworkX graph traversal with crash-weighted edges.

## When to Use This Skill
- User asks for a route between two locations
- User asks "how do I get from X to Y safely"
- User wants to compare multiple route options

## Tools Available
- `find_safe_route(origin, destination)` → returns waypoints,
  distance, average risk score, and human review flag

## Execution Steps
1. Parse origin and destination from user message
2. Call find_safe_route tool with both locations
3. Check if needs_human_review is True
4. If high risk: warn user and ask for confirmation
5. If safe: present route with waypoints and risk scores
6. Always explain what the risk score means in plain language

## Output Format
- Lead with the recommendation (safe or caution)
- List waypoints with individual risk levels
- End with total distance and average risk score
- If high risk, always ask: "Do you want to proceed or
  see an alternative route?"