"""
F_conv Self-Diagnostic Engine
=============================

Computes conversational fidelity (F_conv) for OpenClaw responses.
Post-hoc only (Amendment A6): computed after response delivery.

TKey: TKEY-PS-OC-2026-0308-001
Datasheet: DATASHEET.md
"""

import json
import hashlib
import time
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
import numpy as np

# Paths
LOG_PATH = Path.home() / ".openclaw" / "workspace" / "governed-agent" / "data" / "ps_oc_log.jsonl"
PA_CONFIG_PATH = Path.home() / ".openclaw" / "workspace" / "governed-agent" / "config" / "pa_config.json"

# Embedding model loaded lazily
_model = None
_pa_centroid = None
_pa_config_hash = None
_response_embeddings: List[np.ndarray] = []
_action_embeddings: List[np.ndarray] = []
_energy_history: List[float] = []

# Amendment A2: 14-day non-reported baseline
BASELINE_DAYS = 14
_first_record_timestamp: Optional[float] = None


def _get_model():
    """Lazy-load MiniLM-L6-v2."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _embed(text: str) -> np.ndarray:
    """Embed text using MiniLM-L6-v2. Returns 384-dim vector."""
    model = _get_model()
    return model.encode(text, normalize_embeddings=True)


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors."""
    dot = float(np.dot(a, b))
    norm_a = float(np.linalg.norm(a))
    norm_b = float(np.linalg.norm(b))
    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0
    return dot / (norm_a * norm_b)


def load_pa_config() -> Dict[str, Any]:
    """Load PA configuration and compute centroid."""
    global _pa_centroid, _pa_config_hash
    
    if not PA_CONFIG_PATH.exists():
        raise FileNotFoundError(f"PA config not found at {PA_CONFIG_PATH}")
    
    with open(PA_CONFIG_PATH) as f:
        config = json.load(f)
    
    # Compute PA config hash (Amendment A4)
    config_str = json.dumps(config, sort_keys=True)
    _pa_config_hash = hashlib.sha256(config_str.encode()).hexdigest()[:16]
    
    # Compute PA centroid following primacy_math.py formula:
    # â = (t*p + (1-t)*s) / ||t*p + (1-t)*s||
    purpose_texts = config.get("purpose", [])
    scope_texts = config.get("scope", [])
    constraint_tolerance = config.get("constraint_tolerance", 0.2)
    
    model = _get_model()
    
    # Embed all purpose and scope statements, then average each group
    if purpose_texts:
        purpose_embeddings = model.encode(purpose_texts, normalize_embeddings=True)
        purpose_vector = np.mean(purpose_embeddings, axis=0)
    else:
        purpose_vector = np.zeros(384)
    
    if scope_texts:
        scope_embeddings = model.encode(scope_texts, normalize_embeddings=True)
        scope_vector = np.mean(scope_embeddings, axis=0)
    else:
        scope_vector = np.zeros(384)
    
    # Attractor center formula
    t = constraint_tolerance
    center = t * purpose_vector + (1.0 - t) * scope_vector
    norm = np.linalg.norm(center)
    if norm > 0:
        _pa_centroid = center / norm
    else:
        _pa_centroid = center
    
    return config


def compute_f_conv(response_text: str) -> Dict[str, Any]:
    """
    Compute F_conv for a single response.
    
    POST-HOC ONLY (A6): Call this after the response has been delivered.
    
    Returns dict with all fields specified in DATASHEET.md.
    """
    global _first_record_timestamp
    
    if _pa_centroid is None:
        load_pa_config()
    
    timestamp = time.time()
    iso_timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp))
    
    # Track baseline start
    if _first_record_timestamp is None:
        _first_record_timestamp = timestamp
    
    # Embed response
    response_embedding = _embed(response_text)
    _response_embeddings.append(response_embedding)
    
    # Compute F_conv
    f_conv = _cosine_sim(response_embedding, _pa_centroid)
    
    # Word count and short flag (Amendment A3)
    word_count = len(response_text.split())
    short_flag = word_count < 20
    
    # Lyapunov energy: V(x) = ||x - â||²
    energy = float(np.linalg.norm(response_embedding - _pa_centroid) ** 2)
    _energy_history.append(energy)
    
    # Delta V
    if len(_energy_history) >= 2:
        delta_v = _energy_history[-1] - _energy_history[-2]
    else:
        delta_v = 0.0
    
    # Trajectory stability (fraction of energy-decreasing steps)
    if len(_energy_history) >= 2:
        decreasing = sum(
            1 for i in range(1, len(_energy_history))
            if _energy_history[i] < _energy_history[i-1]
        )
        trajectory_stable = decreasing / (len(_energy_history) - 1) > 0.5
    else:
        trajectory_stable = True
    
    # Compute ρ_wt at three scales
    rho_short = _compute_rho_wt(window=10)
    rho_medium = _compute_rho_wt(window=100)
    rho_long = _compute_rho_wt(window=None)
    
    # Read F_tool from latest telemetry
    f_tool = _read_f_tool()
    
    # Condition zone (from primacy_state.py thresholds)
    # Using F_conv for zone classification
    if f_conv >= 0.76:
        condition = "achieved"
    elif f_conv >= 0.73:
        condition = "weakening"
    elif f_conv >= 0.67:
        condition = "violated"
    else:
        condition = "collapsed"
    
    # Amendment A2: check if in baseline period
    days_elapsed = (timestamp - _first_record_timestamp) / 86400
    in_baseline = days_elapsed < BASELINE_DAYS
    
    record = {
        "timestamp": iso_timestamp,
        "unix_ts": timestamp,
        "f_conv": round(f_conv, 6),
        "f_tool": round(f_tool, 6) if f_tool is not None else None,
        "rho_wt_short": round(rho_short, 6) if rho_short is not None else None,
        "rho_wt_medium": round(rho_medium, 6) if rho_medium is not None else None,
        "rho_wt_long": round(rho_long, 6) if rho_long is not None else None,
        "lyapunov_energy": round(energy, 6),
        "delta_v": round(delta_v, 6),
        "trajectory_stable": trajectory_stable,
        "condition": condition,
        "response_word_count": word_count,
        "short_flag": short_flag,
        "imputed": False,
        "pa_config_hash": _pa_config_hash,
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "embedding_dim": 384,
        "in_baseline": in_baseline,
        "session_id": os.environ.get("OPENCLAW_SESSION_ID", "unknown")
    }
    
    # Log to JSONL
    _log_record(record)
    
    return record


def register_action(action_text: str):
    """
    Register a tool action embedding for ρ_wt computation.
    Call this for each tool call with the action text.
    """
    if _pa_centroid is None:
        load_pa_config()
    action_embedding = _embed(action_text)
    _action_embeddings.append(action_embedding)


def _compute_rho_wt(window: Optional[int] = None) -> Optional[float]:
    """
    Walk-the-talk coherence at specified window size.
    Cosine similarity between centroid of recent response embeddings
    and centroid of recent action embeddings.
    """
    if not _response_embeddings or not _action_embeddings:
        return None
    
    if window is not None:
        resp = _response_embeddings[-window:]
        act = _action_embeddings[-window:]
    else:
        resp = _response_embeddings
        act = _action_embeddings
    
    resp_centroid = np.mean(resp, axis=0)
    act_centroid = np.mean(act, axis=0)
    
    return _cosine_sim(resp_centroid, act_centroid)


def _read_f_tool() -> Optional[float]:
    """Read latest F_tool from TELOS pulse telemetry."""
    try:
        pulse_dir = Path.home() / ".telos" / "pulse"
        memory_line = pulse_dir / "memory_line.txt"
        if memory_line.exists():
            text = memory_line.read_text().strip()
            # Parse "fidelity=X.XXX" from memory line
            for part in text.split("|"):
                part = part.strip()
                if part.startswith("fidelity="):
                    return float(part.split("=")[1])
    except Exception:
        pass
    return None


def _log_record(record: Dict[str, Any]):
    """Append record to JSONL log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")


def get_baseline_status() -> Dict[str, Any]:
    """Check whether baseline period is active."""
    if _first_record_timestamp is None:
        return {"in_baseline": True, "days_elapsed": 0, "days_remaining": BASELINE_DAYS}
    
    days_elapsed = (time.time() - _first_record_timestamp) / 86400
    return {
        "in_baseline": days_elapsed < BASELINE_DAYS,
        "days_elapsed": round(days_elapsed, 1),
        "days_remaining": max(0, round(BASELINE_DAYS - days_elapsed, 1))
    }


def get_summary() -> Dict[str, Any]:
    """Get summary statistics from the log."""
    if not LOG_PATH.exists():
        return {"records": 0}
    
    records = []
    with open(LOG_PATH) as f:
        for line in f:
            try:
                records.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    
    if not records:
        return {"records": 0}
    
    f_convs = [r["f_conv"] for r in records if r.get("f_conv") is not None]
    
    return {
        "records": len(records),
        "f_conv_mean": round(np.mean(f_convs), 4) if f_convs else None,
        "f_conv_median": round(np.median(f_convs), 4) if f_convs else None,
        "f_conv_min": round(min(f_convs), 4) if f_convs else None,
        "f_conv_max": round(max(f_convs), 4) if f_convs else None,
        "f_conv_std": round(np.std(f_convs), 4) if f_convs else None,
        "short_responses": sum(1 for r in records if r.get("short_flag")),
        "baseline_status": get_baseline_status(),
        "latest": records[-1] if records else None
    }
