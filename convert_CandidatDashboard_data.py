import yaml
from pymongo import MongoClient

def fetch_data_from_mongodb():   
    # Se connecter à MongoDB
    client = MongoClient('localhost', 27017)
    db = client['chatbot_candidat'] 
    collection = db['dashboard'] 

    # Récupérer les données de MongoDB
    data = list(collection.find())

    # Fermer la connexion à MongoDB
    client.close()

    return data

def append_nlu_file(data, nlu_file_path):
    with open(nlu_file_path, 'a', encoding='utf-8') as file:
       for item in data:
            tag = item.get('tag', '')
            patterns = item.get('patterns', [])
            
            file.write(f'- intent: {tag}\n')
            file.write(f'  examples: |\n')
            for pattern in patterns:
                file.write(f'    - {pattern}\n')

def append_stories_file(data, stories_file_path):
    with open(stories_file_path, 'a', encoding='utf-8') as file:
       for item in data:
            tag = item.get('tag', '')
            file.write(f'- story: {tag}\n')
            file.write(f'  steps: \n')
            file.write(f'  - intent: {tag}\n')
            file.write(f'  - action: utter_{tag} \n')


def append_rules_file(data, rules_file_path):
    with open(rules_file_path, 'a', encoding='utf-8') as file:
        for item in data:
            tag = item.get('tag', '')
            file.write(f"- rule: Say {tag}'s information\n")  
            file.write(f'  steps: \n')
            file.write(f'  - intent: {tag}\n')
            file.write(f'  - action: utter_{tag} \n')


def append_domain_file(data, domain_file_path):
   # intents = set(item['intent'] for item in data)
   # entities = set(entity for item in data for entity in item.get('entities', []))

    with open(domain_file_path, 'a', encoding='utf-8') as file:
        for item in data:
            tag = item.get('tag', '')
            responses = item.get('responses', '')
            
            file.write(f'  utter_{tag}:\n')
            file.write(f'  - text: "{responses}"\n')             

# Fetch data from MongoDB
mongo_data = fetch_data_from_mongodb()

# Append data to existing NLU file
append_nlu_file(mongo_data, 'data/nlu_candidat.yml')

# Append data to existing stories file
append_stories_file(mongo_data, 'data/stories_candidat.yml')

# Append data to existing rules file
append_rules_file(mongo_data, 'data/rules_candidat.yml')

# Append data to existing domain file
append_domain_file(mongo_data, 'domain_candidat.yml')