"""Demo MCP server implemented with the Python FastMCP helper.

This server implements a simple demo widget with increment, decrement, and
reset tools. The tools return structured content with the current count that
gets rendered in a widget UI."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

import mcp.types as types
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import BaseModel, ConfigDict, Field, ValidationError


# Demo state management
demo_value: int = 0


@dataclass(frozen=True)
class WidgetConfig:
    template_uri: str
    html: str


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


@lru_cache(maxsize=None)
def _load_widget_html(component_name: str) -> str:
    html_path = ASSETS_DIR / f"{component_name}.html"
    if html_path.exists():
        return html_path.read_text(encoding="utf8")

    fallback_candidates = sorted(ASSETS_DIR.glob(f"{component_name}-*.html"))
    if fallback_candidates:
        return fallback_candidates[-1].read_text(encoding="utf8")

    raise FileNotFoundError(
        f'Widget HTML for "{component_name}" not found in {ASSETS_DIR}. '
        "Run `pnpm run build` to generate the assets before starting the server."
    )


# Widget configuration
DEMO_WIDGET = WidgetConfig(
    template_uri="ui://widget/demo.html",
    html=_load_widget_html("demo"),
)


MIME_TYPE = "text/html+skybridge"


class IncrementInput(BaseModel):
    """Schema for increment tool."""

    amount: int = Field(
        default=1,
        description="The amount to increment by (default: 1)",
    )

    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class DecrementInput(BaseModel):
    """Schema for decrement tool."""

    amount: int = Field(
        default=1,
        description="The amount to decrement by (default: 1)",
    )

    model_config = ConfigDict(populate_by_name=True, extra="forbid")


mcp = FastMCP(
    name="demo-app",
    stateless_http=True,
    transport_security=TransportSecuritySettings(
        allowed_hosts=["openai-apps-demo-7lsyxpfena-uw.a.run.app", "unrestricted-nuptially-gage.ngrok-free.dev", "localhost", "127.0.0.1"],
    ),
)


INCREMENT_INPUT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "amount": {
            "type": "integer",
            "default": 1,
            "description": "The amount to increment by (default: 1)",
        }
    },
    "additionalProperties": False,
}

DECREMENT_INPUT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "amount": {
            "type": "integer",
            "default": 1,
            "description": "The amount to decrement by (default: 1)",
        }
    },
    "additionalProperties": False,
}


def _tool_meta(tool_name: str) -> Dict[str, Any]:
    """Generate metadata for tools."""
    if tool_name == "increment":
        return {
            "openai/outputTemplate": DEMO_WIDGET.template_uri,
            "openai/toolInvocation/invoking": "Incrementing demo",
            "openai/toolInvocation/invoked": "Incremented demo",
        }
    elif tool_name == "decrement":
        return {
            "openai/outputTemplate": DEMO_WIDGET.template_uri,
            "openai/toolInvocation/invoking": "Decrementing demo",
            "openai/toolInvocation/invoked": "Decremented demo",
        }
    elif tool_name == "reset":
        return {
            "openai/outputTemplate": DEMO_WIDGET.template_uri,
            "openai/toolInvocation/invoking": "Resetting demo",
            "openai/toolInvocation/invoked": "Reset demo",
            "openai/widgetAccessible": True,
        }
    return {}


def _embedded_widget_resource() -> types.EmbeddedResource:
    """Create embedded widget resource for demo widget."""
    return types.EmbeddedResource(
        type="resource",
        resource=types.TextResourceContents(
            uri=DEMO_WIDGET.template_uri,
            mimeType=MIME_TYPE,
            text=DEMO_WIDGET.html,
        ),
    )


@mcp._mcp_server.list_tools()
async def _list_tools() -> List[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="increment",
            title="Increment demo",
            description="Increments the demo by a specified amount (default: 1).",
            inputSchema=deepcopy(INCREMENT_INPUT_SCHEMA),
            _meta=_tool_meta("increment"),
        ),
        types.Tool(
            name="decrement",
            title="Decrement demo",
            description="Decrements the demo by a specified amount (default: 1).",
            inputSchema=deepcopy(DECREMENT_INPUT_SCHEMA),
            _meta=_tool_meta("decrement"),
        ),
        types.Tool(
            name="reset",
            title="Reset demo",
            description="Resets the demo to zero.",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
            _meta=_tool_meta("reset"),
        ),
    ]


@mcp._mcp_server.list_resources()
async def _list_resources() -> List[types.Resource]:
    """List available resources."""
    return [
        types.Resource(
            name="demo-widget",
            title="Demo Widget",
            uri=DEMO_WIDGET.template_uri,
            description="Demo widget markup",
            mimeType=MIME_TYPE,
            _meta={"openai/widgetPrefersBorder": True},
        )
    ]


async def _handle_read_resource(req: types.ReadResourceRequest) -> types.ServerResult:
    """Handle resource read requests."""
    if str(req.params.uri) != DEMO_WIDGET.template_uri:
        return types.ServerResult(
            types.ReadResourceResult(
                contents=[],
                _meta={"error": f"Unknown resource: {req.params.uri}"},
            )
        )

    contents = [
        types.TextResourceContents(
            uri=DEMO_WIDGET.template_uri,
            mimeType=MIME_TYPE,
            text=DEMO_WIDGET.html,
            _meta={"openai/widgetPrefersBorder": True},
        )
    ]

    return types.ServerResult(types.ReadResourceResult(contents=contents))


def _reply_with_demo(message: str = "") -> types.CallToolResult:
    """Helper to create a tool result with current demo value."""
    global demo_value

    content = []
    if message:
        content.append(types.TextContent(type="text", text=message))

    widget_resource = _embedded_widget_resource()
    meta: Dict[str, Any] = {
        "openai/widget": widget_resource.model_dump(mode="json"),
        "openai/outputTemplate": DEMO_WIDGET.template_uri,
        "openai/widgetAccessible": True,
        "openai/resultCanProduceWidget": True,
        "customMessage": f"Demo value is currently {demo_value}",
        "timestamp": "2025-12-28",
    }

    return types.CallToolResult(
        content=content,
        structuredContent={"count": demo_value},
        _meta=meta,
    )


async def _call_tool_request(req: types.CallToolRequest) -> types.ServerResult:
    """Handle tool call requests."""
    global demo_value

    tool_name = req.params.name
    arguments = req.params.arguments or {}

    if tool_name == "increment":
        try:
            payload = IncrementInput.model_validate(arguments)
        except ValidationError as exc:
            return types.ServerResult(
                types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=f"Input validation error: {exc.errors()}",
                        )
                    ],
                    isError=True,
                )
            )

        amount = payload.amount
        demo_value += amount

        return types.ServerResult(
            _reply_with_demo(f"Demo incremented by {amount}. Current value: {demo_value}")
        )

    elif tool_name == "decrement":
        try:
            payload = DecrementInput.model_validate(arguments)
        except ValidationError as exc:
            return types.ServerResult(
                types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=f"Input validation error: {exc.errors()}",
                        )
                    ],
                    isError=True,
                )
            )

        amount = payload.amount
        demo_value -= amount

        return types.ServerResult(
            _reply_with_demo(f"Demo decremented by {amount}. Current value: {demo_value}")
        )

    elif tool_name == "reset":
        demo_value = 0

        return types.ServerResult(
            _reply_with_demo("Demo has been reset to 0.")
        )

    else:
        return types.ServerResult(
            types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Unknown tool: {tool_name}",
                    )
                ],
                isError=True,
            )
        )


mcp._mcp_server.request_handlers[types.CallToolRequest] = _call_tool_request
mcp._mcp_server.request_handlers[types.ReadResourceRequest] = _handle_read_resource


app = mcp.streamable_http_app()

# Configure allowed hosts for ngrok and local development
from starlette.middleware.trustedhost import TrustedHostMiddleware

# Remove any default TrustedHostMiddleware that might be blocking ngrok
app.user_middleware = [m for m in app.user_middleware if m[0] != TrustedHostMiddleware]

# Add TrustedHostMiddleware with wildcard to allow all hosts (including ngrok)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

try:
    from starlette.middleware.cors import CORSMiddleware
    from starlette.routing import Route
    from starlette.responses import PlainTextResponse, FileResponse
    from pathlib import Path

    # Add a simple home route
    async def home(request):
        """Simple home route to verify server is running."""
        return PlainTextResponse("Demo MCP server")

    # Serve static assets from the assets directory
    assets_path = Path(__file__).resolve().parent.parent / "assets"

    # Serve individual asset files from root for widget loading
    async def serve_js(request):
        """Serve JS asset files."""
        filename = request.path_params.get("filename")
        file_path = assets_path / f"{filename}.js"
        if file_path.exists() and file_path.is_file():
            response = FileResponse(file_path, media_type="application/javascript")
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            return response
        return PlainTextResponse("Not found", status_code=404)

    async def serve_css(request):
        """Serve CSS asset files."""
        filename = request.path_params.get("filename")
        file_path = assets_path / f"{filename}.css"
        if file_path.exists() and file_path.is_file():
            response = FileResponse(file_path, media_type="text/css")
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            return response
        return PlainTextResponse("Not found", status_code=404)

    # Handle OPTIONS preflight requests
    async def handle_options(request):
        """Handle CORS preflight requests."""
        response = PlainTextResponse("", status_code=200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS, HEAD"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Max-Age"] = "86400"
        return response

    # Add the routes to the app
    app.routes.insert(0, Route("/", home))
    app.routes.insert(1, Route("/{filename}.js", serve_js, methods=["GET", "HEAD"]))
    app.routes.insert(2, Route("/{filename}.css", serve_css, methods=["GET", "HEAD"]))
    app.routes.insert(3, Route("/{filename}.js", handle_options, methods=["OPTIONS"]))
    app.routes.insert(4, Route("/{filename}.css", handle_options, methods=["OPTIONS"]))

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST", "OPTIONS", "HEAD"],
        allow_headers=["*"],
        allow_credentials=False,
        expose_headers=["*"],
    )
except Exception:
    pass


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    print(f"Demo MCP server listening on http://localhost:{port}/mcp")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        forwarded_allow_ips="*",
        proxy_headers=True,
    )
