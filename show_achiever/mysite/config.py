from collections.abc import Callable
from importlib import metadata
from pathlib import Path
from typing import Annotated

import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict
from pytz import BaseTzInfo, timezone


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="mysite_",
        validate_default=True,
        extra="ignore",
    )

    # Important settings
    debug: bool = True
    database_connection: pydantic.AnyUrl = pydantic.Field(
        default=pydantic.AnyUrl(
            "postgresql://postgres:postgres@db:5432/postgres",
        ),
    )

    broker_url: pydantic.AnyUrl = pydantic.Field(
        default=pydantic.AnyUrl(
            "amqp://rabbit:local@mysite_broker:5672",
        ),
    )
    cache_connection: pydantic.AnyUrl | None = pydantic.Field(
        validation_alias=pydantic.AliasChoices("REDIS_URL"),
        default=pydantic.AnyUrl(
            "redis://mysite_cache:6379/0",
        ),
    )

    django_secret_key: str = pydantic.Field(
        default="MockSecretKey",
    )

    # Misc
    timezone_name: str = "UTC"

    @property
    def root_path(self: "Settings") -> str:
        """
        Use to prefix all URLs, for example if your microservices are hosted under one domain
        """
        return "/mysite"

    @property
    def title(self: "Settings") -> str:
        """
        Use to set the service name in the OpenAPI documentation
        """
        return __package__.replace("_", " ").title()

    @property
    def service_name(self: "Settings") -> str:
        """
        Service name may be usefull if you are going to make requests from this service to another,
        include it in the User-Agent header
        (this way you'll know which service made the request, and at which version)
        """
        return f"{__package__}/{self.version}"

    @property
    def version(self: "Settings") -> str:
        """
        Some trickery to get the version from the package metadata, or from pyproject.toml
        """
        try:
            return metadata.version(__package__)
        except metadata.PackageNotFoundError:
            pyproject_toml_file = Path(__file__).parent.parent / "pyproject.toml"
            version = "undefined"
            if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
                import toml

                data = toml.load(pyproject_toml_file)
                if "project" in data and "version" in data["project"]:
                    version = data["project"]["version"]
            return version

    @property
    def timezone(self: "Settings") -> BaseTzInfo:
        """
        Returns the timezone object for the current timezone_name
        """
        if getattr(self, "_timezone", None):
            return self._timezone

        self._timezone = timezone(self.timezone_name)
        return self.timezone


def convert_string_to_list(v: str | list) -> Callable[..., list[str]]:
    if not v:
        return []
    if isinstance(v, list):
        return v
    return [item.strip() for item in v.split(",")]


# Assume that the output value is always a list of strings
# but due to technicalities of how Pydantic works, we have to allow it to be a string too.
StringListValidator = Annotated[
    list[str] | str,
    pydantic.BeforeValidator(convert_string_to_list),
]


class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="mysite_security_",
        validate_default=True,
        extra="ignore",
    )

    allow_credentials: bool = True
    allow_methods: StringListValidator = ["*"]
    cors_headers: StringListValidator = ["*"]

    # If you set `cors_allow_origin_regex`, `cors_origins` will be ignored
    cors_origins: StringListValidator = ["*"]
    cors_allow_origin_regex: str | None = ".*localhost:.*|.*your-org.*.github.com"

    csrf_trusted_origins: StringListValidator = ["*"]

    # OpenTelemetry settings
    otel_traces_endpoint: str | None = None
    otel_traces_authorization: str | None = None
    otel_capture_headers_server_request: str = ".*"
    otel_capture_headers_server_response: str = "Content.*,X-.*"
    otel_capture_headers_sanitize_fields: str = "Authorization,.*session.*,set-cookie"


settings = Settings()  # type: ignore[call-arg]
security_settings = SecuritySettings()  # type: ignore[call-arg]
