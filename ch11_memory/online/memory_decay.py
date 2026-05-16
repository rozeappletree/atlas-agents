"""
memory_decay.py — Time-weighted salience scoring for agent memory.

The problem: an agent's memory store grows without bound. After six months,
it's full of facts that were relevant once but will never surface again.
Naive retrieval treats a memory from yesterday the same as one from last year.

This module implements salience scoring that decays stale memories and
amplifies frequently-recalled ones. Run it to see the effect:

    python memory_decay.py

You'll see that a memory accessed yesterday scores dramatically higher than
an identical one stored six months ago, even with the same semantic similarity.
"""

import datetime
import math
from dataclasses import dataclass, field


@dataclass
class MemoryRecord:
    text: str
    semantic_similarity: float      # Cosine score from vector search (0.0–1.0)
    stored_at: datetime.datetime
    last_accessed: datetime.datetime
    access_count: int = 1


def salience(memory: MemoryRecord, now: datetime.datetime | None = None) -> float:
    """
    Score a memory by combining semantic similarity with temporal relevance.

    Decay is exponential: a memory loses ~50% of its time-weight every 30 days.
    Frequent recall slows that decay — each access adds a small bonus (capped
    at 10 accesses to prevent runaway boosting).
    """
    if now is None:
        now = datetime.datetime.now()

    days_since_access = max(0, (now - memory.last_accessed).days)

    # Half-life of 30 days: score = base * 0.5^(days/30)
    decay = math.pow(0.5, days_since_access / 30)

    # Frequency bonus: +5% per access, capped at +50%
    frequency_boost = 1.0 + min(memory.access_count, 10) * 0.05

    return memory.semantic_similarity * decay * frequency_boost


def should_prune(memory: MemoryRecord, threshold: float = 0.05) -> bool:
    """Return True if a memory's salience has dropped below the threshold."""
    return salience(memory) < threshold


# ── Demo ────────────────────────────────────────────────────────────────

def main():
    now = datetime.datetime.now()

    memories = [
        MemoryRecord(
            text="User prefers concise answers",
            semantic_similarity=0.85,
            stored_at=now - datetime.timedelta(days=180),
            last_accessed=now - datetime.timedelta(days=180),
            access_count=1,
        ),
        MemoryRecord(
            text="User prefers concise answers (recalled regularly)",
            semantic_similarity=0.85,
            stored_at=now - datetime.timedelta(days=180),
            last_accessed=now - datetime.timedelta(days=1),
            access_count=12,
        ),
        MemoryRecord(
            text="User is writing a book about AI agents",
            semantic_similarity=0.90,
            stored_at=now - datetime.timedelta(days=30),
            last_accessed=now - datetime.timedelta(days=3),
            access_count=5,
        ),
        MemoryRecord(
            text="User asked about the weather in Rome",
            semantic_similarity=0.60,
            stored_at=now - datetime.timedelta(days=90),
            last_accessed=now - datetime.timedelta(days=90),
            access_count=1,
        ),
        MemoryRecord(
            text="User's preferred stack: Python + FastAPI + Postgres",
            semantic_similarity=0.80,
            stored_at=now - datetime.timedelta(days=7),
            last_accessed=now - datetime.timedelta(days=2),
            access_count=3,
        ),
    ]

    ranked = sorted(memories, key=lambda m: salience(m, now), reverse=True)

    print(f"{'Score':>6}  {'Prune?':>6}  Memory")
    print("─" * 72)
    for m in ranked:
        score = salience(m, now)
        prune = "yes" if should_prune(m) else "no"
        print(f"{score:>6.3f}  {prune:>6}  {m.text[:60]}")

    prunable = [m for m in memories if should_prune(m)]
    print(f"\n{len(prunable)} of {len(memories)} memories are below the salience threshold and can be pruned.")


if __name__ == "__main__":
    main()
