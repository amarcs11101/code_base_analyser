from fastapi import APIRouter
from pydantic import BaseModel
from utility.utils import llama_directory_reader , read_prompt_template_content ,setup_prompt_template ,create_llm_object,create_llm_chain_using_lcel, chunk_documents , group_documents_by_extension_and_batch,combine_batch_content
from pydantic_parser import CodeAnalysisResponse
from db.ChromDbOperation import store_llm_responses_in_vector_db , search_similar_code_in_vector_db
import os
from dotenv import load_dotenv
import asyncio
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
            "input": analyse.prompt
        })

    responses = await asyncio.gather(*(analyse_batch(batch) for batch in batches))
    #saving in chroma db
    store_llm_responses_in_vector_db(responses)

    item_count = { key:  len(value) for key , value  in scanned_file_names.items() }
    return {"responses": responses ,"scanned_file_names": scanned_file_names , "item_count": item_count}

@analyse_router.get("/query")
async def query_code_base(query: str, top_k: int = 3):
    """
    Search for similar code in the vector database.
    """
    persist_directory = "./chroma_db"
    results = await asyncio.to_thread(
        search_similar_code_in_vector_db, query, persist_directory, top_k
    )
    return {"query": query, "results": results}