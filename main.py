from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import re
nlp = spacy.load('pl_core_news_sm')
app = FastAPI()
class ReguestModel(BaseModel):
    text:str
    separator:str


@app.post("/GetRecords/")
async def get_records(item:ReguestModel):
    return get_names(item.text,item.separator)

def extract_names(text):
    doc = nlp(text)
    names = []
    for ent in doc.ents:
        if ent.label_ == 'persName':
            names.append(ent.text)
    if len(names) == 0:
        return None
    return names[0]

def get_code(text):
    pattern = r'\b\d{11}\b'
    codes = re.findall(pattern,text)
    if len(codes) == 0:
        return None
    return codes[0]

def find_last_name(text, target_word):
    pattern = r'\b' + re.escape(target_word) + r'\b\s+(\w+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None
def get_names(text,separator):

    date = text.split(separator)
    entities = []
    for i in date:
        if i != "":
            name = extract_names(i)
            last_name = find_last_name(i, name)
            ids = get_code(i)
            entities.append( {"name":name, "lastName":last_name,"id":ids, "text":i})
    return entities
