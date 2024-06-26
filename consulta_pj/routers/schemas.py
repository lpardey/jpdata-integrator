from pydantic import BaseModel


class JudicaturaSchema(BaseModel):
    idJudicatura: str
    nombreJudicatura: str
    ciudad: str


class GroupedMovimientosSchema(BaseModel):
    judicatura: JudicaturaSchema


class CausasResponse(BaseModel):
    cedula: str
