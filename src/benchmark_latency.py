"""
Benchmark latency utilities.

Cung cấp context manager để tạm thời override environment variables
trong quá trình chạy evaluation A/B configs.
"""

import contextlib
import os
from typing import Generator


@contextlib.contextmanager
def temporary_env(env: dict) -> Generator[None, None, None]:
    """
    Context manager tạm thời set environment variables, khôi phục sau khi xong.

    Args:
        env: Dict {key: value} cần set tạm thời.

    Example:
        with temporary_env({"HYDE_ENABLED": "1", "RERANK_METHOD": "cross_encoder"}):
            result = retrieve(query)
    """
    old_values: dict[str, str | None] = {}
    for key, value in env.items():
        old_values[key] = os.environ.get(key)
        os.environ[key] = str(value)
    try:
        yield
    finally:
        for key, old_value in old_values.items():
            if old_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old_value
