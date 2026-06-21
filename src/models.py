from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class ZendeskTicket(BaseModel):
    ticket_id: int
    subject: str
    description: str
    
class ReviewUpdate(BaseModel):
    answer: str