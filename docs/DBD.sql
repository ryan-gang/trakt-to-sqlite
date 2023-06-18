-- Code for creating database diagram @ https://app.quickdatabasediagrams.com/#/.
-- See accompanying svg image.
show
--
id PK int
type string DEFAULT='show'
title string
year int NULL
trakt_id int
trakt_slug string NULL
tvdb_id int NULL
imdb_id string NULL
tmdb_id int NULL
tvrage_id int NULL

episode
--
id PK int
type string DEFAULT='episode'
show_id int FK >- show.id

movie
--
id PK int
type string DEFAULT='movie'
title string
year int NULL
trakt_id int
trakt_slug int NULL
imdb_id string NULL
tmdb_id int NULL

collected
--
id PK string
type string NULL
media_id int FK >- movie.id FK >- episode.id
collected_at string

ratings
--
id PK string
type string NULL
media_id int FK >- movie.id FK >- episode.id FK >- show.id
rating int
rated_at string NULL

watchlist
--
id PK int
type string NULL
media_id int FK >- movie.id FK >- show.id
watchlisted_at string

watchlog
--
id PK int
type string NULL
media_id int FK >- movie.id FK >- episode.id
watched_at string

