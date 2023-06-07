import pandas as pd
import yaml

# Read all sheets of the Excel file into a dictionary of DataFrames
dfs = pd.read_excel('./crawleddata.xlsx', sheet_name=None, engine='openpyxl')

# Initialize an empty dictionary to store the data
data = {}
IL = set(['  - greet', '  - goodbye', '  - affirm', '  - deny', '  - mood_great', '  - mood_unhappy', '  - bot_challenge'])

# Iterate over the dictionary of DataFrames
for sheet_name, df in dfs.items():
    # Iterate over the dataframe's rows as (index, Series) pairs
    for index, row in df.iterrows():
        item = row['Item'].replace(' ', '_').replace('(', '').replace(')', '').replace(',', '').replace('-', '_')
        for column in df.columns[1:]:
            value_without_commas = str(row[column]).replace(',', '')
            intent = f"{column}_{item}".replace(' ', '_')
            key = f"  utter_{column.replace(' ', '_')}_{item.replace(' ', '_')}"
            text = f"{item.replace('_', ' ')} of {column.replace('_', ' ')} is {value_without_commas}."

            if key not in data:
                data[key] = []
            if {"text": text} not in data[key]:  # check if the text already exists
                data[key].append({"text": text})

            IL.add('  - ' + intent)

preDesigned1 = {
    "utter_greet": [{"text": "Hey! How are you?"}],
    "utter_cheer_up": [{"text": "Here is something to cheer you up:", "image": "https://i.imgur.com/nGF1K8f.jpg"}],
    "utter_did_that_help": [{"text": "Did that help you?"}],
    "utter_happy": [{"text": "Great, carry on!"}],
    "utter_goodbye": [{"text": "Bye"}],
    "utter_iamabot": [{"text": "I am a bot in Omron Asia, powered by Rasa OpenSource."}]
}

# Write the data to a YAML file
with open('domain.yml', 'w') as f:
    f.write('version: "3.1" \n')
    f.write('\n')
    f.write('intents:\n')
    f.write('\n'.join(IL))
    f.write('\n\n')
    f.write("responses:\n")
    for key, value in preDesigned1.items():
        f.write(f'  {key}:\n')
        for v in value:
            f.write(f'  - text: "{v["text"]}"\n')
            if 'image' in v:
                f.write(f'    image: "{v["image"]}"\n')

    for key, value in data.items():
        f.write(key + ':\n')
        for v in value:
            f.write('  - text: "' + v['text'] + '"\n')

    f.write('\n')
    f.write('actions: \n')
    f.write('  - action_fallback \n')
