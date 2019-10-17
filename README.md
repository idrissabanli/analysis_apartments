# README #

## You need the following tools to push this project down. ##

- Python 3.5. *
- Virtual Environment Python
You need to load the pb library before downloading it to see the https://www.tecmint.com/install-pip-in-linux/
To install, enter the terminal `pip install virtualenv` command.
- Firefox Browser > 60.0
- Mozilla Geckodriver 0.23.0 https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz


## Method of project convergence ##
1) Run the command line and enter the folder by typing the cd ApartmentScrape.
2) Enter the command `virtualenv venv`. If everything is fine, you'll see "well done".
3) Enter the `source venv/bin/active` command
4) Enter the `pip install -r requirements.txt` command.

The project is being switched off
1) Open the command line in the ApartmentScrape folder
4) Enter the `source venv / bin / active `function.
5) then `python -c 'import analysis; execute analysis.scrape_apartment ("$ {search_address}")'`. here you can write $ {search_address} the address you want. 
For example: `python -c 'import analysis; analysis.scrape_apartment("Scotland, UK")'`
