import requests
import json

# Replace these values with your own iCloud API credentials
ICLOUD_API_CLIENT_ID = "YOUR_CLIENT_ID"
ICLOUD_API_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
ICLOUD_API_REDIRECT_URI = "YOUR_REDIRECT_URI"

# URL for the iCloud API's OAuth 2.0 authentication endpoint
ICLOUD_API_AUTH_URL = "https://appleid.apple.com/auth/token"

# URL for the iCloud API's asset collections endpoint
ICLOUD_API_ASSET_COLLECTIONS_URL = "https://api.icloud.com/v1/assets/collections"

# URL for the iCloud API's assets endpoint
ICLOUD_API_ASSETS_URL = "https://api.icloud.com/v1/assets"

# URL for the iCloud API's asset URLs endpoint
ICLOUD_API_ASSET_URLS_URL = "https://api.icloud.com/v1/assets/urls"

# OAuth 2.0 parameters for the authentication request
auth_params = {
    "client_id": ICLOUD_API_CLIENT_ID,
    "client_secret": ICLOUD_API_CLIENT_SECRET,
    "redirect_uri": ICLOUD_API_REDIRECT_URI,
    "grant_type": "authorization_code",
    "code": "YOUR_AUTHORIZATION_CODE",  # Replace this with the authorization code obtained during the OAuth 2.0 flow
}

# Send the authentication request
auth_response = requests.post(ICLOUD_API_AUTH_URL, data=auth_params)

# If the request was successful, extract the access token from the response
if auth_response.status_code == 200:
    auth_response_json = auth_response.json()
    access_token = auth_response_json["access_token"]

# Set the authorization header for subsequent API requests
headers = {
    "Authorization": f"Bearer {access_token}",
}

# Send a request to the iCloud API's asset collections endpoint to retrieve a list of asset collections
asset_collections_response = requests.get(ICLOUD_API_ASSET_COLLECTIONS_URL, headers=headers)

# If the request was successful, extract the list of asset collections from the response
if asset_collections_response.status_code == 200:
    asset_collections_response_json = asset_collections_response.json()
    asset_collections = asset_collections_response_json["collections"]

# Iterate through the list of asset collections
for asset_collection in asset_collections:
    # Extract the collection ID from the asset collection
    collection_id = asset_collection["id"]

    # Send a request to the iCloud API's assets endpoint to retrieve a list of assets in the collection
    assets_response = requests.get(f"{ICLOUD_API_ASSETS_URL}?collectionId={collection_id}&contentTypes=all", headers=headers)

    # If the request was successful, extract the list of assets from the response
    if assets_response.status_code == 200:
        assets_response_json = assets_response.json()
        assets = assets_response_json["data"]

        # Iterate through the list of assets
        for asset in assets:
            # Extract the asset ID from the asset
            asset_id = asset["id"]

            # Send a request to the iCloud API's asset URLs endpoint to retrieve the share URL for the asset
            asset_urls_response = requests.get(f"{ICLOUD_API_ASSET_URLS_URL}/{asset_id}", headers=headers)

            # If the request was successful, extract the share URL from the response
            if asset_urls_response.status_code == 200:
                asset_urls_response_json = asset_urls_response.json()
                share_url = asset_urls_response_json["urls"]["public"]

            # Print the share URL for the asset
            print(f"Share URL: {share_url}")
