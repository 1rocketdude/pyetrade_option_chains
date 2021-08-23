# pyetrade_option_chains

Exemplar code to download all option chains for a symbol using pyetrade (V1 Etrade API).
This simple example code demonstrates how to grab credentials and download all the option chains
from a single symbol and convert the etrade API response to common python dictionaries and lists.

Remember to fill in your personalized values for consumer_key and consumer_secret.
You need to request user keys for the "production environment" from Etrade. This is a 3-5 day process.
The "development environment" keys are only useful if you're developing code and want to test against a
dummy environment. See [E*TRADE's Getting Started guide](https://developer.etrade.com/getting-started).

Pyetrade has a number of pretty standard dependencies, including requests, requests_oauthlib, xmltodict

## Install

```shell
git clone https://github.com/1rocketdude/pyetrade_option_chains.git
cd pyetrade_option_chains
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

To download all the option chains for AAPL and save into a JSON file named
"AAPL_chains_YYYYMMDD-HHMMSS.json":

* Modify `KEYS` etrade_option_chains.py
* Run `./etrade_option_chains.py aapl` or `./etrade_option_chains.py --sandbox aapl`

**Note**: E*TRADE's sandbox doesn't actually produce correct option chains so
this will return an error. The sandbox is still useful for debugging e.g. the
OAuth stuff.

The JSON file will have one key called 'quote' which will contain the underlying
data. Then each remaining key is a str representing the expiration date. The
value will contain a list of all puts and calls as dictionaries.

To recover the python object, use something like:

```python
import json
with open('AAPL_chains_YYYYMMDD-HHMMSS.json', 'rt') as f: aapl = json.load(f)
```
