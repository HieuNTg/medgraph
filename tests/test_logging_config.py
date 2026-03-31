"""Tests for structured logging configuration."""

from __future__ import annotations

import json
import logging
import os

from medgraph.logging_config import JSONFormatter, configure_logging


class TestJSONFormatter:
    def test_formats_as_json(self) -> None:
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="hello world",
            args=(),
            exc_info=None,
        )
        output = formatter.format(record)
        parsed = json.loads(output)
        assert parsed["level"] == "INFO"
        assert parsed["message"] == "hello world"
        assert parsed["logger"] == "test"
        assert "timestamp" in parsed

    def test_includes_exception(self) -> None:
        formatter = JSONFormatter()
        try:
            raise ValueError("test error")
        except ValueError:
            import sys

            record = logging.LogRecord(
                name="test",
                level=logging.ERROR,
                pathname="",
                lineno=0,
                msg="failed",
                args=(),
                exc_info=sys.exc_info(),
            )
        output = formatter.format(record)
        parsed = json.loads(output)
        assert "exception" in parsed
        assert "ValueError" in parsed["exception"]


class TestConfigureLogging:
    def test_json_format(self) -> None:
        os.environ["MEDGRAPH_LOG_FORMAT"] = "json"
        try:
            configure_logging()
            root = logging.getLogger()
            assert any(isinstance(h.formatter, JSONFormatter) for h in root.handlers)
        finally:
            os.environ.pop("MEDGRAPH_LOG_FORMAT", None)
            configure_logging()  # reset

    def test_text_format_default(self) -> None:
        os.environ.pop("MEDGRAPH_LOG_FORMAT", None)
        configure_logging()
        root = logging.getLogger()
        assert not any(isinstance(h.formatter, JSONFormatter) for h in root.handlers)
