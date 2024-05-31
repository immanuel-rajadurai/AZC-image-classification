import pandas as pd
import pyinaturalist as pynat

def checkResponse(response: list, latinName: str) -> bool:
    """
    Check if the response is valid
    """

    if len(response) == 0:
        print("No response for:", latinName)
        return False
    return True

def getTaxanomy(taxa: pynat.Taxon) -> list:
    """
    Get the taxanomy of the animal
    """

    taxanomy = []
    ancestor_ids = taxa.ancestor_ids
    for i in range(1, len(ancestor_ids)-1):
        try:
            ancestorJSON = pynat.get_taxa_by_id(ancestor_ids[i])
            ancestor = pynat.Taxon.from_json_list(ancestorJSON)
            title = ancestor[0].name
            taxanomy.append(title)
        except:
            print("Error in getting taxanomy")
            taxanomy.append(None)
    return taxanomy


def retrieveColloquialName(df: pd.DataFrame) -> None:
    """
    Retrieve the colloquial names of the animals in the dataframe
    """

    i = 4700           # use i =
    while i < 10000:
        latinName = df.loc[i, "Latin Names"]

        # Retrieve the taxa
        response = pynat.get_taxa(q=latinName, rank = ["species"])
        taxa = pynat.Taxon.from_json_list(response)

        # Check if there is a response
        if checkResponse(taxa, latinName):

            colloquialName = taxa[0].preferred_common_name
            # Update the dataframe with the colloquial name
            df.loc[i, "Colloquial Names"] = colloquialName

            taxanomy = getTaxanomy(taxa[0])
            strTaxanomy = ",".join(taxanomy)
            df.loc[i, "Taxanomy"] = strTaxanomy
        else:
            print("No response for", latinName)
            df.loc[i, "Colloquial Names"] = ""

        i+=1
        if i % 100 == 0:
            print(i, "done")
            df.to_csv("data/animal_latin_colloquial.csv",index=False)
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