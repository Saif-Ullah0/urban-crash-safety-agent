"""
Urban Crash Safety Agent - Tests
Basic tests to verify tools work correctly and
human-in-the-loop triggers on high risk routes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.tools import score_crash_risk, find_safe_route


# ─── Crash Risk Scoring Tests 

def test_score_crash_risk_returns_valid_structure():
    """Result must have all required keys."""
    result = score_crash_risk(40.7580, -73.9855)
    assert "risk_score" in result
    assert "risk_level" in result
    assert "explanation" in result
    print("PASS: score_crash_risk returns valid structure")


def test_score_crash_risk_score_in_range():
    """Risk score must be between 0 and 1."""
    result = score_crash_risk(40.7580, -73.9855)
    assert 0.0 <= result["risk_score"] <= 1.0
    print(f"PASS: risk_score {result['risk_score']} is in valid range")


def test_score_crash_risk_level_valid():
    """Risk level must be Low, Medium, or High."""
    result = score_crash_risk(40.7580, -73.9855)
    assert result["risk_level"] in ["Low", "Medium", "High"]
    print(f"PASS: risk_level '{result['risk_level']}' is valid")


# ─── Safe Route Finding Tests ─

def test_find_safe_route_returns_valid_structure():
    """Route result must have all required keys."""
    result = find_safe_route("Times Square", "Brooklyn Bridge")
    assert "origin" in result
    assert "destination" in result
    assert "waypoints" in result
    assert "average_risk_score" in result
    assert "needs_human_review" in result
    assert "recommendation" in result
    print("PASS: find_safe_route returns valid structure")


def test_find_safe_route_has_waypoints():
    """Route must have at least 2 waypoints."""
    result = find_safe_route("Times Square", "Brooklyn Bridge")
    assert len(result["waypoints"]) >= 2
    print(f"PASS: route has {len(result['waypoints'])} waypoints")


def test_find_safe_route_human_review_flag():
    """needs_human_review must be True when avg risk above 0.60."""
    result = find_safe_route("Times Square", "Brooklyn Bridge")
    if result["average_risk_score"] > 0.60:
        assert result["needs_human_review"] == True
        print("PASS: high risk route correctly flagged for human review")
    else:
        assert result["needs_human_review"] == False
        print("PASS: safe route correctly not flagged for human review")


def test_waypoints_have_risk_scores():
    """Each waypoint must have a risk score and level."""
    result = find_safe_route("Times Square", "Brooklyn Bridge")
    for wp in result["waypoints"]:
        assert "risk_score" in wp
        assert "risk_level" in wp
    print("PASS: all waypoints have risk scores")


# ─── Run All Tests ─────

if __name__ == "__main__":
    print("Running Urban Crash Safety Agent Tests")
    print("=" * 45)

    tests = [
        test_score_crash_risk_returns_valid_structure,
        test_score_crash_risk_score_in_range,
        test_score_crash_risk_level_valid,
        test_find_safe_route_returns_valid_structure,
        test_find_safe_route_has_waypoints,
        test_find_safe_route_human_review_flag,
        test_waypoints_have_risk_scores,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__} → {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__} → {e}")
            failed += 1

    print("=" * 45)
    print(f"Results: {passed} passed, {failed} failed")