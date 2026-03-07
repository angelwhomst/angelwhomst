import os

USER_NAME = os.getenv('USER_NAME', 'angelwhomst')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

HEADERS = {'authorization': f'token {ACCESS_TOKEN}'}

QUERY_COUNT = {
    'user_getter': 0, 
    'follower_getter': 0, 
    'graph_repos_stars': 0, 
    'recursive_loc': 0, 
    'graph_commits': 0, 
    'loc_query': 0
}

OWNER_ID = None
