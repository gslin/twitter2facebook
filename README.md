# twitter2facebook

# Installation

Setup Twitter's key & secret in `~/.config/twitter2facebook/config.ini`:

    [default]
    twitter_access_token_key = x-x
    twitter_access_token_secret = x
    twitter_consumer_key = x
    twitter_consumer_secret = x
    twitter_username = xxx

Use `sqlite3` to create table schema in `~/.config/twitter2facebook/entry.sqlite3`:

    CREATE TABLE entry (id INTEGER PRIMARY KEY AUTOINCREMENT, twitter_id TEXT UNIQUE, created_at INTEGER);

# License

See [LICENSE](LICENSE).
