"""
F_conv Universal Scorer
========================

Scores ALL semantic output from the agent, not just chat responses.

Every string the agent generates that carries semantic content is a
scorable object: chat responses, diary entries, documentation, commit
messages, research notes, advisory prompts, code comments, memory
entries, governance moment logs, pulse entries.

The F_conv distribution represents the agent's TOTAL verbal alignment
across all output modalities.

TKey: TKEY-PS-OC-2026-0308-001
Amendment A6: All scoring is post-hoc (after the output is finalized).
"""

import json
import time
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from enum import Enum

from f_conv.engine import compute_f_conv, register_action, load_pa_config


class OutputType(str, Enum):
    """Classification of agent output modalities."""
    CHAT_RESPONSE = "chat_response"
    DIARY_ENTRY = "diary_entry"
    DIARY_DRAFT = "diary_draft"
    RESEARCH_NOTE = "research_note"
    PROPOSAL = "proposal"
    COMMIT_MESSAGE = "commit_message"
    PULSE_LOG = "pulse_log"
    DOCUMENTATION = "documentation"
    README = "readme"
    ADVISORY_PROMPT = "advisory_prompt"
    CODE_COMMENT = "code_comment"
    MEMORY_ENTRY = "memory_entry"
    GOVERNANCE_MOMENT = "governance_moment"
    DATASHEET = "datasheet"
    CONSTRAINT_DOC = "constraint_doc"
    FILE_CONTENT = "file_content"


# Extended log path for universal scoring
UNIVERSAL_LOG_PATH = Path.home() / ".openclaw" / "workspace" / "governed-agent" / "data" / "f_conv_universal.jsonl"


def score_output(
    content: str,
    output_type: OutputType,
    source_path: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    session_key: str = "unknown"
) -> Dict[str, Any]:
    """
    Score any semantic output from the agent.
    
    Args:
        content: The text content to score.
        output_type: Classification of the output modality.
        source_path: File path if the output was written to a file.
        metadata: Additional context (commit hash, diary entry number, etc.)
        session_key: Current session identifier.
    
    Returns:
        Scoring result with output_type and source metadata.
    """
    # Load PA if needed
    try:
        load_pa_config()
    except FileNotFoundError:
        return {"error": "PA config not found"}
    
    os.environ["OPENCLAW_SESSION_ID"] = session_key
    
    # For very long content (docs, diary entries), score in chunks
    # and report both chunk scores and aggregate
    if len(content) > 2000:
        return _score_long_content(content, output_type, source_path, metadata)
    
    # Standard scoring
    result = compute_f_conv(content)
    
    # Augment with universal metadata
    result["output_type"] = output_type.value
    result["source_path"] = source_path
    if metadata:
        result["metadata"] = metadata
    
    # Log to universal log
    _log_universal(result)
    
    return result


def _score_long_content(
    content: str,
    output_type: OutputType,
    source_path: Optional[str],
    metadata: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Score long content by chunking into ~500 word segments.
    Reports per-chunk scores and weighted aggregate.
    """
    import numpy as np
    
    words = content.split()
    chunk_size = 500
    chunks = []
    
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i:i + chunk_size])
        chunks.append(chunk_text)
    
    # Score each chunk
    chunk_results = []
    for i, chunk in enumerate(chunks):
        result = compute_f_conv(chunk)
        result["chunk_index"] = i
        result["chunk_word_count"] = len(chunk.split())
        chunk_results.append(result)
    
    # Compute weighted aggregate (weight by word count)
    total_words = sum(r["chunk_word_count"] for r in chunk_results)
    if total_words > 0:
        weighted_f_conv = sum(
            r["f_conv"] * r["chunk_word_count"] / total_words
            for r in chunk_results
        )
    else:
        weighted_f_conv = 0.0
    
    aggregate = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "f_conv_aggregate": round(weighted_f_conv, 6),
        "f_conv_min_chunk": round(min(r["f_conv"] for r in chunk_results), 6),
        "f_conv_max_chunk": round(max(r["f_conv"] for r in chunk_results), 6),
        "num_chunks": len(chunks),
        "total_words": total_words,
        "output_type": output_type.value,
        "source_path": source_path,
        "chunk_scores": [round(r["f_conv"], 4) for r in chunk_results],
        "is_aggregate": True,
    }
    if metadata:
        aggregate["metadata"] = metadata
    
    _log_universal(aggregate)
    
    return aggregate


def score_file(
    filepath: str,
    output_type: Optional[OutputType] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Score a file's content. Auto-detects output_type from path if not provided.
    """
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}
    
    content = path.read_text()
    
    # Auto-detect output type from path
    if output_type is None:
        output_type = _detect_output_type(str(path))
    
    return score_output(
        content=content,
        output_type=output_type,
        source_path=str(path),
        metadata=metadata
    )


def score_commit_message(message: str, commit_hash: str = "") -> Dict[str, Any]:
    """Score a git commit message."""
    return score_output(
        content=message,
        output_type=OutputType.COMMIT_MESSAGE,
        metadata={"commit_hash": commit_hash}
    )


def _detect_output_type(filepath: str) -> OutputType:
    """Infer output type from file path."""
    fp = filepath.lower()
    if "diary" in fp:
        return OutputType.DIARY_ENTRY
    elif "pulse" in fp:
        return OutputType.PULSE_LOG
    elif "proposal" in fp:
        return OutputType.PROPOSAL
    elif "research" in fp:
        return OutputType.RESEARCH_NOTE
    elif "governance_moment" in fp or "governance-moment" in fp:
        return OutputType.GOVERNANCE_MOMENT
    elif "memory" in fp:
        return OutputType.MEMORY_ENTRY
    elif "readme" in fp:
        return OutputType.README
    elif "datasheet" in fp:
        return OutputType.DATASHEET
    elif "constraint" in fp:
        return OutputType.CONSTRAINT_DOC
    else:
        return OutputType.FILE_CONTENT


def _log_universal(record: Dict[str, Any]):
    """Append to universal scoring log."""
    UNIVERSAL_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(UNIVERSAL_LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")


def get_universal_summary() -> Dict[str, Any]:
    """Summary statistics across all output types."""
    import numpy as np
    
    if not UNIVERSAL_LOG_PATH.exists():
        return {"records": 0}
    
    records = []
    with open(UNIVERSAL_LOG_PATH) as f:
        for line in f:
            try:
                records.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    
    if not records:
        return {"records": 0}
    
    # Group by output type
    by_type = {}
    for r in records:
        otype = r.get("output_type", "unknown")
        if otype not in by_type:
            by_type[otype] = []
        
        score = r.get("f_conv", r.get("f_conv_aggregate"))
        if score is not None:
            by_type[otype].append(score)
    
    summary = {
        "total_records": len(records),
        "by_type": {}
    }
    
    all_scores = []
    for otype, scores in by_type.items():
        if scores:
            all_scores.extend(scores)
            summary["by_type"][otype] = {
                "count": len(scores),
                "mean": round(float(np.mean(scores)), 4),
                "std": round(float(np.std(scores)), 4),
                "min": round(float(min(scores)), 4),
                "max": round(float(max(scores)), 4),
            }
    
    if all_scores:
        summary["overall_mean"] = round(float(np.mean(all_scores)), 4)
        summary["overall_std"] = round(float(np.std(all_scores)), 4)
    
    return summary
