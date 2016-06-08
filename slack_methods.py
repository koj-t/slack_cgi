#!/home/kojima/cgi/bin/python
# -*- coding: utf-8 -*-
import requests as req
import json

config_path = "config.json"
url_base = "https://slack.com/api"

with open(config_path) as f:
    cfg = json.load(f)


def post_message(text, channel="_koj"):
    payload = {
        "token": cfg["token"],
        "channel": channel,
        "text": text
    }
    url = url_base + "/chat.postMessage"
    req.post(url, data=payload)


def get_message(channel="general", count=5):
    payload = {
        "token": cfg["token"],
        "channel": detect_channel_id(channel),
        "count": count
    }
    url = url_base + "/channels.history"
    data = json.loads(req.post(url, data=payload).text)
    messages = data['messages']
    user = detect_user(messages[0]['user'])
    text = messages[0]['text']
    return text+":"+user


def get_channel_list():
    payload = {
        "token": cfg["token"]
    }
    url = url_base + "/channels.list"
    data = req.post(url, data=payload)
    return json.loads(data.text)['channels']


def detect_channel_id(channel):
    channels = get_channel_list()
    channel_id = [x['id'] for x in channels if x['name'] == channel]
    return channel_id if len(channel_id) == 1 else ""


def detect_user(user_id):
    params = {"token": cfg["token"], "user": user_id}
    res = req.post("https://slack.com/api/users.info", params=params)
    if res.status_code == 200:
        return res.json()["user"]["name"]
    else:
        print ("detect_user error!:"+res)
        return "detect_user error"
