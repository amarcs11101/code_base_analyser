~ Project Overview & Best Practices :-

  This project analyzes the SakilaProject GitHub repository to extract meaningful insights from the codebase. It provides structured knowledge such as purpose, architecture, key methods, complexity, and other technical metadata by leveraging LLMs (Large Language Models) via LangChain and LlamaIndex.

  The final output is stored in a structured JSON format, suitable for further analysis or documentation purposes.

# Project Structure :-
          code_base_analyser/
            ├── api/v1/
            │   └── analyse.py                       # API for querying the LLM
            ├── config/
            │   └── router.py                        # API routers
            ├── db/
            │   └── ChromaDbOperation.py             # Operations for Vector DB (Chroma)
            ├── prompts/
            │   ├── code_analysis_prompt.txt         # Prompt for analyzing code
            │   └── query_knowledge_base_prompt.txt  # Prompt for querying vector DB
            ├── pydantic_parser/
            │   └── CodeAnalysisResponse.py          # Pydantic models for structured output
            ├── utility/
            │   ├── constants.py                     # Constants for code processing
            │   └── utils.py                         # Utility functions
            ├── .env                                  # API Keys / Env variables / LangSmith config
            ├── requirements.txt                      # Python dependencies
            ├── README.md                             # Project documentation
            ├── BEST_PRACTICES.md                     # Best practices guide
            └── main.py                               # Entry point for running the pipeline



~ Approach & Methodology
  - Codebase Ingestion (Using llama index ` SimpleDirectoryReader ` as it works faster)
  - Chunking for LLM Token Limits
      Split files:
          - Group by file type.
          - Split content into logical, syntactic, or semantic blocks.
          - Ensure no chunk exceeds LLM token limits.
  - LLM Integration
        - LLM: OpenAI gpt-3.5-turbo , GPT-4o / GPT-4-turbo (suitable for code understanding).
        - Framework: LangChain LCEL for structured prompts and output parsing.

~ Knowledge Extraction
    Prompts:
        -----------------------
        | code_analysis_prompt |
        ------------------------
        1. Summarize the purpose of the code.
        2. Identify and list all class names (with short descriptions).
        3. Identify and list all method/function names, including parameters and return types.
        4. Evaluate the complexity of the code (simple, moderate, complex) and provide reasoning.
        5. Ensure the extracted knowledge is structured in a well-organized, readable, and easily      consumable JSON format.
       ----------------------------------
       |query_knowledge_base_prompt.txt |
       ----------------------------------
        1. Output must ONLY be valid JSON.
        2. DO NOT write "Here is your JSON", "Sure!", "Output:", or anything outside the JSON.
        3. If no information is found, clearly state this in `extracted_information` and explain why in `explanation`.
        4. DO NOT include ```json markdown fences.
        5. START your output with '{' and end with '}'.

~  How to Run
      NOTE:- need to clone the SakilaProject if its not in local & then use its file path in the payload
            This can be made dynamic but as of now i haven't done that . 
      1) Enter all the mentioned api key's value .env 
      2) pip install -r requirements.txt
      3) uvicorn main:app --reload
      4) open swagger url :- http://localhost:8000/docs
      5) All the logs can be tracked in the langsmith portal inside logs

~ Assumptions
      1) SakilaProject follows standard Java project structure.
      2) If you are using gpt-3.5-turbo today via OpenAI API, most likely using the 16k version by  default (16,385 tokens).

~ What Does This Limit Include?
     1) Prompt (input) + Completion (output) combined cannot exceed the token limit.
     2) Tokens ≈ words but not exactly:
     3) Its currently answering the question related to all java files only. 
















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

5.  To make it fast following below concepts . 
    ------------------------------------------
   - Combine .java files together (by size or folders). 
   - Aim for chunks of 2000-3000 tokens. 
   - 1 LLM call processes meaningful larger batch.

- App Running Steps
    1) pip install -r requirements.txt
    2) uvicorn main:app --reload
payload :- 
{
  "file_path": "D:\\aaa\\llm_usage\\SakilaProject",
  "chunk_size": 1000
}

############################ BEST PRACTICES ###############################
1) At the end of your prompt, we should add strict instruction (this helps ChatPromptTemplate work as expected):
2) Don't Query Directly using apikey everytime , instead better to query the vector db which would be cost effective
3) 
###########################################################################

# Contains Fast API
# LLM
# Removing __pycache__ file 
Get-ChildItem -Recurse -Include __pycache__,*.pyc,*.pyo | Remove-Item -Force -Recurse

conda create -n fastapi-v1 python=3.10 -y

Tested on question list using api
-------------------------------- 

"What controllers handle customer operations?"

"Give me files related to security configuration."

"Show me files with staff-related methods."

"what are the api available inside customer controller?"

list down all classes present in this project