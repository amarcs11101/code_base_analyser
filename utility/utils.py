"""
@author: Abhishek Amar
@date: 2025-07-19
@description: Utility functions for all supporting operations in the code base analyser.
@version: 1.0
"""  
from llama_index.core import SimpleDirectoryReader  
from langchain_openai.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate  
from pydantic_parser import CodeAnalysisResponse 
from langchain_core.output_parsers import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document as LangChainDocument
from llama_index.core.schema import Document
from typing import List

def convert_llama_to_langchain(docs):
    lc_docs = []
    for doc in docs:
        lc_docs.append(
            LangChainDocument(
                page_content=doc.get_content(),
                metadata=doc.metadata
            )
        )
    return lc_docs

def llama_directory_reader(dir_path: str) -> List[Document]:    
    """
    Reads all files in a directory and returns their content as documents in easy way without looping it.
    Args:
        dir_path (str): The path to the directory to read files from.
    Returns:
        List[Document]: A list of documents containing the content of each file.
    """
    #reader = SimpleDirectoryReader(input_dir=dir_path , recursive=True , required_exts=[".java", ".html",".properties"])
    reader = SimpleDirectoryReader(input_dir=dir_path , recursive=True , required_exts=[".java", ".html",".properties"])
    documents = reader.load_data()
    return documents

def chunk_documents(documents, chunk_size=1000 , overlap=200):
    """
    Splits documents into chunks of specified size.
    """
    lc_docs = convert_llama_to_langchain(documents)
    recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size
                                                             , chunk_overlap=overlap)
    chunks = recursive_text_splitter.split_documents(lc_docs)  
    return chunks

def read_prompt_template_content(file_path)-> str:
    """
    Reads the content of a file and returns it as a string.
    Args:
        file_path (str): The path to the file to read.  
    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def setup_prompt_template(template:str) -> ChatPromptTemplate:
    """
    Sets up a prompt template for code analysis using PydanticOutputParser.
    Args:
        template (str): The template string to use for the prompt.    
    """
    #pydantic_output_parser = PydanticOutputParser(pydantic_object=CodeAnalysisResponse)
    prompt=ChatPromptTemplate.from_messages([
        ("system",template),
        ("human","{code_chunk}"),
        ("user","{input}")
    ]
)
    #prompt = prompt.partial(format_instructions=pydantic_output_parser.get_format_instructions())
    return prompt

def create_llm_object(model_name="gpt-3.5-turbo", temperature=0.0, max_tokens=1000) -> ChatOpenAI:
    """
    Creates a ChatOpenAI instance with specified parameters.
    Args:
        model_name (str): The name of the model to use. Defaults to "gpt-3.5-turbo".
        temperature (float): The temperature for the model. Defaults to 0.0.
        max_tokens (int): The maximum number of tokens to generate. Defaults to 1000.  
    """
    return ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens, streaming=True)

def create_llm_chain_using_lcel(prompt, llm) :
    """
    Advantage of using LCEL is it allows for a more modular and flexible approach to building LLM chains.
    It enables the use of various components like text splitters, prompts, LLMs,    
    and output parsers in a more structured way, making it easier to manage and modify the chain.
    This function creates a chain that processes code documents through a series of transformations,
    including text splitting, conversion to dictionaries, prompting, LLM processing, and output parsing.
    This is particularly useful for analyzing code files and extracting structured information from them. 
    Args:   
        prompt (PromptTemplate): The prompt template to use.
        llm (ChatOpenAI): The language model to use.
        code_document (str, optional): The code document to analyze. Defaults to None.
        output_parser (PydanticOutputParser, optional): The output parser to use. Defaults to None.
    """
    #pydantic_output_parser = PydanticOutputParser(pydantic_object=CodeAnalysisResponse)
    parser=StrOutputParser()
    
    chain = ( 
              prompt
            | llm
            | parser
    )
    return chain

def group_documents_by_extension_and_batch(docs, max_chars=8000):
    """
    Groups documents by extension and batches them by total character size.
    """
    file_groups = {
        "java": [],
        "html": [],
        "properties": []
    }
    scanned_file_names = {
        "java":set(),
        "html": set(),
        "properties":set()
    }
    for doc in docs:
        file_name = doc.metadata.get("file_name", "").lower()
        if file_name.endswith(".java"):
            file_groups["java"].append(doc)
            scanned_file_names["java"].add(file_name)
        elif file_name.endswith(".html"):
            file_groups["html"].append(doc)
            scanned_file_names["html"].add(file_name)
        elif file_name.endswith(".properties"):
            file_groups["properties"].append(doc)
            scanned_file_names["properties"].add(file_name)

    batches = []

    for extension, group in file_groups.items():
        current_batch = []
        current_size = 0
        for doc in sorted(group, key=lambda x: len(doc.get_content()), reverse=True):
            content_size = len(doc.get_content())
            if current_size + content_size > max_chars:
                if current_batch:
                    batches.append(current_batch)
                current_batch = []
                current_size = 0
            current_batch.append(doc)
            current_size += content_size
        if current_batch:
            batches.append(current_batch)

    return batches , scanned_file_names

def combine_batch_content(batch):
    return "\n\n".join(doc.get_content() for doc in batch)


 

