"""
F_conv Integration — Next-Turn Retrospective Scoring
=====================================================

Scores the agent's previous response(s) at the start of the next turn.
This guarantees A6 compliance structurally: the response was already
delivered before scoring begins.

Integration point: called at session start or turn start, before
the agent processes the new inbound message.

Usage:
    from f_conv.integration import score_previous_responses
    score_previous_responses(session_key="current_session")
"""

import json
import time
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from f_conv.engine import compute_f_conv, register_action, load_pa_config

# Track what we've already scored to avoid double-scoring
SCORED_INDEX_PATH = Path.home() / ".openclaw" / "workspace" / "governed-agent" / "data" / "scored_index.json"


def _load_scored_index() -> Dict[str, Any]:
    """Load the index of already-scored responses."""
    if SCORED_INDEX_PATH.exists():
        with open(SCORED_INDEX_PATH) as f:
            return json.load(f)
    return {"last_scored_timestamp": 0, "scored_count": 0}


def _save_scored_index(index: Dict[str, Any]):
    """Save the scored index."""
    SCORED_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SCORED_INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)


def extract_my_responses_from_session(session_history: List[Dict]) -> List[Dict[str, Any]]:
    """
    Extract agent responses from session history.
    
    Expects format: [{"role": "assistant", "content": "...", "timestamp": ...}, ...]
    Filters to assistant messages only. Skips tool calls.
    """
    responses = []
    for msg in session_history:
        if msg.get("role") == "assistant" and msg.get("content"):
            content = msg["content"]
            # Skip pure tool-call turns, NO_REPLY, HEARTBEAT_OK
            if content.strip() in ("NO_REPLY", "HEARTBEAT_OK"):
                continue
            if len(content.strip()) < 5:
                continue
            responses.append({
                "content": content,
                "timestamp": msg.get("timestamp", time.time()),
            })
    return responses


def extract_tool_actions_from_session(session_history: List[Dict]) -> List[str]:
    """
    Extract tool action descriptions from session history for ρ_wt.
    
    Looks for tool_use entries and constructs action text from tool name + params.
    """
    actions = []
    for msg in session_history:
        if msg.get("role") == "assistant" and msg.get("tool_calls"):
            for tc in msg["tool_calls"]:
                tool_name = tc.get("name", tc.get("function", {}).get("name", "unknown"))
                # Build a simple action description
                action_text = f"Tool call: {tool_name}"
                actions.append(action_text)
    return actions


def score_previous_responses(
    responses: Optional[List[Dict[str, Any]]] = None,
    tool_actions: Optional[List[str]] = None,
    session_key: str = "unknown"
) -> List[Dict[str, Any]]:
    """
    Score any unscored previous responses.
    
    Call this at the START of a new turn, before processing inbound.
    
    Args:
        responses: List of {"content": str, "timestamp": float} dicts.
                   If None, caller must provide them from session history.
        tool_actions: List of tool action description strings for ρ_wt.
        session_key: Current session identifier.
    
    Returns:
        List of scoring results for newly scored responses.
    """
    if responses is None:
        return []
    
    # Load PA config if not already loaded
    try:
        load_pa_config()
    except FileNotFoundError:
        return []
    
    # Load scored index
    index = _load_scored_index()
    last_ts = index.get("last_scored_timestamp", 0)
    
    # Register tool actions for ρ_wt
    if tool_actions:
        for action in tool_actions:
            register_action(action)
    
    # Score unscored responses
    results = []
    for resp in responses:
        ts = resp.get("timestamp", 0)
        if ts <= last_ts:
            continue  # Already scored
        
        content = resp["content"]
        
        # Set session ID for the record
        os.environ["OPENCLAW_SESSION_ID"] = session_key
        
        # Compute F_conv (this logs to JSONL automatically)
        result = compute_f_conv(content)
        results.append(result)
    
    # Update index
    if results:
        latest_ts = max(r.get("unix_ts", 0) for r in results)
        index["last_scored_timestamp"] = latest_ts
        index["scored_count"] = index.get("scored_count", 0) + len(results)
        _save_scored_index(index)
    
    return results


def score_single_response(response_text: str, session_key: str = "unknown") -> Dict[str, Any]:
    """
    Score a single response. Convenience wrapper.
    
    Use this when you have the response text directly
    (e.g., from a heartbeat that reads recent session history).
    """
    os.environ["OPENCLAW_SESSION_ID"] = session_key
    try:
        load_pa_config()
    except FileNotFoundError:
        return {"error": "PA config not found"}
    
    return compute_f_conv(response_text)
