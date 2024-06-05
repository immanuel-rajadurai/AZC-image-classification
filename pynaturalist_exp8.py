import os
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
from pyinaturalist import get_observations, get_observation_species_counts
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm  # Progress bar

# Replace 'user_id' with desired iNaturalist username
user_id = 'tomasz58'

# Directory to save images. -- can change to wherever you want to save it
save_dir = f'/Users/efe/Documents/AZC Internship/{user_id}_images'

# Function to download and resize image
def download_and_resize_image(url, save_dir, obs_id, max_size=(256, 256)):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.thumbnail(max_size)

        # Ensure the save directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Save the image with a unique name based on the observation ID
        img_name = f"{obs_id}.jpg"
        img_path = os.path.join(save_dir, img_name)
        img.save(img_path)
        return img_path
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return None

# Retry logic with exponential backoff
session = requests.Session()
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor=1
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount('https://', adapter)

try:
    # Fetch observation species counts
    counts = get_observation_species_counts(user_id=user_id, quality_grade='research')


    observation_ids = []
    image_urls = []  
    common_names = []
    scientific_names = []

    # Process species counts for all species
    for species in tqdm(counts['results'], desc='Processing species'):
        taxon_id = species['taxon']['id']

        # Fetch all observations for the current species
        observations = session.get(f'https://api.inaturalist.org/v1/observations?taxon_id={taxon_id}&user_id={user_id}', timeout=10).json()['results']
        
        for observation in observations:
            # Extract and store observation details
            observation_ids.append(observation['id'])

            # Extract and store animal names
            taxon = observation.get('taxon')
            if taxon:
                common_name = taxon.get('preferred_common_name', 'No common name available')
                scientific_name = taxon.get('name', 'No scientific name available')
            else:
                common_name = 'No common name available'
                scientific_name = 'No scientific name available'
            
            common_names.append(common_name)
            scientific_names.append(scientific_name)

            # Extract and store image data
            if 'observation_photos' in observation and observation['observation_photos']:
                photo = observation['observation_photos'][0]['photo']
                image_url = photo['url']
                image_urls.append((image_url, observation['id']))
            else:
                image_urls.append((None, observation['id']))

    # Create a DataFrame with observation details
    data = {
        'Observation ID': observation_ids,
        'Common Name': common_names,
        'Scientific Name': scientific_names,
        'Image URL': [url for url, _ in image_urls]  
    }
    df = pd.DataFrame(data)

    # Save to a CSV file -- again change to wherever you want to store it
    csv_path = f'/Users/efe/Documents/AZC Internship/{user_id}_dataset.csv'
    df.to_csv(csv_path, index=False)

    print(f"Data saved to {csv_path}")

    # Download and resize images, and update DataFrame with image paths
    image_paths = []
    for url, obs_id in tqdm(image_urls, desc='Downloading images'):
        if url:
            image_path = download_and_resize_image(url, save_dir=save_dir, obs_id=obs_id)
            image_paths.append(image_path if image_path else None)
        else:
            image_paths.append(None)

    # Add image paths to the DataFrame
    df['Image Path'] = image_paths

    # Save the updated DataFrame to the CSV again
    df.to_csv(csv_path, index=False)

    print(f"Updated data with image paths saved to {csv_path}")

except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
