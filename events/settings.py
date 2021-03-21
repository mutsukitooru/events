from datetime import timedelta


CHECK_EVERY = timedelta(minutes=5)

RSS_CONFIGURE = {
    "release": "http://feeds.feedburner.com/crunchyroll/rss/anime",
    "news": "http://feeds.feedburner.com/crunchyroll/animenews",
}

DATABASE_CONFIGURE = {
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": 5432,
}