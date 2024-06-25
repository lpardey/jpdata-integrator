from fastapi import APIRouter

router = APIRouter(prefix="/healthcheck", tags=["Healthcheck"])


@router.get("")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
