import requests
import time

import config
from utils import query_count

def simple_request(func_name, query, variables, max_retries=5, backoff_factor=1.5):
    attempt = 0
    while attempt < max_retries:
        request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables':variables}, headers=config.HEADERS)
        if request.status_code == 200:
            return request
        if request.status_code in (502, 503, 504) or (request.status_code == 429):
            wait = backoff_factor * (2 ** attempt)
            print(f"[simple_request] {func_name} failed with {request.status_code}, retrying in {wait:.1f}s (attempt {attempt+1}/{max_retries})")
            time.sleep(wait)
            attempt += 1
            continue
        raise Exception(func_name, ' has failed with a', request.status_code, request.text, config.QUERY_COUNT)
    raise Exception(func_name, f' failed after {max_retries} retries', request.status_code, request.text, config.QUERY_COUNT)

def user_getter(username):
    query_count('user_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            id
            createdAt
        }
    }'''
    variables = {'login': username}
    request = simple_request(user_getter.__name__, query, variables)
    return {'id': request.json()['data']['user']['id']}, request.json()['data']['user']['createdAt']

def follower_getter(username):
    query_count('follower_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            followers {
                totalCount
            }
        }
    }'''
    request = simple_request(follower_getter.__name__, query, {'login': username})
    return int(request.json()['data']['user']['followers']['totalCount'])

def graph_repos_stars(count_type, owner_affiliation, cursor=None, add_loc=0, del_loc=0):
    query_count('graph_repos_stars')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!, $cursor: String) {
        user(login: $login) {
            repositories(first: 100, after: $cursor, ownerAffiliations: $owner_affiliation) {
                totalCount
                edges {
                    node {
                        ... on Repository {
                            nameWithOwner
                            stargazers {
                                totalCount
                            }
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': config.USER_NAME, 'cursor': cursor}
    request = simple_request(graph_repos_stars.__name__, query, variables)
    if request.status_code == 200:
        if count_type == 'repos':
            return request.json()['data']['user']['repositories']['totalCount']
        elif count_type == 'stars':
            total_stars = 0
            for node in request.json()['data']['user']['repositories']['edges']: 
                total_stars += node['node']['stargazers']['totalCount']
            return total_stars