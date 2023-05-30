from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any
from drug_predict import DrugPredict

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
    drug_name: str = None
    side_effects: list[Any] = []
    generic_name: str = None
    drug_classes: list[Any] = []
    brand_names: list[Any] = []
    activity: str = None
    rx_otc: str = None
    pregnancy_category: str = None
    csa: str = None
    alcohol: str = None
    medical_condition: str = None
    related_drugs: list[Any] = []
    rating: Any = None
    medical_condition_description: str = None


@app.get("/")
async def root():
    return {"message": "Hello, Head over to /docs"}


@app.get("/adrugsearch", response_model= list[DrugSeachOut], response_model_exclude_unset=True)
async def drugSearch(drug_query:str, focus: str = None ) -> Any:
    result = DrugPredict.getPrediction(drug_query, focus)  # [{'company_name': drugin.drug_query}]
    return result


@app.post("/api/drugsearch", response_model= list[DrugSeachOut], response_model_exclude_unset=True)
async def drugSearch2(drugin: DrugSeachIn) -> Any:
    result = DrugPredict.getPrediction(drugin.drug_query, drugin.focus) #[{'company_name': drugin.drug_query}]
    return result
