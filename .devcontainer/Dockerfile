# Dockerfile for Devcontainer
# https://hub.docker.com/r/microsoft/devcontainers-python/
FROM mcr.microsoft.com/devcontainers/python:3

USER vscode

# Adds UV Package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --chown=vscode:vscode . /workspace
