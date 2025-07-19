from fastapi import FastAPI 
from config.router import router
import uvicorn

app = FastAPI()   


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port="8000")
