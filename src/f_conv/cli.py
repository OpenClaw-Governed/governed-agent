"""
F_conv CLI — manual scoring and summary tools.

Usage:
    python cli.py score "Your response text here"
    python cli.py summary
    python cli.py baseline-status
    python cli.py test
"""

import sys
import json
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from f_conv.engine import compute_f_conv, load_pa_config, get_summary, get_baseline_status


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == "score":
        if len(sys.argv) < 3:
            print("Usage: python cli.py score \"response text\"")
            return
        text = " ".join(sys.argv[2:])
        result = compute_f_conv(text)
        print(json.dumps(result, indent=2))
    
    elif cmd == "summary":
        summary = get_summary()
        print(json.dumps(summary, indent=2))
    
    elif cmd == "baseline-status":
        status = get_baseline_status()
        print(json.dumps(status, indent=2))
    
    elif cmd == "test":
        # Run a quick self-test with sample responses
        print("Loading PA config...")
        config = load_pa_config()
        print(f"PA config loaded. Hash: {config.get('version', 'unknown')}")
        print()
        
        test_responses = [
            ("High alignment", "The TELOS governance framework ensures that every tool call is scored against the Primacy Attractor before execution, maintaining human oversight through the EXECUTE, CLARIFY, and ESCALATE verdict cascade."),
            ("Medium alignment", "I built a new dashboard page for Mission Control that displays social media engagement metrics and content pipeline status."),
            ("Low alignment", "The weather today is sunny with a high of 72 degrees and a slight breeze from the west."),
            ("Short response", "Yes, done."),
        ]
        
        for label, text in test_responses:
            result = compute_f_conv(text)
            print(f"{label}:")
            print(f"  F_conv: {result['f_conv']:.4f}")
            print(f"  Condition: {result['condition']}")
            print(f"  Energy: {result['lyapunov_energy']:.4f}")
            print(f"  Words: {result['response_word_count']}")
            print(f"  Short: {result['short_flag']}")
            print()
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
