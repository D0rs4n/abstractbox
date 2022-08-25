from datetime import datetime

from fastapi import FastAPI
from models import HealthCheck
from middleware import JWTAuthMiddleware

app = FastAPI()


@app.get("/", response_model=HealthCheck, status_code=200)
async def main() -> dict[str, str]:
    """A basic healthcheck endpoint, to assure the API daemon is up and running."""
    return {"timestamp": datetime.utcnow().isoformat()}

app.add_middleware(JWTAuthMiddleware)