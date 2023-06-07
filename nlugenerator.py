import pandas as pd

# Read the Excel file
xlsx = pd.ExcelFile('./crawleddata.xlsx')

# Predefined intents
yaml_data = [
    {
        "intent": "greet",
        "examples": "- hey\n- hello\n- hi\n- hello there\n- good morning\n- good evening\n- moin\n- hey there\n- let's go\n- hey dude\n- goodmorning\n- goodevening\n- good afternoon\n- how are you\n- nice to meet you"
    },
    {
        "intent": "goodbye",
        "examples": "- cu\n- good by\n- cee you later\n- good night\n- bye\n- goodbye\n- have a nice day\n- see you around\n- bye bye\n- see you later"
    },
    {
        "intent": "affirm",
        "examples": "- yes\n- y\n- indeed\n- of course\n- that sounds good\n- correct"
    },
    {
        "intent": "deny",
        "examples": "- no\n- n\n- never\n- I don't think so\n- don't like that\n- no way\n- not really"
    },
    {
        "intent": "mood_great",
        "examples": "- perfect\n- great\n- amazing\n- feeling like a king\n- wonderful\n- I am feeling very good\n- I am great\n- I am amazing\n- I am going to save the world\n- super stoked\n- extremely good\n- so so perfect\n- so good\n- so perfect"
    },
    {
        "intent": "mood_unhappy",
        "examples": "- my day was horrible\n- I am sad\n- I don't feel very well\n- I am disappointed\n- super sad\n- I'm so sad\n- sad\n- very sad\n- unhappy\n- not good\n- not very good\n- extremly sad\n- so saad\n- so sad"
    },
    {
        "intent": "bot_challenge",
        "examples": "- are you a bot?\n- are you a human?\n- am I talking to a bot?\n- am I talking to a human?\n- who are you?\n- can you introduce yourself?"
    }
]

unique_intents = set([d["intent"] for d in yaml_data])

for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx, sheet)

    products = []
    product_list_underscored = []
    for col in df.columns:
        products.append(col)  # original product names with spaces
        product_list_underscored.append(col.replace(" ", "_"))  # product names with underscores
    productList = products[1:]
    productListUnderscored = product_list_underscored[1:]

    # Iterate through the items in the dictionary
    for item in range(df.shape[0]):
        value = str(df['Item'][item]).replace(' ', '_').replace('(', '').replace(')', '').replace(',', '').replace('-', '_')
        for product, product_underscored in zip(productList, productListUnderscored):
            if product == 'LD60':
                examples = "- " + "\n- ".join([
                    f"What is the {value.replace('_', ' ')} for [LG60]({product})?",
                    f"What are the {value.replace('_', ' ')} for [LG60]({product})?",
                ])
            else:
                examples = "- " + "\n- ".join([
                    f"What is the {value.replace('_', ' ')} of {product}?",
                    f"What are the {value.replace('_', ' ')} of {product}?",
                    f"Details about the {value.replace('_', ' ')} of {product}?",
                    f"{value.replace('_', ' ')} of {product}?",
                    f"{product} {value.replace('_', ' ')}?",
                    f"can you tell me about the {value.replace('_', ' ')} of {product}?",
                    f"What is the {value.replace('_', ' ')} required for {product}?",
                    f"{value.replace('_', ' ')} specifications of {product}?",
                    f"Do you have the information about {value.replace('_', ' ')} of {product}?",
                    f"Do you have the information with  {product} {value.replace('_', ' ')}?",
                    f"Do you know about {value.replace('_', ' ')} of {product}?",
                    f"Do you know {product} {value.replace('_', ' ')}?",
                    f"What is the {value.replace('_', ' ')} for {product}?",
                    f"What are the {value.replace('_', ' ')} for {product}?",
                ])
            intent = f"{product_underscored}_{value}"
            if intent not in unique_intents:
                yaml_data.append({"intent": intent, "examples": examples})
                unique_intents.add(intent)

# Write the dictionary to a YAML file
with open('nlu.yml', 'w') as file:
    # Write the first two lines
    file.write('version: "3.1"\n')
    file.write('\n')
    file.write('nlu:\n')
    for data in yaml_data:
        file.write(f'- intent: {data["intent"]}\n')
        file.write(f'  examples: |\n')
        for line in data["examples"].split('\n'):
            file.write(f'    {line}\n')