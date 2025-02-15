from achiever_app.schemas.healthz import HealthSchema

from .router import achiever_app_internal_router


@achiever_app_internal_router.get("/healthz")
def health_check() -> HealthSchema:
    return HealthSchema()
