# pyetrade_option_chains
exemplar code to download all option chains for a symbol using pyetrade (V1 Etrade API).
This simple example code demonstrates how to grab credentials and download all the option chains
from a single symbol and convert the etrade API response to common python dictionaries and lists.

Remember to fill in your personalized values for consumer_key and consumer_secret.
You need to request user keys for the "production environment" from Etrade. This is a 3-5 day process.
The "development environment" keys are only useful if you're developing code and want to test against a
dummy environment.

Pyetrade has a number of pretty standard dependencies, including requests, requests_oauthlib, xmltodict

INSTALL:

    git clone https://github.com/jessecooper/pyetrade.git
    cd pyetrade
    git checkout dev
    pip install --user setup.py

    cd ..
    git clone https://github.com/1rocketdude/pyetrade_option_chains.git

USAGE: to download all the option chains for AAPL and save into a JSON file named AAPL-YYYY-MM-DD.json
    cd pyetrade_option_chains

    modify consumer_key and consumer_secret in etrade_option_chains.py
    pyetrade_option_chains.py aapl

    The JSON file will have one key called 'quote' which will contain the underlying data.
    Then each remaining key is a str representing the expiration date. The value will contain a list of all puts and calls
    as dictionaries.

    To recover the python object, use something like:
        import json
        with open('AAPL-YYYY-MM-DD.json','rt') as f: aapl=json.load(f)
        
