# Auto farm script Grepolis

## Description

This is a python script that :
- launches and logins into the game
- auto claims the ressources from villagers town
- you can specify the name of the cities where you want to recruit troops instead, and which troops to recruit
- you can queue building construction automatically
- auto trades with villagers to balance ressources 

## Requirements

Download geckodriver for your OS (https://geckodriver.com/download/). Firefox is required for this version of the bot.\
Unpack the webdriver, make sure it can be executed as a program and copy its path to data/data.txt in the path_to_driver variable.\
Having python installed (unsure which version is required, it works with python 3.12 for me at least). If necessary use a virtual environment (venv for instance) : 
```
python -m venv .venv
source .venv/bin/activate
```
And install required modules :
```
pip install -r requirements.txt
```

## Using

Enter your password and login in data.txt

By default the bot claims resources in all cities. If you don't want it to do so, put the corresponding cities' names in the non_farm_cities list in the file src/variables.py

### Run

```
python src/run.py
```

## Contact
phileasmahuzier@gmail.com