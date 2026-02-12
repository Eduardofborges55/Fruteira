import sentry_sdk

sentry_sdk.init(
    dsn="SUA_DSN_DO_SENTRY_AQUI",
    traces_sample_rate=1.0,
)
