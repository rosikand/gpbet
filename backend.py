"""
File: backend.py
------------------
Backend program that orchestrates the entire pipeline. 
"""


import pdb
import sys 
import json
import nhl 
import nba
# import nfl
from openai import OpenAI
import streamlit as st


debug = False


class BackendInterface:
    """
    Backend interface. 
    """

    def __init__(self):

        self.nba = nba.NBAInterface()
        self.nhl = nhl.NHLInterface()
        # self.nfl = nfl.NFLInterface()

        self.openai_api_key = "PASTE YOUR KEY HERE!"
        assert self.openai_api_key is not "PASTE YOUR KEY HERE!"
        self.openai_client = OpenAI(api_key=self.openai_api_key)

        self.chat_history = [{"role": "system", "content": "You are a bot that understands natural language and will be given queries regarding sports analytics and betting questions. Your job is to use the context given by the user and assist them in deciding if the bets proposed are good or not based on the context given. If they provide stats in the context, make sure to include the relevant portions of the stats, in a well formatted manner in your analysis. Additional context, such as news from reddit may also be given, but not all the time. Finally, your response should be concluded with a conclusion that gives the user a yes or no answer if they asked a yes or no type question."}]


    def get_openai_response(self):
        # uses current chat history to generate response. Append current prompt to chat history first. 
        
        completion = self.openai_client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=self.chat_history
        )

        res = completion.choices[0].message.content.strip()

        self.chat_history.append({"role": "assistant", "content": res})

        return res 
    

    def initial_openai_response(self, prompt):
        init_prompt = f"Here are parlays that have worked in the recent past: Daniel Gafford points over 10.5, Nikola Jokic points over 24.5, Nicolas Claxton points over 11.0, Luka Doncic rebounds over 10.0, Mikal Bridges assists over 3.5, Draymond Green over 1.5 blocks + steals, Kyrie Irving under 24.5 points, Domantas Sabonis over 13.5 rebounds. Given the user question and player below, answer the users question based on the context given: \n \n {prompt}"

        prompt_dict = {"role": "user", "content": init_prompt}

        self.chat_history.append(prompt_dict)

        if debug:
            print("first openai response running...")

        res = self.get_openai_response()


        return res

    

    def secondary_openai_response(self, follow_up_user_prompt):

        temp_dict = {"role": "user", "content": follow_up_user_prompt}

        self.chat_history.append(temp_dict)


        if debug:
            print("secondary openai response running...")

        res = self.get_openai_response()

        return res


    def get_prompt(self, user_input, verbose=False):
        # handles user input 

        sport_determined = None 

        nhl_res = self.nhl.find_player_name(user_input)
        nba_res = self.nba.find_player_name(user_input)
        # nfl_res = self.nfl.find_player_name(user_input)

        if len(nhl_res) > 0:
            sport_determined = 'nhl'

        elif len(nba_res) > 0:
            sport_determined = 'nba'

        # elif len(nfl_res) > 0:
            # sport_determined = 'nfl'

        if sport_determined is None:
            return "Invalid player name or sport is out of season. Please try again. We support NHL and NBA players currently."
        
        if sport_determined == 'nba':
            prompt_constructed = self.nba.build_prompt(user_input)
        elif sport_determined == 'nhl':
            prompt_constructed = self.nhl.build_prompt(user_input)
        # elif sport_determined == 'nfl':
            # prompt_constructed = self.nfl.build_prompt(user_input)
        else:
            raise Exception("Invalid sport determined")
        
        if verbose:
            print(prompt_constructed)

        
        return prompt_constructed
    

    def get_result_single(self, user_input, verbose=False):

        constructed_prompt = self.get_prompt(user_input, verbose=verbose)
        
        openai_res = self.initial_openai_response(constructed_prompt)

       # self.chat_history = self.chat_history[1:]  # we don't want to keep the system message in the chat history anymore 

        return openai_res
    

    def get_followup_response(self, prompt):
        return self.secondary_openai_response(prompt)

