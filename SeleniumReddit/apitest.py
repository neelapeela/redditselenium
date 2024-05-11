import requests

# Define the API endpoint URL
url = 'http://127.0.0.1:5000/analyze'

# Define the search query
search_query = {
    'search_query': 'amazon echo',
    'permissions-policy': 'ch-ua-form-factor'
}

# Send a POST request to the API endpoint
response = requests.post(url, json=search_query)

# Print the response
print(response.json())
