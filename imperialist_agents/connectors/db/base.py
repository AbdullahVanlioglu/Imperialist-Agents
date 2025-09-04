from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Iterable, List, Tuple


class Database(ABC):
    """Abstract base class for database connectors."""

    @abstractmethod
    def execute(self, sql: str, params: Iterable[Any] | None = None) -> List[Tuple[Any, ...]]:
        """
        Execute a SQL statement with optional parameters.

        Args:
        sql: The SQL string to execute.
        params: Optional parameters for parameterized queries.

        Returns:
        A list of tuples representing query results (empty list for non-SELECT statements).
        """
        raise NotImplementedError