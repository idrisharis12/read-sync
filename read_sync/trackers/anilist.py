import requests
from read_sync.library import db

# AniList OAuth2 Implicit Grant URL for CLI apps
CLIENT_ID = "14389" # Mock/public CLI client ID if one exists, or prompt user
AUTH_URL = f"https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&response_type=token"

def login():
    """Prompt user to login and save the access token."""
    print(f"To connect AniList, please visit:\n\n{AUTH_URL}\n")
    token = input("Paste your Access Token here: ").strip()
    
    if not token:
        print("No token provided. Aborting.")
        return False
        
    # We store the token in the SQLite DB (tracker table or a new config table)
    # For simplicity in MVP, we just write it to a local config file
    config_file = db.CONFIG_DIR / "anilist_token.txt"
    with open(config_file, "w") as f:
        f.write(token)
        
    print("✅ AniList successfully authenticated!")
    return True
    
def get_token():
    config_file = db.CONFIG_DIR / "anilist_token.txt"
    if not config_file.exists():
        return None
    with open(config_file, "r") as f:
        return f.read().strip()

def update_progress(media_id: int, progress: int):
    """Scrobble chapter progress to AniList GraphQL API."""
    token = get_token()
    if not token:
        print("AniList is not authenticated.")
        return
        
    query = '''
    mutation ($mediaId: Int, $progress: Int) {
        SaveMediaListEntry (mediaId: $mediaId, progress: $progress) {
            id
            progress
        }
    }
    '''
    variables = {
        'mediaId': media_id,
        'progress': progress
    }
    
    url = 'https://graphql.anilist.co'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    if response.status_code == 200:
        print(f"☁️ Synced Chapter {progress} to AniList.")
    else:
        print(f"Failed to sync to AniList: {response.text}")
