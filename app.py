from fastapi import FastAPI
from route.test_route import test
from route.need_route import need
from route.serve_route import serve
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "*", # Izinkan akses dari semua origin. Paling mudah untuk development lokal.
    # Jika ingin lebih spesifik (port Flutter default sering di atas 50000)
    # "http://localhost:50000",
    # "http://127.0.0.1:50000",
]

# 3. Tambahkan Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,           # Mengizinkan header cookie
    allow_methods=["*"],              # Mengizinkan semua metode HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"],              # Mengizinkan semua header dalam permintaan
)

if __name__ == "__main__":
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True)
