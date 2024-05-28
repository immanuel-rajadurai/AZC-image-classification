import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Read the animal names in Latin
df = pd.read_csv("data/animal_names_latin.txt", header=None, names = ["Latin Names"])
# Remove the underscores in the names and convert to a dataframe
df = (df["Latin Names"].apply(lambda x: " ".join(x.split("_")))).to_frame()
df["Colloquial Names"] = ""

df.to_csv("data/animal_latin_colloquial.csv",index=False)

# Initialize the OpenAI client with your API key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=API_KEY)  # Replace with your actual API key
 
"""
latinName = df.loc[3, "Latin Names"]
print("Answering the question...")
conversation = [
    {"role": "system", "content": "You are an expert taxonomist, skilled as giving the right colloquial equivalent latin names. When given a name, your responses should be straight to the point, that is you should strictly give the colloquial name only. Eg: When I ask for the colloquial name of: atypoides riversi, your response should be: crab and not River crab. Let's get started!"},
    {"role": "user", "content": f"Give me just the high level colloquial species name, no adjectives, of: {latinName}."}
]

# Generate a chat completion
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=conversation,
    temperature=0
)
print("Done!")
print(completion.choices[0].message.content)
df.loc[3, "Colloquial Names"] = completion.choices[0].message.content

"""
# Print the generated response
print("Answering the question...")
for i in range(10):
    latinName = df.loc[i, "Latin Names"]
    conversation = [
        {"role": "system", "content": "You are an expert taxonomist, skilled as giving the right colloquial equivalent latin names. When given a name, your responses should be straight to the point, that is you should strictly give the colloquial name only. Eg: When I ask for the colloquial name of: atypoides riversi, your response should be: River crab. And for latin names you are uncertain about, just give the high level species name with no adjectives. Let's get started!"},
        {"role": "user", "content": f"Give me just the high level colloquial name of: {latinName}. When given a name, your responses should be straight to the point, that is you should strictly give the colloquial name only. Eg: When I ask for the colloquial name of: atypoides riversi, your response should be: River crab. And for latin names you are uncertain about, just give the high level species name with no adjectives."}
    ]

    # Generate a chat completion
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0
    )
    
    df.loc[i, "Colloquial Names"] = completion.choices[0].message.content
print("Done!")
df.to_csv("data/animal_latin_colloquial.csv",index=False)