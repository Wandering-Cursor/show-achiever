from achiever_app.operations.demo.read import latest_demo
from achiever_app.schemas.demo import DemoSchema
from mysite.errors.http_errors import NotFoundError

from .router import demo_router


@demo_router.get(
    "/latest",
)
def get_latest_demo() -> DemoSchema:
    demo = latest_demo()

    if not demo:
        raise NotFoundError()

    return DemoSchema.model_validate(demo)
