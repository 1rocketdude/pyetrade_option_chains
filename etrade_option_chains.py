#!/usr/local/bin/python

import datetime as dt
import argparse
import pyetrade
import json
import ast
import sys

''' 
    Grab the option expire dates and option chains for the specified symbol.
    Save as a JSON file
    
'''

def option_expire_dates_from_xml(q) -> list:
    """ Take the returned array of XML objects and create a list of dt.dates.
        INPUT: q is the result of the api.get_option_expire_date() call. It is actually a dictionary
                derived from XML from the Etrade API.
        OUTPUT: a list of dt.date values representing the expiration dates
    """
    dates = [dt.date(
            int(this_date["year"]),
            int(this_date["month"]),
            int(this_date["day"]))
            for this_date in q['OptionExpireDateResponse']['ExpirationDate']
        ]
    return dates

def get_all_option_chains(api, underlying_symbol) -> dict:
    """ Returns the all the option chains for the underlying_symbol with expiration_dates
        as the key. This requires two calls, one to get_option_expire_date, then
        to get all the expiration_dates and multiple calls to get_option_chains
        with defaults.

    """
    try:
        q = api.get_option_expire_date(underlying_symbol,resp_format='xml')
        expiration_dates = option_expire_dates_from_xml(q)
    except Exception:
        raise

    rtn = dict()
    for this_expiry_date in expiration_dates:
        q = api.get_option_chains(underlying_symbol, this_expiry_date)
        chains = q['OptionChainResponse']['OptionPair']
        rtn[this_expiry_date] = [i['Put'] for i in chains] + [i['Call'] for i in chains]
    return rtn

def strvals_to_real(q) -> dict:
    ''' given the input dictionary, produce an equivalent with all real numbers converted from
        strings. This should be iterative.
    '''
    rtn = dict()
    for k,v in q.items():
        if isinstance(v,str):
            try:
                rtn[k] = ast.literal_eval(v)
            except:
                rtn[k] = v
        elif isinstance(v,dict):
            rtn[k] = strvals_to_real(v)
        else:
            rtn[k] = v
    return rtn

def alter_quote_dict(quote) -> dict:
    ''' Put the etrade returned quote dict into the form that I'm used to seeing.
        Input form: 'Product' keys
                    'All' keys
    '''
    rtn = strvals_to_real(quote['All'])
    rtn['dateTimeUTC'] = int(quote['dateTimeUTC'])
    for k in ('dateTime','quoteStatus','ahFlag','hasMiniOptions'):
        rtn[k] = quote[k]
    rtn['securityType'] = quote['Product']['securityType']
    rtn['symbol'] = quote['Product']['symbol']
    return rtn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Grab all the option chains for the specified symbol',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('symbol', help='symbol name', type=str)
    args = parser.parse_args()
    
# FILL THESE IN WITH YOUR KEY AND SECRET
    consumer_key = ''
    consumer_secret = ''

    oauth = pyetrade.ETradeOAuth(consumer_key, consumer_secret)
    print(oauth.get_request_token())
    API_token = input('eTrade token: ')
    oauth.get_access_token(API_token)
    api = pyetrade.market.ETradeMarket(consumer_key, consumer_secret,
                                       oauth.access_token['oauth_token'],
                                       oauth.access_token['oauth_token_secret'],
                                       dev=False)

    q = api.get_quote([args.symbol],require_earnings_date=True,resp_format='xml')     # a dict response
    quote = alter_quote_dict(q['QuoteResponse']['QuoteData'])
    
    try:
        chains = get_all_option_chains(api, quote['symbol'])
    except Exception as err:
        print('%s failed get_all_option_chains' % (quote['symbol']))
        print(err)
        sys.exit(1)

# chains has key that is dt.date; convert key to str (JSON needs a string as the key, not a dt.date)
# also convert all values in each ordered dict to floats/ints
    converted_chains = {'quote': quote}     # start of dictionary
    for (expiry_date,chain_list) in chains.items():
        converted_chain_list = [ strvals_to_real(v) for v in chain_list]
        converted_chains[str(expiry_date)] = converted_chain_list               # use str(expiry_date) because eventually this will be saved as JSON

    json_filename = '%s chains %s.json' % (quote['symbol'], str(dt.date.today()))
    with open(json_filename, 'wt') as f:
        json.dump(converted_chains,f)
