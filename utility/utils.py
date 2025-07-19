"""
@author: Abhishek Amar
@date: 2025-07-19
@description: Utility functions for all supporting operations in the code base analyser.
@version: 1.0
"""

from llama_index.core import SimpleDirectoryReader 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline
from transformers import AutoTokenizer, AutoModel

def llama_directory_reader(dir_path: str):    
    """
    Reads files from a directory and returns a list of documents.
    Only files with specified extensions (.py, .html, .js) are included.
    Args:
        dir_path (str): The path to the directory to read files from.
    Returns:
        list: A list of documents read from the directory.
    """ 
    reader = SimpleDirectoryReader(input_dir=dir_path , recursive=True , required_exts=[".java", ".html",".properties"])
    documents = reader.load_data()
    return documents

def chunk_documents(documents, chunk_size=1000 , overlap=200):
    """
    Splits documents into chunks of specified size.
    """
    recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size
                                                             , chunk_overlap=overlap)
    chunks =[]
    for doc in documents:
        file_path = doc.metadata.get("file_path", "")
        text = doc.get_content()
        splits = recursive_text_splitter.split_text(text)
        for split in splits:
            chunks.append({
                "source": file_path,
                "content": split
            })

    return chunks , [doc.metadata.get("file_path", "") for doc in documents]

def perform_embadding(chunks):    
    pipe = pipeline("feature-extraction", model="microsoft/codebert-base")
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")

