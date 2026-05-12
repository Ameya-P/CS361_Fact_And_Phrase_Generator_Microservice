from pydantic import BaseModel
from typing import Optional

class PhraseRequest(BaseModel):
    category: Optional[str] = None
    
class PhraseResponse(BaseModel):
    phrase: str
    category: Optional[str] = None
    num_uses: int