from app.core.bootstrap import bootstrap
from fastapi import FastAPI

from app.core.db.base import Base
from app.core.db.session import engine
import app.orm  # noqa: F401  # ensure all models are imported

delivery_app = FastAPI(title="Food Delivery API")

bootstrap(delivery_app)

@delivery_app.on_event("startup")
def on_startup() -> None:
    # Base.metadata.create_all(bind=engine)
    pass


@delivery_app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
