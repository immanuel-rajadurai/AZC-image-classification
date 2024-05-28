from pyinaturalist import *

response = get_taxa(q='lumbricus terrestris', rank = ["species"])
print()
print("Answer")
taxa = Taxon.from_json_list(response)

print(taxa[0].preferred_common_name)