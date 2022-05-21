#Try grouping potentially split up entities
import logging
import joblib


logging.basicConfig(filename='ner.log', encoding='utf-8', level=logging.INFO)


import torch
import re
from simpletransformers.ner import NERModel

cuda_available = torch.cuda.is_available()

model = joblib.load("ner_classifier.joblib")
      
new_labels_enum = {"PER":"PERSON","LOC":"GPE","ORG":"ORGANIZATION","MISC":"MISCELLANEOUS"}
begin_ent = re.compile("B-[A-Za-z]+")
def group_split_entities(predictions):
  entities = {}
  list_prediction = list(predictions[0])
  for i in range(0,len(list_prediction)):
    end_entity = ""
    list_ent = list_prediction[i]
    entity = list(list_ent.keys())[0]
    if list_ent[entity] == "O" or re.match("I-[A-Za-z]+",list_ent[entity]):
      continue
    elif begin_ent.match(list_ent[entity]):
        end_entity = list_ent[entity][2:]
        valid_ent=True
        new_entity = entity
        i=i+1
        while i< len(list_prediction) and valid_ent:
          list_ent=list_prediction[i]
          entity = list(list_ent.keys())[0]
          if re.match("I-"+end_entity,list_ent[entity]):
            new_entity = new_entity+" "+entity
            i+=1
          else:
            valid_ent = False        
        entities = {**entities, new_entity:new_labels_enum[end_entity]}
        
    else:
      entities = {**entities,entity:list_ent[entity]}
    
  return entities

def predict_ner(user_input):
    logging.info("Making Prediction")
    prediction, _ = model.predict([user_input])
    grouped_entities = group_split_entities(prediction)
    logging.info('\nNER PREDICTION \nUser input: %s\n Predicted Entities: %s', user_input, str(grouped_entities))
    return grouped_entities

def get_entity(user_input,entity_type):
  predictions = predict_ner(user_input)
  people = [k for k in predictions.keys() if predictions[k]==entity_type]
  return people