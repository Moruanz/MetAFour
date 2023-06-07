import pandas as pd

# Read the Excel file
xlsx = pd.ExcelFile('./crawleddata.xlsx')

yaml_data = []
unique_rules = set()

for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx, sheet)

    products = []
    for col in df.columns:
        products.append(col)
    productList = products[1:]

    # Iterate through the items in the dictionary
    for item in range(df.shape[0]):
        value = str(df['Item'][item]).replace(' ', '_').replace('(', '').replace(')', '').replace(',', '').replace('-', '_')
        for product in productList:
            rule_name = f"{product}_{value}".replace(' ', '_').replace('(', '').replace(')', '').replace(',', '').replace('-', '_')
            if rule_name not in unique_rules:
                yaml_data.append({
                    "rule": f"return_{rule_name}",
                    "steps": [
                        {"intent": rule_name},
                        {"action": f"utter_{rule_name}"}
                    ]
                })
                unique_rules.add(rule_name)

# Add extra rules
extra_rules = [
    {
        "rule": "Say goodbye anytime the user says goodbye",
        "steps": [
            {"intent": "goodbye"},
            {"action": "utter_goodbye"}
        ]
    },
    {
        "rule": "Say 'I am a bot' anytime the user challenges",
        "steps": [
            {"intent": "bot_challenge"},
            {"action": "utter_iamabot"}
        ]
    },
    {
        "rule": "Greet user",
        "steps": [
            {"intent": "greet"},
            {"action": "utter_greet"}
        ]
    },
    {
        "rule": "Fallback Rule",
        "steps": [
            {"intent": "nlu_fallback"},
            {"action": "action_fallback"}
        ]
    },    
]

yaml_data.extend(extra_rules)

# Write the dictionary to a YAML file
with open('rules.yml', 'w') as file:
    # Write the first two lines
    file.write('version: "3.1"\n')
    file.write("\n")
    file.write('rules:\n')
    file.write("\n")
    # Write the generated content
    for data in yaml_data:
        file.write(f'- rule: {data["rule"]}\n')
        file.write('  steps:\n')
        for step in data["steps"]:
            if "intent" in step:
                file.write(f'  - intent: {step["intent"]}\n')
            else:
                file.write(f'  - action: {step["action"]}\n')
