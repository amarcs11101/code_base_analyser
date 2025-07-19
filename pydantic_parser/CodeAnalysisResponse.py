from pydantic import BaseModel, Field
from typing import List, Optional
{
    "file_path": "{file_path}",
    "purpose": "<short summary of file purpose>",
    "classes": [
        {
            "name": "<class name>",
            "description": "<short description>"
        }
    ],
    "methods": [
        {
            "name": "<method/function name>",
            "parameters": ["<param1>", "<param2>"],
            "returns": "<return type>",
            "description": "<short description>"
        }
    ],
    "complexity": "<simple/moderate/complex>",
    "complexity_reason": "<why you classified it as such>"
}
"""
My Own Pydantic Output Parser for implementing the LCEL (Language Chain Execution Language) for code analysis.
"""
class CodeAnalysisResponse(BaseModel):
    file_path: str = Field(..., description="Path to the file being analyzed")
    purpose: str = Field(..., description="Short summary of the file's purpose")
    classes: List[dict] = Field(..., description="List of classes with their names and descriptions")
    methods: List[dict] = Field(..., description="List of methods with their names, parameters, return types, and descriptions")
    complexity: str = Field(..., description="Complexity level of the code (simple/moderate/complex)")
    complexity_reason: Optional[str] = Field(None, description="Reason for the complexity classification")