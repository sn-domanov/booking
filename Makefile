COMPOSE = docker compose

BASE_COMPOSE = -f docker/compose.yml

DEV_COMPOSE = -f docker/compose.dev.yml

.PHONY: \
	dev-up \
	dev-up-build \
	dev-down \
	dev-down-volumes \
	dev-api-bash \
	dev-api-logs


# ─────────────────────────────────────────
# Dev
# ─────────────────────────────────────────

dev-up:
	$(COMPOSE) ${BASE_COMPOSE} $(DEV_COMPOSE) up -d

dev-up-build:
	$(COMPOSE) ${BASE_COMPOSE} $(DEV_COMPOSE) up --build -d

dev-down:
	$(COMPOSE) ${BASE_COMPOSE} $(DEV_COMPOSE) down

dev-down-v:
	$(COMPOSE) ${BASE_COMPOSE} $(DEV_COMPOSE) down -v

dev-api-bash:
	$(COMPOSE) ${BASE_COMPOSE} $(DEV_COMPOSE) exec -it -u "1000:1000" api bash

dev-api-logs:
	$(COMPOSE) ${BASE_COMPOSE} $(DEV_COMPOSE) logs -f api
