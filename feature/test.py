from fastapi.responses import JSONResponse
def test_func():
    return JSONResponse(status_code=200, content={
        "succes" : True,
        "message": 'checkpoint'
    })