from datetime import datetime

from pydantic import BaseModel


class NewCausaSchema(BaseModel):
    idJuicio: str
    nombreDelito: str
    fechaIngreso: datetime


class JudicaturaSchema(BaseModel):
    idJudicatura: str
    nombreJudicatura: str
    ciudad: str


class MovimientoCausaSchema(BaseModel):
    causa: NewCausaSchema
    judicatura: JudicaturaSchema
