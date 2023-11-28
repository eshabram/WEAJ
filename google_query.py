import requests

# Your Google Custom Search Engine (CSE) API key
api_key = ' AIzaSyCnaNHhVk7mCTB4r_V3ACbkOazY05B4uF4 '

# Your CSE ID
cse_id = '97ea8e86608a74b0a'

# Query for image search
query = 'car'  # Modify this query as needed

# URL for the Google Custom Search JSON API
url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}&searchType=image'

# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract and print image URLs from the results
    for item in data.get('items', []):
        image_url = item.get('link', '')
        print(image_url)
else:
    print('API request error!')
