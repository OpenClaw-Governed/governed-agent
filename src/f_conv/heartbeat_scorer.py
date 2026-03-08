"""
F_conv Heartbeat Scorer
========================

Standalone script that scores recent agent responses from session history.
Designed to run from a heartbeat or cron job.

Usage:
    python heartbeat_scorer.py [--last-n 5] [--session-key KEY]
    
How it works:
    1. Reads recent session messages via OpenClaw sessions_history
       (or from a message dump file)
    2. Identifies unscored assistant responses
    3. Scores each one post-hoc (A6 compliant — responses already delivered)
    4. Logs results to ps_oc_log.jsonl
    5. Prints summary

In practice, the main agent calls this logic during heartbeats or
at the start of turns via the integration module.
"""

import json
import sys
import os
from pathlib import Path

# Add parent paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from f_conv.engine import compute_f_conv, register_action, load_pa_config, get_summary


def score_from_file(filepath: str, last_n: int = 5) -> None:
    """
    Score responses from a JSON message dump file.
    
    Expected format: list of {"role": "...", "content": "...", "timestamp": ...}
    """
    load_pa_config()
    
    with open(filepath) as f:
        messages = json.load(f)
    
    # Filter to assistant messages
    responses = [
        m for m in messages
        if m.get("role") == "assistant"
        and m.get("content")
        and m["content"].strip() not in ("NO_REPLY", "HEARTBEAT_OK")
        and len(m["content"].strip()) >= 5
    ]
    
    # Take last N
    responses = responses[-last_n:]
    
    print(f"Scoring {len(responses)} responses...")
    print()
    
    for i, resp in enumerate(responses):
        content = resp["content"]
        # Truncate display
        preview = content[:80].replace("\n", " ")
        if len(content) > 80:
            preview += "..."
        
        result = compute_f_conv(content)
        
        print(f"  [{i+1}] F_conv: {result['f_conv']:.4f} | "
              f"Energy: {result['lyapunov_energy']:.4f} | "
              f"Words: {result['response_word_count']} | "
              f"Condition: {result['condition']}")
        print(f"      {preview}")
        print()
    
    # Print summary
    summary = get_summary()
    print(f"Total records: {summary['records']}")
    if summary.get('f_conv_mean'):
        print(f"F_conv mean: {summary['f_conv_mean']:.4f} | "
              f"std: {summary.get('f_conv_std', 0):.4f} | "
              f"range: [{summary.get('f_conv_min', 0):.4f}, {summary.get('f_conv_max', 0):.4f}]")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="F_conv Heartbeat Scorer")
    parser.add_argument("--file", "-f", help="JSON message dump to score")
    parser.add_argument("--last-n", "-n", type=int, default=5, help="Score last N responses")
    parser.add_argument("--summary", "-s", action="store_true", help="Show summary only")
    args = parser.parse_args()
    
    if args.summary:
        summary = get_summary()
        print(json.dumps(summary, indent=2))
        return
    
    if args.file:
        score_from_file(args.file, last_n=args.last_n)
    else:
        print("No input provided. Use --file or pipe session history.")
        print("Usage: python heartbeat_scorer.py --file messages.json --last-n 5")


if __name__ == "__main__":
    main()
