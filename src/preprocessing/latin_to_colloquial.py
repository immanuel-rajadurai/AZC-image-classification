import pandas as pd

class AnimalPipeline:
    def __init__(self, dataset_path):
        self.dataset = pd.read_csv(dataset_path)
        self.dataset['Colloquial Name'] = self.dataset['Colloquial Name'].str.strip().str.lower()
        self.dataset['Latin Name'] = self.dataset['Latin Name'].str.strip().str.lower()

    def sanitize_name(self, name):
        """ Sanitize the input name to match the dataset format. """
        return name.strip().lower()  # Convert to lowercase and remove leading/trailing spaces

    def animal_exists(self, colloquial_name):
        """ Check if an animal exists in the dataset by its colloquial name. """
        sanitized_name = self.sanitize_name(colloquial_name)
        exists = not self.dataset[self.dataset['Colloquial Name'] == sanitized_name].empty
        if exists:
            print(f"'{colloquial_name}' exists in the dataset.")
        else:
            print(f"'{colloquial_name}' does not exist in the dataset.")
        return exists

    def get_latin_name(self, colloquial_name):
        """ Get the Latin name for a given colloquial name if it exists. """
        sanitized_name = self.sanitize_name(colloquial_name)
        result = self.dataset[self.dataset['Colloquial Name'] == sanitized_name]
        if not result.empty:
            latin_name = result['Latin Name'].values[0]
            return latin_name
        else:
            print(f"No Latin name found for '{colloquial_name}' in the dataset.")
            return None

    def get_latin_names(self, colloquial_names):
        """ Get a list of Latin names for the given list of colloquial names. """
        latin_names = []
        for name in colloquial_names:
            latin_name = self.get_latin_name(name)
            if latin_name:
                latin_names.append(latin_name)
        return latin_names


file_path = ".\\data\\animal_latin_colloquial.csv"
pipeline = AnimalPipeline(file_path)

  
input_list = ["Oak Spider", "Lion"]

    

   
output_list = pipeline.get_latin_names(input_list)

    
print(output_list)

