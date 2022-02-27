#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import html
import os
import selenium
import selenium.webdriver.firefox.options
import sentry_sdk
import sqlite3
import time
import twitter
import urllib

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class Twitter2Facebook(object):
    def post(self, text):
        url = 'https://mbasic.facebook.com/'

        home = os.environ['HOME']

        firefox_binary = '/usr/bin/firefox-esr'
        profile_dir = home + '/.mozilla/firefox-esr/selenium'

        options = selenium.webdriver.firefox.options.Options()
        options.headless = True
        options.profile = profile_dir

        with selenium.webdriver.Firefox(firefox_binary=FirefoxBinary(firefox_binary), options=options) as b:
            b.get(url)

            t = b.find_element(by=By.CSS_SELECTOR, value='#mbasic_inline_feed_composer textarea')
            t.send_keys(text)

            btn = b.find_element(by=By.CSS_SELECTOR, value='#mbasic_inline_feed_composer input[value="Post"]')
            btn.click()

    def main(self):
        home = os.environ['HOME']
        f_conf = '{}/.config/twitter2facebook/config.ini'.format(home)
        f_db = '{}/.config/twitter2facebook/entry.sqlite3'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        if 'sentry_sdk_url' in c['default'] and '' != c['default']['sentry_sdk_url']:
            sentry_sdk_url = c['default']['sentry_sdk_url']
            sentry_sdk.init(sentry_sdk_url)

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
            # Generate "text" with unescape (workaround).
            text = html.unescape(status.text)
            for u in status.urls:
                text = text.replace(u.url, u.expanded_url)

            # Skip if it's a reply.
            if status.in_reply_to_user_id:
                continue

            # Skip if it's a retweet.
            if status.retweeted:
                continue

            # Skip if it's from IFTTT and it contains Instagram url.
            try:
                if 'IFTTT' in status.source and 'https://instagr.am/p/' in status.urls[0].expanded_url:
                    continue
            except IndexError:
                pass

            # Generate "url"
            url = 'https://twitter.com/{}/status/{}'.format(urllib.parse.quote(t_user), urllib.parse.quote(status.id_str))

            c = s.cursor()

            c.execute(sql_select, (status.id_str, ))
            if 0 == c.fetchone()[0]:
                content = '{} # {}'.format(text, url)
                print('* content = {}'.format(content))

                print(content)
                self.post(content)

                c.execute(sql_insert, (status.id_str, int(time.time())))
                s.commit()

if __name__ == '__main__':
    Twitter2Facebook().main()
