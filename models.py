from pydantic import BaseModel
from typing import Optional
from bson.objectid import ObjectId

class PhraseRequest(BaseModel):
    category: Optional[str] = None
    
class PhraseResponse(BaseModel):
    _id: ObjectId
    title: Optional[str] = None
    phrase: str
    category: Optional[str] = None
    num_uses: int