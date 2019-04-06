import requests
import json
import random
import datetime
import time
import tweepy
import configparser

dict = {
    "api": "https://api.datamuse.com",
    "parameter": [
        "sl",
        "rel_rhy",
        "rel_nry",
        "hom",
        "sl"
    ],
    "training_data": [
        "tentacion",
        "tentation",
        "shin",
        "temptation",
        "nation",
        "akin",
        "men",
        "inauguration",
        "probation",
        "raven",
        "amen",
        "roman",
        "flavor",
        "grinch",
        "freight",
        "name",
        "security"
    ]
}

def wait_until(h):
    t = datetime.datetime.today()
    print('printed at: {}'.format(t))
    future = datetime.datetime(t.year,t.month, t.day, h, 0)
    if t.hour >= h:
        future += datetime.timedelta(days=1)
    print('next at: {}'.format(future))
    time.sleep((future-t).seconds)

def get_related_word(api, param, word):
    raw_response = requests.get('{}/words?{}={}'.format(api, param, word)).json()

    try:
        rel_word = random.choice(raw_response)["word"]
    except:
        rel_word = ""

    return rel_word

def authenticate(key, secret, token, tok_secret):
    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(token, tok_secret)
    api = tweepy.API(auth)

    print(api.me().name)
    
    return api


def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    api = authenticate(config['DEFAULT']['consumer_key'],
                       config['DEFAULT']['consumer_secret'],
                       config['DEFAULT']['access_token'],
                       config['DEFAULT']['access_token_secret'])

    cons_fails = 0

    while True:
 
        response = get_related_word(dict["api"],
                                    random.choice(dict["parameter"]),
                                    random.choice(dict["training_data"]))
        if response == "":
            cons_fails += 1
            print("failed {} times".format(cons_fails))
            time.sleep(5)
            continue
        else:
            cons_fails = 0
            tweet = "XXX" + response.capitalize()
            api.update_status(tweet)
            print(tweet)
            wait_until(12)


        if cons_fails > 10:
            break


if __name__ == "__main__":
    main()