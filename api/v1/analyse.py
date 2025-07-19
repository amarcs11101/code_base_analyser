from fastapi import APIRouter
from pydantic import BaseModel
from utility.utils import llama_directory_reader , read_prompt_template_content
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
    
    template_prompt = read_prompt_template_content("prompts/code_analysis_prompt.txt")
    if template_prompt is None or len(template_prompt) == 0:    
        return {"message": "Prompt template is empty or not found."} 
     
     # Combine all code chunks from documents
    code_chunk = "\n".join(doc.get_content() for doc in docs)  

    template_prompt=template_prompt.replace("{code_chunk}", code_chunk)
    
    """ 
    Chunking the documents into smaller parts
    """ 
     
    return {"message":"Success","data":template_prompt ,"file_path":None, "doc_scan_count":None}