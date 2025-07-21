from pydantic import BaseModel, Field
from typing import List, Dict, Any 
"""
My Own Pydantic Output Parser for implementing the LCEL (Language Chain Execution Language) for code analysis.
"""
class CodeAnalysisResponse(BaseModel):
    api_query: str = Field(
        ...,
        description="The original user query given to the API.",
        example="Give me files related to security configuration."
    )
    question: str = Field(
        ...,
        description="Optional clarification or rephrased version of the user query.",
        example="Give me files related to security configuration."
    )
    context_used: List[str] = Field(
        ...,
        description="List of files, components, or configurations used to answer the question.",
        example=["SuccessHandler.java", "UserDetailsServiceImpl.java", "WebSecurityConfig.java"]
    )
    extracted_information: Dict[str, Any] = Field(
        ...,
        description="Structured answer extracted from the context in key-value or nested format.",
        example={
            "controllers": [
                "SuccessHandler.java",
                "UserDetailsServiceImpl.java",
                "WebSecurityConfig.java"
            ]
        }
    )
    explanation: str = Field(
        ...,
        description="A brief explanation of how this answer was derived from the provided context.",
        example="This answer is derived directly from the classes involved in securing the web application using Spring Security in the  project."
    )