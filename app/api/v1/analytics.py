import hashlib
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.analytics import PageView, ResumeDownload

router = APIRouter(tags=["analytics"])


class PageViewRequest(BaseModel):
    page: str
    referrer: str | None = None


@router.post("/analytics/pageview", status_code=202)
async def record_page_view(
    body: PageViewRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    ua = request.headers.get("User-Agent", "")
    ua_hash = hashlib.sha256(ua.encode()).hexdigest()[:16] if ua else None

    view = PageView(
        page=body.page[:500],
        referrer=body.referrer[:1000] if body.referrer else None,
        user_agent_hash=ua_hash,
    )
    db.add(view)
    await db.flush()
    return {"accepted": True}


@router.post("/analytics/resume-download", status_code=202)
async def record_resume_download(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    referrer = request.headers.get("Referer")
    download = ResumeDownload(referrer=referrer[:1000] if referrer else None)
    db.add(download)
    await db.flush()
    return {"accepted": True}
