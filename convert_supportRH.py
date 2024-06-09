import yaml
from pymongo import MongoClient

def fetch_data_from_mongodb():     
    # Se connecter à MongoDB
    client = MongoClient('localhost', 27017)
    db = client['chat_bot'] 
    collection = db['support_rh'] 

    # Récupérer les données de MongoDB
    data = list(collection.find())

    # Fermer la connexion à MongoDB
    client.close()

    return data

def append_nlu_file(data, nlu_file_path):
    with open(nlu_file_path, 'a', encoding='utf-8') as file:
       for item in data:
            tag = item.get('Tag', '')
            patterns = item.get('Question', [])
            
            file.write(f'- intent: {tag}\n')
            file.write(f'  examples: |\n') 
            file.write(f'    - {patterns}\n') 

# def append_stories_file(data, stories_file_path):
  #  with open(stories_file_path, 'a', encoding='utf-8') as file:
    #   for item in data:
        #    tag = item.get('Tag', '')
         #   file.write(f'- story: {tag}\n')
          #  file.write(f'  steps: \n')
          #  file.write(f'  - intent: {tag}\n')
          #  file.write(f'  - action: utter_{tag} \n') 


def append_rules_file(data, rules_file_path):
    with open(rules_file_path, 'a', encoding='utf-8') as file:
        for item in data:
            tag = item.get('Tag', '')
            file.write(f"- rule: Say {tag}'s information\n")  
            file.write(f'  steps: \n')
            file.write(f'  - intent: {tag}\n')
            file.write(f'  - action: utter_{tag} \n')


def append_domain_file(data, domain_file_path):
   # intents = set(item['intent'] for item in data)
   # entities = set(entity for item in data for entity in item.get('entities', []))

    with open(domain_file_path, 'a', encoding='utf-8') as file:
        for item in data:
            tag = item.get('Tag', '')
            responses = item.get('Réponse', '')
            
            file.write(f'  utter_{tag}:\n')
            file.write(f'  - text: "{responses}"\n')             

# Fetch data from MongoDB
mongo_data = fetch_data_from_mongodb()

# Append data to existing NLU file
append_nlu_file(mongo_data, 'data/RH/nlu.yml')

# Append data to existing stories file
# append_stories_file(mongo_data, 'data/RH/stories.yml')

# Append data to existing rules file
append_rules_file(mongo_data, 'data/RH/rules.yml')

# Append data to existing domain file
append_domain_file(mongo_data, 'data/RH/domain.yml')