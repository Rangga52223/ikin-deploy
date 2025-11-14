from route import test
from feature.test import test_func
@test.get("/")
async def test_r():
    return test_func()