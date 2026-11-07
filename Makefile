SHELL := /bin/bash
.DEFAULT_GOAL := help

-include .env

API_PORT ?= 8000
WEB_PORT ?= 3000

export API_PORT WEB_PORT

.PHONY: help install dev dev-backend dev-frontend test test-backend test-frontend \
	lint lint-backend lint-frontend typecheck typecheck-backend typecheck-frontend

help:
	@echo "fair2fly development commands"
	@echo "  make install     Install backend and frontend dependencies"
	@echo "  make dev         Run the API and web app in development mode"
	@echo "  make test        Run backend and frontend tests"
	@echo "  make lint        Run lint and format checks"
	@echo "  make typecheck   Run Python and TypeScript type checks"

install:
	cd backend && uv sync --frozen --all-groups
	cd frontend && npm ci

dev:
	@./scripts/check-port.sh "$(API_PORT)" "API" "API_PORT"
	@./scripts/check-port.sh "$(WEB_PORT)" "web" "WEB_PORT"
	@$(MAKE) --no-print-directory -j2 dev-backend dev-frontend

dev-backend:
	@./scripts/check-port.sh "$(API_PORT)" "API" "API_PORT"
	cd backend && uv run --frozen uvicorn app.main:app --host 0.0.0.0 --port "$(API_PORT)" --reload

dev-frontend:
	@./scripts/check-port.sh "$(WEB_PORT)" "web" "WEB_PORT"
	cd frontend && npm run dev -- --port "$(WEB_PORT)"

test: test-backend test-frontend

test-backend:
	cd backend && uv run --frozen pytest

test-frontend:
	cd frontend && npm run test

lint: lint-backend lint-frontend

lint-backend:
	cd backend && uv run --frozen ruff check .
	cd backend && uv run --frozen ruff format --check .

lint-frontend:
	cd frontend && npm run lint

typecheck: typecheck-backend typecheck-frontend

typecheck-backend:
	cd backend && uv run --frozen mypy .

typecheck-frontend:
	cd frontend && npm run typecheck
