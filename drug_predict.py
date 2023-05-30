import pandas as pd
import numpy as np
import spacy
import re
import json

df = pd.read_parquet('clean_drug_master.parquet', engine='fastparquet')
df.drug_name = df.drug_name.str.lower().str.strip()
drugs = df.drug_name.str.split("/").to_list()
drugs = [[d.strip() for d in drug] for drug in drugs]

nlp = spacy.load('drugmatcher')


class DrugPredict:

    def __init__(self):
        pass

    @staticmethod
    def getPrediction(query: str, focus: str):
        # Process the text
        text = query
        doc = nlp(text)

        # Print the entities
        query_result = []
        for ent in doc.ents:
            if ent.label_ == 'DRUG':
                query_result.append(ent.text)

        query_result = list(set(query_result))

        result = []
        focus = [f.strip() for f in focus.split(',')]
        # focus = list(set(focus))

        custom_focus = ['drug_name', 'side_effects', 'generic_name', 'drug_classes', 'brand_names',
                        'pregnancy_category', 'csa', 'related_drugs']

        for q in query_result:
            indexes = [index for index, sublist in enumerate(drugs) if q in sublist]

            for idx in indexes:
                try:
                    json_ = df.loc[idx, focus].to_json()
                except:
                    json_ = df.loc[idx, custom_focus].to_json()

                result.append(json.loads(json_))

        return result