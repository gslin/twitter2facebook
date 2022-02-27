# twitter2facebook

Sync Twitter's timeline to Facebook's without Facebook API by posting to `mbasic.facebook.com`.

This project is developed and tested in Ubuntu 18.04 only.

# Pre-installation

Install these packages first:

* chromium-browser
* chromium-chromedriver

And create symbolic link for chromedriver:

    sudo ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver

# Login Facebook

For local/desktop server, you can just open the browser and login Facebook.  For remote server (e.g. VPS), you may install `tightvncserver` and `icewm` to setup VNC:

    tightvncserver -depth 24 -geometry 1366x768

Then SSH into the server and create a tunnel (`:1` is usually `:5901`) to allow your VNC viewer to access the desktop environment:

    ssh -L5901:127.0.0.1:5901 server.example.com

Once you have accessed the desktop environment, just login Facebook, and you can `pkill Xtightvnc` to terminate VNC server.

# Workaround on Chromium

Chromium cannot use cookies in headless mode with latest version (now it's 71), so you need the workaround to install old version, and avoid from upgrading:

    apt-cache showpkg chromium-browser
    sudo apt install \
        chromium-browser=65.0.3325.181-0ubuntu1 \
        chromium-chromedriver=65.0.3325.181-0ubuntu1 \
        chromium-codecs-ffmpeg=65.0.3325.181-0ubuntu1
    sudo apt-mark hold chromium-browser chromium-chromedriver chromium-codecs-ffmpeg

Since this chromium is old, I suggest that just use it for twitter2facebook (so it will only access Facebook site), and not to use it regularly, for security reason.

# Installation

Install Python 3 first (I used `pyenv` to run it), then use `pip` to install dependencies:

    pip install -r requirements.txt

Setup Twitter's key & secret in `~/.config/twitter2facebook/config.ini`:

    [default]
    sentry_sdk_url = https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@sentry.io/yyyyyyy
    twitter_access_token_key = x-x
    twitter_access_token_secret = x
    twitter_consumer_key = x
    twitter_consumer_secret = x
    twitter_username = xxx

I use Sentry to log error (to notify me when Facebook logout my account), and you can keep empty if you don't want to use Sentry.

Use `sqlite3` to create table schema in `~/.config/twitter2facebook/entry.sqlite3`:

    CREATE TABLE entry (id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id TEXT UNIQUE, created_at INTEGER);

# Crontab

When using pyenv, you might need to specify pyenv to run this script:

    LANG=en_US.UTF-8 ~/.pyenv/shims/python3 /path/twitter2facebook/twitter2facebook.py

# License

See [LICENSE](LICENSE).
