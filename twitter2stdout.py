#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os
import sqlite3
import twitter

class Twitter2Stdout(object):
    def main():
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

        for status in sorted(list(t.GetUserTimeline(screen_name=t_user)), key=lambda x: x.id):
            print('* tweet = {}'.format(status))

if __name__ == '__main__':
    Twitter2Stdout.main()
