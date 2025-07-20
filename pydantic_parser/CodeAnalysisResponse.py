from pydantic import BaseModel, Field
from typing import List, Optional 
"""
My Own Pydantic Output Parser for implementing the LCEL (Language Chain Execution Language) for code analysis.
"""
class ClassDescription(BaseModel):
    name: str
    description: str

class MethodDescription(BaseModel):
    name: str
    parameters: List[str]
    returns: str
    description: str

class CodeAnalysisResponse(BaseModel):
    file_path: str = Field(..., description="Path to the file being analyzed")
    purpose: str = Field(..., description="Short summary of the file's purpose")
    classes: List[ClassDescription]
    methods: List[MethodDescription]
    complexity: str = Field(..., description="Complexity level of the code (simple/moderate/complex)")
    complexity_reason: Optional[str] = Field(None, description="Reason for the complexity classification")