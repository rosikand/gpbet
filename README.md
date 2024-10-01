# CS 224G (Winter 2024) Project: GPbeT


> This repo holds the code for our CS 224G project called GPbeT: a system that uses LLM's with per-player context to assist in sports betting. 

> Done in collaboration with Govind Chada, Prerit Choudhary, Sina Mohammadi, and Kabir Jolly. 

## Usage 

There are two main ways to use the app: 

- Through the frontend app at https://cs224g-gpbet.streamlit.app/. 
- Through the backend locally through a command-line interface or running the frontend locally: 

To use the app locally: 

- `pip install -r requirements.txt`
- Run backend through CLI: `python3 cli.py`.
- Run frontend locally: `streamlit run frontend.py`


### Daily picks feature 

In addition to the front-end, we have implemented an experimental daily picks feature which live-scrapes bets from prizepicks and provides the user with suggested bets to place. Due to technical limitations (lack of headless web browser scraping) and potential legal issues, we did not deploy this feature to the front-end, but a user can run it by executing `python3 daily.py`. 


### Info on repository structure 

The structure of this repository is as follows: 

- The code for the system is housed in `./`, including the backend and frontend code. 
- `/nbs` and `/playground` contain archived sandbox code that didn't make the final program. 



### Screenshot 

**Frontend**: 


<center>
    <img alt="picture 2" src="https://cdn.jsdelivr.net/gh/minimatest/vscode-images@main/images/4c8e5a6dc5eafdf8bb9fd21861da67b694ec89f803e439e880387f375d63710d.png" width="350" />  
</center>

