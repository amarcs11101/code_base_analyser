~ Steps Followed to create this project 
    1) Selecting a directory for code base analysing .
    2) Using llama index library to find all (java, html , properties ) files present in a directory recursively .
    3) Chunking each and every file using langchain RecursiveCharacterTextSplitter with some overlap between words , so that our llm can find the relationship between each and every sentense
    4) Using the ` Embadding techniques ` of Langchain or any other like(huggingface. OpenAI , Olama, Mistral etc) .
        OpenAI's embadding ` text-embedding-3-large ` is paid version & offers robust embeddings for mixed code and documentation but going for free embaddings 

        ` CodeBERT  ` , ` GraphCodeBERT ` , and ` CodeT5+ ` provide superior embeddings tuned on large-scale code repositories, capturing function signatures, APIs, and structural patterns efficiently. 

        Here There are two Approaches that can be considered to complete this requirement :- 
        1) By Embadding (using any embadding techniques of huggingface , openai , olama , mistral ) and then save those embaddings in vector db for similarity search kind of result .
        2) By Using Prompt Template --> Where the prompt will be given to the LLM and LLM with give the result based on the prompt . Here LLM will use self attension techniques to find the meaningful insights from the entire chunk and give the structed output . 

        ` NOTE:- 
          Embeddings + retrieval could also lead to the same structured output eventually as directly      giving the chunk data to llm.
          However, for this task, since the codebase is fixed and the output expectation is predefined, direct prompting with a well-crafted template is more efficient and aligns perfectly with the requirement.

          As Embeddings make sense if we were building an interactive tool to answer dynamic user questions about the codebase later (a retrieval-augmented system). But here, the objective is extraction, not search.



- App Running Steps
    1) pip install -r requirements.txt
    2) uvicorn main:app
payload :- 
{
  "file_path": "D:\\aaa\\llm_usage\\SakilaProject",
  "chunk_size": 1000
}

# Contains Fast API
# LLM
# Removing __pycache__ file 
Get-ChildItem -Recurse -Include __pycache__,*.pyc,*.pyo | Remove-Item -Force -Recurse

conda create -n fastapi-v1 python=3.10 -y