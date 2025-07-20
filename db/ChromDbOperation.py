from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List  
import json

def save_data_in_vector_db(llm_responses: List[str], persist_directory: str = "./chroma_db"
):
    """
    Stores LLM structured responses into Chroma vector DB with semantic embedding and dynamic metadata.

    Args:
        llm_responses (List[str]): List of JSON strings (LLM responses).
        persist_directory (str): Directory path to persist Chroma DB.
        language (str): Programming language for metadata (optional, default 'Java').
    """
    llm_list = list(set(llm_responses))
    embedding_function = OpenAIEmbeddings()
    docs_to_store = []

    for response_str in llm_list:
        if not response_str or not response_str.strip():
            print("Skipping empty response.")
            continue

        try:
            response_json = json.loads(response_str)
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON:\n{response_str}")
            continue

        file_path = response_json.get("file_path", "Unknown")
        project = file_path.split("\\")[-1] if "\\" in file_path else "UnknownProject"

        purpose = response_json.get("purpose", "")
        class_descriptions = ", ".join(
            f"{cls['name']} ({cls['description']})"
            for cls in response_json.get("classes", [])
        )
        method_names = ", ".join(
            method['name'] for method in response_json.get("methods", [])
        )
        complexity = response_json.get("complexity", "")

        text_to_embed = (
            f"This code belongs to project {project}. Purpose: {purpose}. "
            f"Classes involved: {class_descriptions}. "
            f"Methods included: {method_names}. "
            f"Complexity is {complexity}."
        )

        metadata = {
            "file_path": file_path,
            "raw_json": response_str, 
            "project": project,
        }

        doc = Document(
            page_content=text_to_embed,
            metadata=metadata
        )

        docs_to_store.append(doc)

        docs_to_store.append(doc)
 
    vectorstore = Chroma.from_documents(
        documents=docs_to_store,
        embedding=embedding_function,
        persist_directory=persist_directory
    )
    vectorstore.persist() 
    print(f"Stored {len(docs_to_store)} documents in Chroma DB at {persist_directory}.")


def perform_similarity_search(query: str, persist_directory: str = "./chroma_db", top_k: int = 3):
    embedding_function = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory=persist_directory,embedding_function=embedding_function)

    results = vectorstore.similarity_search(query, k=top_k)

    for idx, doc in enumerate(results, 1):
        print(f"\n Result #{idx}")
        print(f"Content:\n{doc.page_content}\n")
        print(f"Metadata:\n{doc.metadata}\n")
        print("-" * 50)

    return results

