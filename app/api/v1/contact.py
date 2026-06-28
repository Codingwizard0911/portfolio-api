import hashlib
from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.models.contact import ContactSubmission

router = APIRouter(tags=["contact"])


class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str | None = None
    message: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name is required")
        if len(v) > 200:
            raise ValueError("Name too long")
        return v

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message is required")
        if len(v) > 5000:
            raise ValueError("Message too long")
        return v


class ContactResponse(BaseModel):
    success: bool
    message: str


@router.post("/contact", response_model=ContactResponse)
async def submit_contact(
    body: ContactRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> ContactResponse:
    client_ip = request.headers.get("X-Forwarded-For", request.client.host if request.client else "")
    ip_hash = hashlib.sha256(client_ip.encode()).hexdigest()[:16] if client_ip else None

    submission = ContactSubmission(
        name=body.name,
        email=str(body.email),
        subject=body.subject,
        message=body.message,
        ip_hash=ip_hash,
    )
    db.add(submission)
    await db.flush()

    return ContactResponse(success=True, message="Message received. I'll respond within 24 hours.")
