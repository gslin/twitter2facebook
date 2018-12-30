# twitter2facebook

Sync Twitter's timeline to Facebook's without Facebook API by posting to `mbasic.facebook.com`.

This is developed and tested in Ubuntu 18.04 only.

# Pre-installation

Install these packages first:

* chromium-browser
* chromium-chromedriver

And create symbolic link for chromedriver:

    ln -s ../lib/chromium-browser/chromedriver /usr/bin/chromedriver

Then login Facebook and keep cookies.

# Workaround on Chromium

Chrome cannot use cookies in headless mode with latest version (now it's 71), so you need the workaround to install old version, and avoid from upgrading:

    sudo apt install \
        chromium-browser=65.0.3325.181-0ubuntu1 \
        chromium-chromedriver=65.0.3325.181-0ubuntu1 \
        chromium-codecs-ffmpeg=65.0.3325.181-0ubuntu1
    sudo apt-mark hold chromium-browser chromium-chromedriver chromium-codecs-ffmpeg

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
