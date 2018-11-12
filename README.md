# twitter2facebook

This is developed and tested in Ubuntu 18.04 only.

# Pre-installation

Install these packages first:

* chromium-browser
* chromium-chromedriver

And create symbolic link for chromedriver:

    ln -s ../lib/chromium-browser/chromedriver /usr/bin/chromedriver

# Installation

Install Python 3 first (I used `pyenv` to run it), then use `pip` to install dependencies:

    pip install -r requirements.txt

Setup Twitter's key & secret in `~/.config/twitter2facebook/config.ini`:

    [default]
    twitter_access_token_key = x-x
    twitter_access_token_secret = x
    twitter_consumer_key = x
    twitter_consumer_secret = x
    twitter_username = xxx

Use `sqlite3` to create table schema in `~/.config/twitter2facebook/entry.sqlite3`:

    CREATE TABLE entry (id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id TEXT UNIQUE, created_at INTEGER);

# Crontab

When using pyenv, you might need to specify pyenv to run this script:

    LANG=en_US.UTF-8 ~/.pyenv/shims/python3 /path/twitter2facebook/twitter2facebook.py

# License

See [LICENSE](LICENSE).
