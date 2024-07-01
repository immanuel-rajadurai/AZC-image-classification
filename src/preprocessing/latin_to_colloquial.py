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

    def check_latin_name(self, latin_name):
        """ Check if a Latin name exists in the dataset. """
        sanitized_name = self.sanitize_name(latin_name)
        exists = not self.dataset[self.dataset['Latin Name'] == sanitized_name].empty
        return exists


if __name__ == "__main__":
    file_path = ".\\data\\animal_latin_colloquial.csv"
    pipeline = AnimalPipeline(file_path)

    input_list = ["Oak Spider", "Lion"]
    output_list = pipeline.get_latin_names(input_list)
    print(output_list)