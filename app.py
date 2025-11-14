from fastapi import FastAPI
from route.test_route import test
from route.need_route import need
from route.serve_route import serve
import uvicorn
app = FastAPI(
    title="HTH Apps API",
    version="Alpha 1.0.0",
    description="App to analysis and visualization telemetries",
    openapi_url=None,      
    docs_url=None,         
    redoc_url=None         
)

app.include_router(test)
app.include_router(need)
app.include_router(serve)


if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True)
