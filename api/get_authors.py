import requests
import xml.etree.ElementTree as ET
import configparser  # Importamos la librería estándar para .ini/.cfg

def get_authors():
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Get the Goodreads API key from the configuration file
    goodreads_api_key = config.get('goodreads', 'api_key')
    
    # Define the Goodreads API URL for authors
    url = f'https://www.goodreads.com/author_url/{goodreads_api_key}?user_id={goodreads_api_key}'
    
    # Make a GET request to the Goodreads API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.content)
        
        # Extract author information from the XML
        authors = []
        for author in root.findall('.//author'):
            author_info = {
                'id': author.find('id').text,
                'name': author.find('name').text,
                'image_url': author.find('image_url').text,
                'small_image_url': author.find('small_image_url').text,
            }
            authors.append(author_info)
        
        return authors
    else:
        print(f'Error: {response.status_code}')
        return None
