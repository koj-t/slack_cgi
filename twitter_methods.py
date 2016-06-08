#!/home/kojima/cgi/bin/python
# coding:utf-8
from requests_oauthlib import OAuth1Session
import json

# 各種認証キー読み込み
twitter_config_path = "../../twitter_config.json"
with open(twitter_config_path) as f:
    tw_cfg = json.load(f)

CK = tw_cfg["CK"]
CS = tw_cfg["CS"]
AT = tw_cfg["AT"]
AS = tw_cfg["AS"]
twitter = OAuth1Session(CK, CS, AT, AS)


# DMの投稿
def post_dm(text, to_user_name):
    url = "https://api.twitter.com/1.1/direct_messages/new.json"
    params = {"text": text, "screen_name": to_user_name}
    res = twitter.post(url, params=params)
    if res.status_code == 200:
        print ("OK! DM Post Done")
        fp = open("log", "a")
        fp.writelines(text+"\n")
        fp.close
    else:
        print("dm post error: %d" % res.status_code)


# TLの取得
def get_timeline(count=20):
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    params = {"count": count}
    res = twitter.get(url, params=params)
    if res.status_code == 200:
        timeline = json.loads(res.text)
        for tweet in timeline:
            print (tweet["user"]["screen_name"]+":\n\t"+tweet["text"])
    else:
        print ("get timeline error: %d" % res.status_code)


# ツイート
def post_tweet(text, mention=""):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    if mention == "":
        mention = "@koj_sandbox "
    else:
        mention = "@" + mention + " "
    params = {"status": mention+text}
    res = twitter.post(url, params=params)
    if res.status_code == 200:
        print ("OK! Tweet Post Done")
        fp = open("log", "a")
        fp.writelines(text+"\n")
        fp.close
    else:
        print ("tweet post error: %d" % res.status_code)


# DMの取得
def get_dm(count=10, silent=False):
    url = "https://api.twitter.com/1.1/direct_messages.json"
    params = {"count": count}
    res = twitter.get(url, params=params)
    if res.status_code == 200:
        dm_list = json.loads(res.text)
        if silent:
            return dm_list[0]["text"]
        for dm in dm_list:
            print (dm["sender"]["screen_name"]+"->" +
                   dm["recipient"]["screen_name"]+":\n\t"+dm["text"])


# TLのストリーム表示
def show_tl_stream():
    import twitter
    auth = twitter.OAuth(AT, AS, CK, CS)
    t_stream = twitter.TwitterStream(
        auth=auth,
        domain="userstream.twitter.com")
    for msg in t_stream.user():
        if "text" in msg:
            print (msg["user"]["screen_name"]+":"+msg["text"]+"\n")


# 検索
def search_tweets(word="進捗", count=10):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {"q": word, "lang": "ja", "count": count}
    res = twitter.get(url, params=params)
    if res.status_code == 200:
        results = json.loads(res.text)["statuses"]
        for result in results:
            print ("@"+result["user"]["screen_name"]+":\n"+result["text"]+"\n")


# 検索のストリーム表示
def search_stream(word="進捗"):
    import twitter
    auth = twitter.OAuth(AT, AS, CK, CS)
    t_stream = twitter.TwitterStream(
        auth=auth,
        domain="stream.twitter.com")
    for msg in t_stream.statuses.filter(track=word):
        if "text" in msg:
            print ("@"+msg["user"]["screen_name"]+":\n"+msg["text"]+"\n")

if __name__ == "__main__":
    print "Content-Type: text/html\n"
    get_dm(1)
