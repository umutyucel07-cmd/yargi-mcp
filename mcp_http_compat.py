"""Compatibility helpers for MCP HTTP deployments."""

from __future__ import annotations


class MCPHeaderCompatibilityMiddleware:
    """Map legacy session headers to the standard MCP session header."""

    STANDARD_HEADER = b"mcp-session-id"
    LEGACY_HEADERS = {b"x-session-id", b"session-id"}

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope.get("type") == "http":
            headers = list(scope.get("headers", []))
            has_standard_header = any(key.lower() == self.STANDARD_HEADER for key, _ in headers)

            if not has_standard_header:
                legacy_value = next(
                    (
                        value
                        for key, value in headers
                        if key.lower() in self.LEGACY_HEADERS and value
                    ),
                    None,
                )
                if legacy_value is not None:
                    scope = dict(scope)
                    scope["headers"] = headers + [(self.STANDARD_HEADER, legacy_value)]

        await self.app(scope, receive, send)
