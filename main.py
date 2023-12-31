"""start app"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from mongoengine import connect, disconnect, DEFAULT_CONNECTION_NAME
from library.library_exceptions import AppException
from patrons.patron_routes import PATRON_ROUTER
from library_item.library_item_routes import LIBRARY_ITEM_ROUTER, LIBRARY_ACTIONS_ROUTER


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect("localhost:27017")
    yield
    disconnect(DEFAULT_CONNECTION_NAME)


app = FastAPI(title="LibraryMGMT", lifespan=lifespan)
app.include_router(PATRON_ROUTER, prefix="/patrons", tags=["Patrons"])
app.include_router(LIBRARY_ITEM_ROUTER, prefix="/items", tags=["Library Items"])
app.include_router(LIBRARY_ACTIONS_ROUTER, prefix="/library", tags=["Library Actions"])


@app.exception_handler(AppException)
async def app_exception_handler(_, exc):
    return JSONResponse({"message": exc.message}, status_code=exc.status_code)


if __name__ == "__main__":
    connect("localhost:27017")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
