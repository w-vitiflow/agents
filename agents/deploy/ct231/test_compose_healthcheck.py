#!/usr/bin/env python3
"""Verify shipped ERP compose healthcheck uses a quoted grep pattern."""
from pathlib import Path

COMPOSE = Path(__file__).with_name("docker-compose.hermes.yml")


def test_hermes_healthcheck_uses_quoted_grep_pattern():
    text = COMPOSE.read_text()
    assert "healthcheck:" in text
    assert "grep -Fq 'Gateway is running'" in text
    assert "grep -q Gateway is running" not in text