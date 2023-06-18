CREATE TABLE [collected] ( [id] TEXT PRIMARY KEY NOT NULL, [type]
TEXT, [media_id] INTEGER NOT NULL, [collected_at] TEXT NOT NULL,
FOREIGN KEY([media_id]) REFERENCES [movie]([id]), FOREIGN
KEY([media_id]) REFERENCES [episode]([id]) )

CREATE TABLE [episode] ( [type] TEXT DEFAULT 'episode', [id] INTEGER
PRIMARY KEY NOT NULL, [show_id] INTEGER NOT NULL REFERENCES [show]
([id]), [season] INTEGER NOT NULL, [number] INTEGER NOT NULL, [title]
TEXT, [trakt_id] INTEGER NOT NULL, [tvdb_id] INTEGER, [imdb_id] TEXT,
[tmdb_id] INTEGER, [tvrage_id] INTEGER )

CREATE TABLE [movie] ( [type] TEXT DEFAULT 'movie', [id] INTEGER
PRIMARY KEY NOT NULL, [title] TEXT NOT NULL, [year] INTEGER,
[trakt_id] INTEGER NOT NULL, [trakt_slug] INTEGER, [imdb_id] TEXT,
[tmdb_id] INTEGER )

CREATE TABLE [ratings] ( [id] TEXT PRIMARY KEY NOT NULL, [type] TEXT,
[media_id] INTEGER NOT NULL, [rating] INTEGER NOT NULL, [rated_at]
TEXT, FOREIGN KEY([media_id]) REFERENCES [movie]([id]), FOREIGN
KEY([media_id]) REFERENCES [episode]([id]), FOREIGN KEY([media_id])
REFERENCES [show]([id]) )

CREATE TABLE [show] ( [type] TEXT DEFAULT 'show', [id] INTEGER PRIMARY
KEY NOT NULL, [title] TEXT NOT NULL, [year] INTEGER, [trakt_id]
INTEGER NOT NULL, [trakt_slug] TEXT, [tvdb_id] INTEGER, [imdb_id]
TEXT, [tmdb_id] INTEGER, [tvrage_id] INTEGER )

CREATE TABLE [watchlist] ( [id] INTEGER PRIMARY KEY NOT NULL, [type]
TEXT, [media_id] INTEGER NOT NULL, [watchlisted_at] TEXT NOT NULL,
FOREIGN KEY([media_id]) REFERENCES [movie]([id]), FOREIGN
KEY([media_id]) REFERENCES [show]([id]) )

CREATE TABLE [watchlog] ( [id] INTEGER PRIMARY KEY NOT NULL, [type]
TEXT, [media_id] INTEGER NOT NULL, [watched_at] TEXT NOT NULL, FOREIGN
KEY([media_id]) REFERENCES [movie]([id]), FOREIGN KEY([media_id])
REFERENCES [episode]([id]) )