from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.portfolio import router as portfolio_router, prices_router, imports_router

app = FastAPI(
    title="FinAssistant API",
    description="Financial Assistant Backend API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(portfolio_router)
app.include_router(prices_router)
app.include_router(imports_router)


@app.get("/")
def root():
    return {"message": "FinAssistant API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
