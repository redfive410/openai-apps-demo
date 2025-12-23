# Demo Widget - OpenAI Apps SDK Demo

A simple demo widget example for use with the OpenAI Apps SDK and MCP (Model Context Protocol).

## What's Included

- **Demo Widget** (`src/demo/`) - A React-based interactive demo widget
- **Python MCP Server** (`demo_server/`) - MCP server that exposes demo tools and serves static assets
- **Build System** (`build-all.mts`) - Vite-based build that produces versioned bundles with inlined CSS/JS
- **Docker Support** - Production-ready containerization with uv package manager

## Quick Start

### Local Development with uv

[uv](https://github.com/astral-sh/uv) is a fast Python package manager written in Rust.

```bash
# 1. Install Node dependencies
pnpm install

# 2. Build the frontend widget
pnpm run build

# 3. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 4. Install Python dependencies and run server
uv sync
uv run python demo_server/main.py
```

The server will start on `http://localhost:8000` and serve both the MCP protocol and static assets.

### Docker (Production-Ready)

```bash
# 1. Install Node dependencies
pnpm install

# 2. Build the frontend widget (required before Docker build!)
pnpm run build

# 3. Build Docker image
docker build -t openai-apps-demo .

# 4. Run the container
docker run -p 8000:8000 openai-apps-demo
```

The server will be available at `http://localhost:8000`.

## Testing in ChatGPT

1. Enable [developer mode](https://platform.openai.com/docs/guides/developer-mode) in ChatGPT
2. Expose your local server using [ngrok](https://ngrok.com/):
   ```bash
   ngrok http 8000
   ```
3. Add the connector in ChatGPT Settings > Connectors using the ngrok URL:
   ```
   https://<your-endpoint>.ngrok-free.app/mcp
   ```
4. Add the app to your conversation using the "More" options
5. Try asking: "Show me the demo" or "Increment the demo by 5"

## Development

### Available Scripts

- `pnpm run build` - Build production bundles with inlined CSS/JS
- `pnpm run serve` - Serve built assets on port 4444 (optional, for testing)
- `pnpm run tsc` - Type check all TypeScript files

### Development Notes

**No Vite Dev Server Needed:** The Python server serves pre-built static files from the `assets/` directory. You only need to run `pnpm run build` when you make frontend changes, then restart the Python server.

**Asset Loading:** The Python server loads widget HTML at startup and caches it in memory using `@lru_cache`. This is extremely fast and requires no separate asset server in production.

**Inlined Assets:** The build process creates self-contained HTML files with CSS and JavaScript inlined. This avoids CORS issues and reduces HTTP requests.

## Repository Structure

```
.
├── src/
│   ├── demo/           # Demo widget source code
│   ├── index.css       # Global styles
│   ├── types.ts        # Shared TypeScript types
│   └── use-*.ts        # Shared React hooks
├── assets/             # Built widget bundles (generated, included in Docker)
├── demo_server/        # Python MCP server
│   ├── main.py         # FastMCP server with static file serving
│   └── requirements.txt # Python dependencies (for pip)
├── build-all.mts       # Build orchestrator (creates inlined HTML)
├── package.json        # Node dependencies and scripts
├── pyproject.toml      # Python project config (for uv)
├── Dockerfile          # Docker image definition
└── .dockerignore       # Files to exclude from Docker image
```

## How It Works

### MCP + Apps SDK

The Model Context Protocol (MCP) connects ChatGPT to your tools and UI:

1. **List tools** - Server advertises available tools with JSON schemas
2. **Call tools** - Model invokes tools with user-provided arguments (increment, decrement, reset)
3. **Return widgets** - Server includes widget metadata in responses (`_meta.openai/outputTemplate`)

The widget is rendered inline in ChatGPT using the built assets.

## Deploying

### Docker Deployment (Recommended)

The easiest way to deploy is using Docker:

```bash
# 1. Build frontend assets
pnpm run build

# 2. Build Docker image (multi-platform if needed)
docker build --platform linux/amd64 -t openai-apps-demo .

# 3. Tag and push to your registry
docker tag openai-apps-demo gcr.io/YOUR_PROJECT/openai-apps-demo
docker push gcr.io/YOUR_PROJECT/openai-apps-demo

# 4. Deploy to Google Cloud Run (example)
gcloud run deploy openai-apps-demo \
  --image gcr.io/YOUR_PROJECT/openai-apps-demo \
  --port 8000 \
  --allow-unauthenticated \
  --region us-central1

# 5. Add your production MCP endpoint to ChatGPT
# https://YOUR_SERVICE_URL/mcp
```

### Alternative: Manual Deployment

If deploying without Docker:

1. Build the widgets:
   ```bash
   pnpm run build
   ```

2. Install dependencies with uv:
   ```bash
   uv sync
   ```

3. Deploy the entire application directory (including `assets/`)

4. Run the server:
   ```bash
   uv run python demo_server/main.py
   ```

5. Add your production MCP endpoint to ChatGPT

**Note:** The Python server serves both the MCP protocol and static assets. You don't need a separate asset server or CDN.

## Customizing

- **Widget UI** - Edit files in `src/demo/`
- **MCP tools** - Modify `demo_server/main.py`
- **Add new widgets** - Create a new directory in `src/` with an `index.tsx` entry point

The build script automatically detects new widgets.

## Available Tools

The MCP server exposes three tools:

- `increment` - Increments the demo by a specified amount (default: 1)
- `decrement` - Decrements the demo by a specified amount (default: 1)
- `reset` - Resets the demo to zero

## License

MIT
