from achiever_app.models.demo import DemoModel


def latest_demo() -> DemoModel | None:
    try:
        return DemoModel.objects.latest()
    except DemoModel.DoesNotExist as e:
        raise e
        return None
