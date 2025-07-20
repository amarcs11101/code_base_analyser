from fastapi import APIRouter
from pydantic import BaseModel
from utility.utils import llama_directory_reader , read_prompt_template_content ,setup_prompt_template ,create_llm_object,create_llm_chain_using_lcel, chunk_documents , group_documents_by_extension_and_batch,combine_batch_content
from pydantic_parser import CodeAnalysisResponse
from db.ChromDbOperation import save_data_in_vector_db , perform_similarity_search
from utility.constants import CHROME_DB_STORAGE_PATH
import os
from dotenv import load_dotenv
import asyncio
import shutil
#from git import Repo
analyse_router = APIRouter()

load_dotenv()

class CodeAnalyser(BaseModel):
    file_path :str = "D:\\aaa\\llm_usage\\SakilaProject"
    chunk_size: int = 1000
    git_url: str=""
   
@analyse_router.post("/knowledge-base")
async def create_git_knowledge_base(analyse : CodeAnalyser):
    """
    Reading the entire directory with the specified file extensions
    """"" 
    if os.path.isdir(analyse.file_path) is False:
        return {"message": f"The specified path {analyse.file_path} is not a directory."}
    
    #if analyse.git_url and len(analyse.git_url) > 0:
    #    Repo.clone_from(analyse.git_url, analyse.file_path)

    docs =llama_directory_reader(analyse.file_path)    
    #print(f"Documents loaded: {docs}")
    if docs is None or len(docs) == 0:
        return {"message": f"No documents found in the specified directory {analyse.file_path}."}
    
    template_prompt = read_prompt_template_content("prompts/code_analysis_prompt.txt")
    if template_prompt is None or len(template_prompt) == 0:    
        return {"message": "Prompt template is empty or not found."}  
 
    print(f"Template Prompt: {template_prompt}")

    prompt_template = setup_prompt_template(template_prompt)
    print("Prompt template set up successfully.")
    print(f"Prompt Template: {prompt_template}")
    print(f"input vraibles are : {prompt_template.input_variables}")

    llm = create_llm_object(os.getenv("MODEL_NAME"))  
    print("LLM Object created successfully.")

    llm_chain = create_llm_chain_using_lcel(prompt_template, llm)
    print("LLM Chain created successfully.")

    responses = [] 
    batches , scanned_file_names = group_documents_by_extension_and_batch(docs, max_chars=8000) 
    
    async def analyse_batch(batch):
        combined_content = combine_batch_content(batch)
        return await llm_chain.ainvoke({ 
            "file_path": analyse.file_path,
            "code_chunk": combined_content,
            "input": prompt_template
        })

    responses = await asyncio.gather(*(analyse_batch(batch) for batch in batches)) 

    shutil.rmtree(CHROME_DB_STORAGE_PATH, ignore_errors=True)

    #saving in chroma db
    save_data_in_vector_db(responses)

    item_count = { key:  len(value) for key , value  in scanned_file_names.items() }
    return {"message":f"Successfully extracted the insights of the project .  Please call /query api to ask any question related to the project {analyse.file_path} ","data": responses ,"scanned_file_names": scanned_file_names , "item_count": item_count}

@analyse_router.get("/knowledge-base")
async def query_git_knowledge_base(query: str, top_k: int = 3):
    """
    Search for similar code in the vector database.
    """
    persist_directory = CHROME_DB_STORAGE_PATH
    results = perform_similarity_search(query, persist_directory, top_k)
    if not results or len(results) == 0:
        return {"message": "No similar code found."}
    return {"query": query, "results": results}