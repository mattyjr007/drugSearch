from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any
app = FastAPI()


class DrugSeachIn(BaseModel):
    drug_query: str = Field(example="What is the side effects of paracetamol ?")
    focus: str  = Field(default=None, example="side_effects, drug_classes")

    class Config:
        schema_extra = {
            "example": {
                "drug_query": "What is the side effects of paracetamol ?",
                "focus": "side_effects, drug_classes",
            }
        }


class DrugSeachOut(BaseModel):
    company_name: str = None
    product_services: list[Any] = []
    SIC: list[Any] = []
    NAICS: list[Any] = []
    Url: str | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/adrugsearch", response_model= list[DrugSeachOut], response_model_exclude_unset=True)
async def drugSearch(drug_query:str, focus: str = None ) -> Any:
    return [{'company_name': drug_query}]


@app.post("/api/drugsearch", response_model= list[DrugSeachOut], response_model_exclude_unset=True)
async def drugSearch2(drugIn: DrugSeachIn) -> Any:
    return [{'company_name': drugIn.drug_query}]
