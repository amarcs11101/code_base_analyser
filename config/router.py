from fastapi import APIRouter 
from api.v1.analyse import analyse_router
router = APIRouter()

router.include_router(analyse_router,prefix="/analyse", tags=["CODEBASE ANALYSER"])
