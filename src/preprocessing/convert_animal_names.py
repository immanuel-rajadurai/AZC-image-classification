import pandas as pd
import pyinaturalist as pynat

# Read the animal names in Latin
df = pd.read_csv("data/animal_latin_colloquial.csv")
print("----------------------Running------------------------------")

# Print the generated response
print("Answering the question...")
for i in range(50):
    latinName = df.loc[i, "Latin Names"]

    # Retrieve the taxa
    response = pynat.get_taxa(q=latinName, rank = ["species"])
    taxa = pynat.Taxon.from_json_list(response)

    # Check if there is a response
    if len(taxa) == 0:
        print("No response for", latinName)
        break

    # Check if there is a colloquial name
    colloquialName = taxa[0].preferred_common_name
    if colloquialName in (None, "", " "):
        print("No colloquial name for", latinName)
        break

    # Update the dataframe with the colloquial name
    df.loc[i, "Colloquial Names"] = colloquialName

print("Done!")
# Save the dataframe
df.to_csv("data/animal_latin_colloquial.csv",index=False)