"""Application configuration using Pydantic BaseSettings."""
# ruff: noqa: I001 - Imports structured for Jinja2 template conditionals

from pathlib import Path
from typing import Literal

from pydantic import computed_field, field_validator, model_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


def find_env_file() -> Path | None:
    """Find .env file in current or parent directories."""
    current = Path.cwd()
    for path in [current, current.parent]:
        env_file = path / ".env"
        if env_file.exists():
            return env_file
    return None


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=find_env_file(),
        env_ignore_empty=True,
        extra="ignore",
    )

    # === Project ===
    PROJECT_NAME: str = "proj2"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: Literal["development", "local", "staging", "production"] = "local"
    TIMEZONE: str = "UTC"  # IANA timezone (e.g. "UTC", "Europe/Warsaw", "America/New_York")
    MODELS_CACHE_DIR: Path = Path("./models_cache")
    MEDIA_DIR: Path = Path("./media")
    MAX_UPLOAD_SIZE_MB: int = 50  # Max file upload size in MB
    # Soft per-org storage cap surfaced on /billing — not enforced yet (5 GB).
    STORAGE_SOFT_LIMIT_BYTES: int = 5 * 1024 * 1024 * 1024

    # === Logfire ===
    LOGFIRE_TOKEN: str | None = None
    LOGFIRE_SERVICE_NAME: str = "proj2"
    LOGFIRE_ENVIRONMENT: str = "development"

    # === Database (PostgreSQL async) ===
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "proj2"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URL(self) -> str:
        """Build async PostgreSQL connection URL."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Build sync PostgreSQL connection URL (for Alembic)."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Pool configuration
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    # === Auth (SECRET_KEY for JWT/Session/Admin) ===
    SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info: ValidationInfo) -> str:
        """Validate SECRET_KEY is secure in production."""
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        # Get environment from values if available
        env = info.data.get("ENVIRONMENT", "local") if info.data else "local"
        if v == "change-me-in-production-use-openssl-rand-hex-32" and env == "production":
            raise ValueError(
                "SECRET_KEY must be changed in production! "
                "Generate a secure key with: openssl rand -hex 32"
            )
        return v

    # === JWT Settings ===
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"

    # Public URL of the frontend; used to build OAuth redirect targets and
    # Stripe checkout/portal return URLs. Always declared (not gated) because
    # the billing model_validator references it unconditionally.
    FRONTEND_URL: str = "http://localhost:3000"

    # === OAuth2 (Google) ===
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/oauth/google/callback"

    # === Auth (API Key) ===
    API_KEY: str = "change-me-in-production"
    API_KEY_HEADER: str = "X-API-Key"

    @field_validator("API_KEY")
    @classmethod
    def validate_api_key(cls, v: str, info: ValidationInfo) -> str:
        """Validate API_KEY is set in production."""
        env = info.data.get("ENVIRONMENT", "local") if info.data else "local"
        if v == "change-me-in-production" and env == "production":
            raise ValueError(
                "API_KEY must be changed in production! "
                "Generate a secure key with: openssl rand -hex 32"
            )
        return v

    # === Redis ===
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int = 0

    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_URL(self) -> str:
        """Build Redis connection URL."""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # === Rate Limiting ===
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds

    # === Taskiq ===
    TASKIQ_BROKER_URL: str = "redis://localhost:6379/1"
    TASKIQ_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # === Sentry ===
    SENTRY_DSN: str | None = None

    # === Prometheus ===
    PROMETHEUS_METRICS_PATH: str = "/metrics"
    PROMETHEUS_INCLUDE_IN_SCHEMA: bool = False
    # When set, /metrics requires `Authorization: Bearer <token>`. Leave empty
    # to expose unauthenticated (recommended only behind a private network or
    # a reverse-proxy-level allow-list — Prometheus scrapes internally).
    PROMETHEUS_AUTH_TOKEN: str = ""

    # === File Storage (S3/MinIO) ===
    S3_ENDPOINT: str | None = None
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_BUCKET: str = "proj2"
    S3_REGION: str = "us-east-1"

    # === AI Agent (pydantic_ai, google) ===
    GOOGLE_API_KEY: str = ""
    AI_MODEL: str = "gemini-2.5-flash"
    AI_TEMPERATURE: float = 0.7
    AI_THINKING_ENABLED: bool = False
    AI_THINKING_EFFORT: str = "medium"  # "low", "medium", "high"
    AI_AVAILABLE_MODELS: list[str] = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
    ]
    AI_FRAMEWORK: str = "pydantic_ai"
    LLM_PROVIDER: str = "google"

    # === Stripe Billing ===
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_API_VERSION: str = "2025-04-30.acacia"
    STRIPE_TRIAL_DAYS_DEFAULT: int = 14
    STRIPE_TRIAL_REQUIRES_PAYMENT_METHOD: bool = False

    BILLING_DEFAULT_CURRENCY: str = "usd"
    BILLING_SUCCESS_URL: str = ""
    BILLING_CANCEL_URL: str = ""
    BILLING_PORTAL_RETURN_URL: str = ""

    @model_validator(mode="after")
    def _set_billing_urls(self) -> "Settings":
        frontend = self.FRONTEND_URL.rstrip("/")
        if not self.BILLING_SUCCESS_URL:
            self.BILLING_SUCCESS_URL = (
                frontend + "/billing?status=success&session_id={CHECKOUT_SESSION_ID}"
            )
        if not self.BILLING_CANCEL_URL:
            self.BILLING_CANCEL_URL = frontend + "/pricing?status=canceled"
        if not self.BILLING_PORTAL_RETURN_URL:
            self.BILLING_PORTAL_RETURN_URL = frontend + "/billing"
        return self

    CREDITS_PER_USD: int = 1000
    CREDITS_LOW_THRESHOLD: int = 100
    CREDITS_FREE_TIER_GRANT: int = 500

    # === Email ===
    EMAIL_PROVIDER: str = "resend"
    EMAIL_FROM: str = "noreply@proj2.com"
    EMAIL_FROM_NAME: str = "proj2"
    EMAIL_REPLY_TO: str | None = None
    RESEND_API_KEY: str = ""
    LOG_PROVIDER_WRITE_TO_DISK: bool = False

    # === CORS ===
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    @field_validator("CORS_ORIGINS")
    @classmethod
    def validate_cors_origins(cls, v: list[str], info: ValidationInfo) -> list[str]:
        """Warn if CORS_ORIGINS is too permissive in production."""
        env = info.data.get("ENVIRONMENT", "local") if info.data else "local"
        if "*" in v and env == "production":
            raise ValueError(
                "CORS_ORIGINS cannot contain '*' in production! Specify explicit allowed origins."
            )
        return v


settings = Settings()
