import nfl_data_py as nfl
import util
import json


class NFLInterface:
    """
    NBA interface.
    """

    def __init__(self):
        self.stats = nfl.import_weekly_data([2024])
        self.all_players_list = self.stats["player_display_name"].unique().tolist()

        assert self.stats is not None
        assert self.all_players_list is not None

    def get_nfl_stats(self, player_name, n_rows=10):
        player_stats = self.stats[self.stats["player_display_name"] == player_name]
        first_n_rows = player_stats.head(n_rows).to_dict(orient='records')
        keys_to_remove = []
        stats_string = '\n'
        stats_string += f'---------- Recent Stats for {player_name} ----------\n'
        for elem in first_n_rows:
            for key in keys_to_remove:
                elem.pop(key, None)
            stats_string += json.dumps(elem)
            stats_string += '\n'
        stats_string += '-----------------------------------------------\n'
        return stats_string

    def find_player_name(self, user_prompt_text):
        return util.find_player_name(user_prompt_text, self.all_players_list)

    def build_prompt(self, user_input, verbose=False):

        names_found = self.find_player_name(user_input)

        if len(names_found) > 1:
            raise Exception("Multiple player names found. Please be more specific")
        elif len(names_found) < 1:
            raise Exception("Invalid player name. Please try again.")

        player_name = names_found[0]

        build_prompt = ""

        build_prompt += f"User question: {user_input}\n"
        build_prompt += f"Player name: {player_name}\n"
        build_prompt += f"context given: \n \n"
        stats_res = self.get_nfl_stats(player_name=player_name, n_rows=10)
        build_prompt += stats_res
        reddit_res = util.scrape_reddit(player_name=player_name, n_rows=10, subreddit_name='nfl')
        build_prompt += reddit_res

        if verbose:
            print(build_prompt)

        return build_prompt

    def test_interface(self):
        example_prompt = "Will Patrick Mahomes score more than 2 TDs next game?"
        res = self.build_prompt(example_prompt, verbose=False)
        print(res)

