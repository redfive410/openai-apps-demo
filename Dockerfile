FROM python:3.13-slim

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy application files
COPY . /app
WORKDIR /app

# Environment configuration
ENV PYTHONUNBUFFERED=1

# Install Python dependencies using uv
RUN uv sync

# Expose port 8000
EXPOSE 8000

# Run the MCP server
CMD ["uv", "run", "python", "demo_server/main.py"]
