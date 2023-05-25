# twitter2facebook

Sync Twitter's timeline via RSS Bridge to Facebook's timeline without Facebook API by posting to `mbasic.facebook.com`.

This project is developed and tested in Ubuntu 20.04 so far.

# Pre-installation

Install these packages first:

* firefox-esr
* firefox-esr-geckodriver

In Ubuntu you may need to install via https://launchpad.net/~mozillateam/+archive/ubuntu/ppa this PPA repository.

# Login Facebook

For remote server (e.g. VPS), you may install `tightvncserver` and `icewm` then setup a VNC server afterwards:

    tightvncserver -depth 24 -geometry 1366x768

Once VNC is set, try to create a SSH tunnel (`:1` in X environment is usually `:5901` for TCP) to allow your VNC viewer to access the desktop environment securely:

    ssh -L5901:127.0.0.1:5901 server.example.com

Once you have accessed the desktop environment, open the browser with `-profile` assignment within the terminal:

    firefox-esr -profile ~/.mozilla/firefox-esr/selenium

Then login Facebook and close the browser.  Now you can run `pkill Xtightvnc` to terminate the VNC server.

Please note that Facebook login is somehow strange, therefore sometimes you need to close the browser and open it again to make sure you're really login-ed.

# Installation

Install Python 3 first (I used `pyenv` to run it), then use `pip` to install dependencies:

    pip install -r requirements.txt

Setup Twitter's key & secret in `~/.config/twitter2facebook/config.ini`:

    [default]
    sentry_sdk_url = https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@sentry.io/yyyyyyy
    twitter_rssbridge_jsonfeed_url = https://x

I use Sentry to log error (to notify me when Facebook logout my account), and you can keep empty if you don't want to use Sentry.

Use `sqlite3` to create table schema in `~/.config/twitter2facebook/entry.sqlite3`:

    CREATE TABLE entry (id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id TEXT UNIQUE, created_at INTEGER);

# Crontab

When using pyenv, you might need to specify pyenv to run this script:

    LANG=en_US.UTF-8 ~/.pyenv/shims/python3 /path/twitter2facebook/twitter2facebook.py

# License

See [LICENSE](LICENSE).
