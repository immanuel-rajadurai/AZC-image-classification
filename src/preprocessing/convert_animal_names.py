import pandas as pd
import pyinaturalist as pynat


def retrieveColloquialName(df: pd.DataFrame) -> None:
    """
    Retrieve the colloquial names of the animals in the dataframe
    """

    i = 0           # use i = 1000
    while i < 10000:
        latinName = df.loc[i, "Latin Names"]

        # Retrieve the taxa
        response = pynat.get_taxa(q=latinName, rank = ["species"])
        taxa = pynat.Taxon.from_json_list(response)

        # Check if there is a response
        if len(taxa) == 0:
            print("No response for", latinName)
            df.loc[i, "Colloquial Names"] = "Species not found"
            continue

        # Check if there is a colloquial name
        colloquialName = taxa[0].preferred_common_name
        if colloquialName in (None, "", " "):
            print("No colloquial name for", latinName)
            df.loc[i, "Colloquial Names"] = "No colloquial name"
        else:
            # Update the dataframe with the colloquial name
            df.loc[i, "Colloquial Names"] = colloquialName

        i+=1
        if i % 100 == 0:
            print(i, "done")
            ask = input("Do you want to continue? (y/n)")
            ask = ask.lower()
            if ask == "n":
                break

if __name__ == "__main__":

    # Read the animal names in Latin
    df = pd.read_csv("data/animal_latin_colloquial.csv")
    print("----------------------Running------------------------------")

    # Retrieve the colloquial names of the animals
    retrieveColloquialName(df)
    # Print the generated response
    print("Answering the question...")


    print("Done!")
    # Save the dataframe
    df.to_csv("data/animal_latin_colloquial.csv",index=False)