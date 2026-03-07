import datetime

import config
from utils import daily_readme, perf_counter, formatter
from github_api import user_getter, follower_getter, graph_repos_stars
from loc_cache import loc_query, commit_counter
from svg_renderer import svg_overwrite

if __name__ == '__main__':
    print('Calculation times:')
    
    user_data, user_time = perf_counter(user_getter, config.USER_NAME)
    config.OWNER_ID, acc_date = user_data
    formatter('account data', user_time)
    
    # 2. Age/Uptime Calculation (Update this date to your actual birthday)
    age_data, age_time = perf_counter(daily_readme, datetime.datetime(2004, 8, 10))
    formatter('age calculation', age_time)
    
    total_loc, loc_time = perf_counter(loc_query, ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'], 7)
    formatter('LOC (cached)', loc_time) if total_loc[-1] else formatter('LOC (no cache)', loc_time)
    commit_data, commit_time = perf_counter(commit_counter, 7)
    
    star_data, star_time = perf_counter(graph_repos_stars, 'stars', ['OWNER'])
    repo_data, repo_time = perf_counter(graph_repos_stars, 'repos', ['OWNER'])
    contrib_data, contrib_time = perf_counter(graph_repos_stars, 'repos', ['OWNER', 'COLLABORATOR', 'ORGANIZATION_MEMBER'])
    
    follower_data, follower_time = perf_counter(follower_getter, config.USER_NAME)

    for index in range(len(total_loc)-1): 
        total_loc[index] = '{:,}'.format(total_loc[index]) 

    svg_overwrite('dark_mode.svg', age_data, commit_data, star_data, repo_data, contrib_data, total_loc[:-1])
    svg_overwrite('light_mode.svg', age_data, commit_data, star_data, repo_data, contrib_data, total_loc[:-1])

    print('\033[F\033[F\033[F\033[F\033[F\033[F\033[F\033[F',
        '{:<21}'.format('Total function time:'), '{:>11}'.format('%.4f' % (user_time + age_time + loc_time + commit_time + star_time + repo_time + contrib_time)),
        ' s \033[E\033[E\033[E\033[E\033[E\033[E\033[E\033[E', sep='')

    print('Total GitHub GraphQL API calls:', '{:>3}'.format(sum(config.QUERY_COUNT.values())))
    for funct_name, count in config.QUERY_COUNT.items(): 
        print('{:<28}'.format('   ' + funct_name + ':'), '{:>6}'.format(count))