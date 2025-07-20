from fastapi import APIRouter
from pydantic import BaseModel
from utility.utils import llama_directory_reader , read_prompt_template_content ,setup_prompt_template ,create_llm_object,create_llm_chain_using_lcel, chunk_documents
from pydantic_parser import CodeAnalysisResponse
import os
from dotenv import load_dotenv
analyse_router = APIRouter()

load_dotenv()

class CodeAnalyser(BaseModel):
    file_path :str = "D:\\aaa\\llm_usage\\SakilaProject"
    chunk_size: int = 1000
    prompt : str = "Please analyze the code and provide a summary of its purpose, classes, methods, and complexity."

@analyse_router.post("/code")
async def analyse_code_base(analyse : CodeAnalyser):
    """
    Reading the entire directory with the specified file extensions
    """"" 
    if os.path.isdir(analyse.file_path) is False:
        return {"message": f"The specified path {analyse.file_path} is not a directory."}
    
    docs =llama_directory_reader(analyse.file_path)    
    #print(f"Documents loaded: {docs}")
    if docs is None or len(docs) == 0:
        return {"message": f"No documents found in the specified directory {analyse.file_path}."}
    
    template_prompt = read_prompt_template_content("prompts/code_analysis_prompt.txt")
    if template_prompt is None or len(template_prompt) == 0:    
        return {"message": "Prompt template is empty or not found."} 
    code_chunk=chunk_documents(docs, analyse.chunk_size) 
     # Combine all code chunks from documents
   # code_chunk = "\n".join(doc.get_content() or "" for doc in docs)

    # template_prompt=template_prompt.replace("{code_chunk}", code_chunk) 
    # template_prompt=template_prompt.replace("{file_path}", analyse.file_path)
    print(f"Template Prompt: {template_prompt}")

    prompt_template = setup_prompt_template(template_prompt)
    print("Prompt template set up successfully.")
    llm = create_llm_object(os.getenv("MODEL_NAME"))  
    print("LLM Object created successfully.")
    llm_chain = create_llm_chain_using_lcel(prompt_template, llm)
    print("LLM Chain created successfully.")
    responses = []
    for chunk in code_chunk:
        result = llm_chain.invoke({
            "file_path": analyse.file_path,
            "code_chunk": chunk.page_content,
            "input": analyse.prompt
        })
        responses.append(result)

    return {"message":"Success","data":responses ,"file_path":None, "doc_scan_count":None}