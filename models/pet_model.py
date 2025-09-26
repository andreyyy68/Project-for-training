from pydantic import BaseModel
from typing import Optional, List

class CategoryModel(BaseModel):
    id: int
    name: str

class TagModel(BaseModel):
    id: int
    name: str

class PetModel(BaseModel):
    id: int
    category: Optional[CategoryModel]
    name: str
    photoUrls: List[str]
    tags: Optional[List[TagModel]]
    status: Optional[str]