from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from src.common.config import get_settings
from src.common.db import table_exists
from src.common.io import ensure_directory, read_json


settings = get_settings()
ensure_directory(settings.reports_dir)
ensure_directory(settings.plots_dir)
app = FastAPI(title="Open Data Analytics Lab")
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).resolve().parent / "static")), name="static")
app.mount("/reports", StaticFiles(directory=str(settings.reports_dir)), name="reports")

REQUEST_COUNT = Counter(
    "app_request_count",
    "Total number of HTTP requests handled by the web service.",
    ["method", "path"],
)


@app.middleware("http")
async def record_request_metrics(request: Request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, path=request.url.path).inc()
    return response


@app.get("/")
def index(request: Request):
    quality_report = read_json(settings.reports_dir / "data_quality_report.json", default={})
    research_report = read_json(settings.reports_dir / "data_research_report.json", default={})
    visualization_manifest = read_json(
        settings.reports_dir / "visualization_manifest.json",
        default={"plots": []},
    )

    plot_paths = [f"/reports/plots/{name}" for name in visualization_manifest.get("plots", [])]
    context = {
        "request": request,
        "database_ready": settings.database_path.exists() and table_exists(settings.database_path),
        "database_path": str(settings.database_path),
        "csv_path": str(settings.csv_path),
        "quality_report": quality_report,
        "research_report": research_report,
        "plots": plot_paths,
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse(
        {
            "status": "ok",
            "database_ready": settings.database_path.exists() and table_exists(settings.database_path),
        }
    )


@app.get("/metrics")
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
