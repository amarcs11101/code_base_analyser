from fastapi import APIRouter
from pydantic import BaseModel
from utility.utils import llama_directory_reader, chunk_documents 
import os
analyse_router = APIRouter()

class CodeAnalyser(BaseModel):
    file_path :str
    chunk_size: int = 1000

@analyse_router.post("/code")
async def analyse_code_base(analyse : CodeAnalyser):
    """
    Reading the entire directory with the specified file extensions
    """"" 
    if os.path.isdir(analyse.file_path) is False:
        return {"message": f"The specified path {analyse.file_path} is not a directory."}
    
    docs =llama_directory_reader(analyse.file_path)    
    print(f"Documents loaded: {docs}")
    if docs is None or len(docs) == 0:
        return {"message": f"No documents found in the specified directory {analyse.file_path}."}
    
    """ 
    Chunking the documents into smaller parts
    """
    chunks,file_path = chunk_documents(docs, analyse.chunk_size)
     
    return {"message":"Success","data":chunks ,"file_path":file_path, "doc_scan_count":len(file_path)}