from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import availability, bookings, resume, auth, users
from app.services.booking_service import BookingError

app = FastAPI(title="PrepPilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router, prefix="/api/resume", tags=["resume"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(availability.router, prefix="/api/availability", tags=["availability"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["bookings"])


@app.exception_handler(BookingError)
async def booking_error_handler(_: Request, exc: BookingError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"data": None, "error": {"message": exc.message}},
    )


@app.exception_handler(HTTPException)
async def http_error_handler(_: Request, exc: HTTPException):
    message = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return JSONResponse(
        status_code=exc.status_code,
        content={"data": None, "error": {"message": message}},
        headers=exc.headers,
    )

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
