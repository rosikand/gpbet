import datetime
import praw
import re

def scrape_reddit(player_name, n_rows=10, subreddit_name='nba'):
    player_name = player_name.lower()

    user_agent = 'praw_scraper_1.0'

    reddit = praw.Reddit(client_id='Xj8_ZM8C5fS-P-rrqhQtvA',
                         client_secret='28lrVo4MkYysk8Z9EwlqDl2DL-SusA',
                         user_agent=user_agent)

    subreddit_name = subreddit_name

    res = ""
    res += f'---------- Recent news from reddit for {player_name} ----------\n'
    for submission in reddit.subreddit(subreddit_name).search(player_name, sort='top', time_filter='week',
                                                              limit=n_rows):
        temp_res = " "
        temp_res += f"Title: {submission.title}\n"
        # TODO: get content
        # temp_res += f"Content: {submission.selftext}\n"  # too unfiltered
        temp_res += f"Comments: {submission.num_comments}\n"
        temp_res += f"Date: {datetime.datetime.fromtimestamp(submission.created)}\n"
        temp_res += "\n-----------------\n"

        if player_name in temp_res.lower():
            res += temp_res

    res += '-----------------------------------------------\n'

    return res


def find_player_name(user_prompt_text, player_list):
    # TODO: handle complex scandanavian names with accents
    pattern = r'\b(?:' + '|'.join(re.escape(name) for name in player_list) + r')\b'
    # Search for names in the prompt using the regex pattern, ignoring case
    matches = re.findall(pattern, user_prompt_text, flags=re.IGNORECASE)

    # Return names as they originally appear in the names list
    return [name for name in player_list if
            any(re.match(re.escape(name), match, re.IGNORECASE) for match in matches)]
