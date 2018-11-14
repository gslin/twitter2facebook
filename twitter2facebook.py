#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os
import selenium
import selenium.webdriver.chrome.options
import sqlite3
import time
import twitter
import urllib

def post(text):
    url = 'https://mbasic.facebook.com/'

    home = os.environ['HOME']

    chrome_options = selenium.webdriver.chrome.options.Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--user-data-dir={}/.config/chromium'.format(home))
    chrome_options.binary_location = '/usr/bin/chromium-browser'

    with selenium.webdriver.Chrome(options=chrome_options) as b:
        b.get(url)

        t = b.find_element_by_css_selector('#mbasic_inline_feed_composer textarea')
        t.send_keys(text)

        btn = b.find_element_by_css_selector('#mbasic_inline_feed_composer input[value="Post"]')
        btn.click()

def work():
    home = os.environ['HOME']
    f_conf = '{}/.config/twitter2facebook/config.ini'.format(home)
    f_db = '{}/.config/twitter2facebook/entry.sqlite3'.format(home)

    c = configparser.ConfigParser()
    c.read(f_conf)

    t_ak = c['default']['twitter_access_token_key']
    t_as = c['default']['twitter_access_token_secret']
    t_ck = c['default']['twitter_consumer_key']
    t_cs = c['default']['twitter_consumer_secret']
    t_user = c['default']['twitter_username']
    t = twitter.Api(access_token_key=t_ak, access_token_secret=t_as, consumer_key=t_ck, consumer_secret=t_cs)

    s = sqlite3.connect(f_db)

    sql_insert = 'INSERT INTO entry (twitter_id, created_at) VALUES (?, ?);'
    sql_select = 'SELECT COUNT(*) FROM entry WHERE twitter_id = ?;'

    for status in sorted(list(t.GetUserTimeline(screen_name=t_user)), key=lambda x: x.id):
        # Generate "text"
        text = status.text
        for u in status.urls:
            text = text.replace(u.url, u.expanded_url)

        # Skeip if it's a reply.
        if status.in_reply_to_user_id:
            continue

        # Skip if it's a retweet.
        if status.retweeted:
            continue

        # Generate "url"
        url = 'https://twitter.com/{}/status/{}'.format(urllib.parse.quote(t_user), urllib.parse.quote(status.id_str))

        c = s.cursor()

        c.execute(sql_select, (status.id_str, ))
        if 0 == c.fetchone()[0]:
            content = '{} # {}'.format(text, url)
            print('* content = {}'.format(content))

            print(content)
            post(content)

            c.execute(sql_insert, (status.id_str, int(time.time())))
            s.commit()

if __name__ == '__main__':
    work()
