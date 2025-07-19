from fastapi import APIRouter
from pydantic import BaseModel

analyse_router = APIRouter()

class CodeAnalyser(BaseModel):
    file_path :str

@analyse_router.post("/code")
async def analyse_code_base(analyse : CodeAnalyser):
    return {"message":"Success"}