from ninja import Schema

class CordenadasBancariasSchema(Schema):
    banco: str
    numero_conta: str
    titular_conta: str
    iban: str | None = None
    numero_express: str | None = None
    swift_bic: str | None = None

    class Config:
        orm_mode = True