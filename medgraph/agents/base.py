"""
Base class for MEDGRAPH background agents.

All agents follow the same lifecycle:
    1. Initialize with GraphStore reference
    2. run() — execute the agent's enrichment task
    3. Return AgentResult with stats and any errors
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    """Result of an agent run, including stats and errors."""

    agent_name: str
    records_processed: int = 0
    records_updated: int = 0
    records_skipped: int = 0
    errors: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0

    @property
    def success(self) -> bool:
        return len(self.errors) == 0

    def summary(self) -> str:
        status = "OK" if self.success else f"ERRORS({len(self.errors)})"
        return (
            f"[{self.agent_name}] {status} — "
            f"processed={self.records_processed}, "
            f"updated={self.records_updated}, "
            f"skipped={self.records_skipped}, "
            f"time={self.duration_seconds:.1f}s"
        )


class BaseAgent(ABC):
    """
    Abstract base for all MEDGRAPH enrichment agents.

    Subclasses implement _execute() with their specific logic.
    The run() method wraps execution with timing and error handling.
    """

    def __init__(self, store: GraphStore, name: Optional[str] = None) -> None:
        self.store = store
        self.name = name or self.__class__.__name__

    def run(self) -> AgentResult:
        """Execute the agent with timing and error handling."""
        result = AgentResult(agent_name=self.name)
        start = time.monotonic()
        try:
            self._execute(result)
        except Exception as e:
            logger.error(f"[{self.name}] Fatal error: {e}")
            result.errors.append(str(e))
        result.duration_seconds = time.monotonic() - start
        logger.info(result.summary())
        return result

    @abstractmethod
    def _execute(self, result: AgentResult) -> None:
        """Implement agent-specific enrichment logic. Mutate result in place."""
        ...
