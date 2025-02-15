from fastapi.responses import RedirectResponse
from mysite.config import settings

from .router import achiever_app_router


@achiever_app_router.get(
    "/",
    include_in_schema=False,
)
def index() -> RedirectResponse:
    if settings.debug:
        return RedirectResponse(
            url=settings.root_path + "/docs",
        )
    return None
