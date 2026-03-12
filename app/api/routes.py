from fastapi import APIRouter

from app.api import auth, dashboard, children, web_auth, attendance, visits, points, reports


api_router = APIRouter()

# API auth routes (JWT)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Web login (cookie-based)
api_router.include_router(web_auth.router, tags=["web-auth"])

# Dashboard & UI routes
api_router.include_router(dashboard.router, tags=["dashboard"])
api_router.include_router(children.router, tags=["children"])
api_router.include_router(attendance.router, tags=["attendance"])
api_router.include_router(visits.router, tags=["visits"])
api_router.include_router(points.router, tags=["points"])
api_router.include_router(reports.router, tags=["reports"])

