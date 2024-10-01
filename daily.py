"""
File: daily.py
------------------
Interface for scraping daily prizepicks bets and suggesting bets to the user. 
Will be implemented as a button to press. 
"""

import pdb
import sys 
import json
import nhl 
import nba
import time 
# import nfl
from openai import OpenAI
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
import pdb




class DailyInterface:
    """
    daily interface. 
    """

    def __init__(self):

        self.nba = nba.NBAInterface()
        self.nhl = nhl.NHLInterface()
        # self.nfl = nfl.NFLInterface()

        self.openai_api_key = "PASTE YOUR KEY HERE!"
        assert self.openai_api_key is not "PASTE YOUR KEY HERE!"



    def openai_response(self, messages):
        
        client = OpenAI(api_key=self.openai_api_key)

        # final_prompt = f"Given the user question and player below, answer the users question based on the context given: \n \n {prompt}"


        completion = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages
        )

        return completion.choices[0].message.content.strip()
    

    def get_prompt(self, user_input, verbose=False, get_news=True):
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
            return "Invalid player name. Please try again. We support NHL and NBA players currently."
        
        if sport_determined == 'nba':
            prompt_constructed = self.nba.build_prompt(user_input, get_news=get_news)
        elif sport_determined == 'nhl':
            prompt_constructed = self.nhl.build_prompt(user_input, get_news=get_news)
        # elif sport_determined == 'nfl':
            # prompt_constructed = self.nfl.build_prompt(user_input)
        else:
            raise Exception("Invalid sport determined")
        
        if verbose:
            print(prompt_constructed)

        
        return prompt_constructed

    
    def get_result(self, user_input, verbose=False):

        constructed_prompt = self.get_prompt(user_input, verbose=verbose)
        
        openai_res = self.openai_response(constructed_prompt)
        self.append_to_history(user_input, openai_res)

        return openai_res
    


    def get_daily_lines(self, max_lines_per_category=10):
        return self.scrape_lines(max_lines_per_category)


    def get_daily_picks(self, max_lines_per_category=10):

        sample_list = self.get_daily_lines(max_lines_per_category=max_lines_per_category)

        messages = [{"role": "system",
                          "content": "You are a bot that understands natural language and will be given queries regarding sports analytics and betting questions. Your job is to use the context given by the user and assist them in deciding if the bets proposed are good or not based on the context given. If they provide stats in the context, make sure to include the relevant portions of the stats, in a well formatted manner in your analysis. Additional context, such as news from reddit may also be given. Here are parlays that have worked in the recent past: Daniel Gafford points over 10.5, Nikola Jokic points over 24.5, Nicolas Claxton points over 11.0, Luka Doncic rebounds over 10.0, Mikal Bridges assists over 3.5, Draymond Green over 1.5 blocks + steals, Kyrie Irving under 24.5 points, Domantas Sabonis over 13.5 rebounds. Finally, your response should be concluded with a conclusion that gives the user a yes or no answer if they asked a yes or no type question."}]

        for betline in tqdm(sample_list):
            # prompt_ = "Look at the bet line below and analyze whether or not the bet is good given the context: \n" + betline
            prompt_ = betline
            curr_prompt = self.get_prompt(prompt_, get_news=False)
            # curr_prompt = "-----------------------------------------------\n" + curr_prompt
            messages.append({"role": "user", "content": curr_prompt})

        # master_prompt_temp = "-----------------------------------------------\n".join(prompts)


        # master_prompt_prefix = "Out of the following bet lines, determine which bets are good based on the context given (the last part of your answer should be bullet points stating the bet line and a yes or no answer): \n"
        master_prompt_suffix = "Out of the above bet lines, determine which bets are good based on the context given (conclude your answer by writing bullet points about the good bets only out of the ones provided, and for each bullet point in this conclusion, state a tldr): \n"
        messages.append({"role": "user", "content": master_prompt_suffix})
        res = self.openai_response(messages)
        return res


    def scrape_lines(self, max_lines_per_category=10):
        
        driver = uc.Chrome()
        # path = '/Users/rosikand/Desktop/cs224g-proj/core/driver/chromedriver'
        # driver = webdriver.Chrome(service=Service(path))


        driver.get("https://app.prizepicks.com/")
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[3]/div[3]/div/div/button")))
        driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/div/button").click()
        time.sleep(2)



        final_lines = []

        # driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div/main/div/nav/div/div[3]").click()
        driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='NBA']").click()
        time.sleep(2)


        stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

        categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')

        for category in tqdm(categories):
            if "(Combo)" in category:
                continue


            driver.find_element(By.XPATH, f"//div[text()='{category}']").click()

            player_projs = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div/main/div/div[2]/div[1]/div[3]")))


            betlines_all = player_projs[0].text

            betlines_all = betlines_all.split("\nMORE")

            betlines_max = betlines_all[:max_lines_per_category]

            for bet in betlines_max:
                # line = bet.split("\n", 1)[1]
                # line = line.rsplit("\n", 1)[0]
                bet_ = bet[1:-5]
                final_lines.append(bet_)
                

        # get all but last
        final_lines = final_lines[:-1]

        driver.quit()

        return final_lines




inter = DailyInterface()
res = inter.get_daily_picks()
print(res)
