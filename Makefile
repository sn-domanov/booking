COMPOSE = docker compose

DEV_STACK   = -f docker/compose/dev.yml

.PHONY: dev-up dev-up-build dev-down dev-down-v dev-api-bash

# ─────────────────────────────────────────
# Dev
# ─────────────────────────────────────────

dev-up:
	$(COMPOSE) $(DEV_STACK) up -d

dev-up-build:
	$(COMPOSE) $(DEV_STACK) up --build -d

dev-down:
	$(COMPOSE) $(DEV_STACK) down

dev-down-v:
	$(COMPOSE) $(DEV_STACK) down -v

dev-api-bash:
	$(COMPOSE) $(DEV_STACK) exec -it -u "1000:1000" api bash
