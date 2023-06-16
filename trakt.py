from typing import Literal, Optional, TypedDict


class ShowIDs(TypedDict):
    trakt: int  # 406221
    slug: str  # "parks-and-recreation"
    tvdb: int  # 1088061
    imdb: str  # "tt1504148"
    tmdb: int  # 397635
    tvrage: Optional[int]  # None


class ShowBare(TypedDict):
    title: str  # "Parks and Recreation"
    year: int  # 2009


class Show(ShowBare, ShowIDs):
    ids: ShowIDs


class ShowRow(TypedDict):
    type: Literal["show"]
    id: int  # ids.trakt, will be treated as primary key.
    title: str  # "Parks and Recreation"
    year: int  # 2009
    trakt_id: int  # 8546
    trakt_slug: str  # "parks-and-recreation"
    tvdb_id: int  # 84912
    imdb_id: str  # "tt1266020"
    tmdb_id: int  # 8592
    tvrage_id: Optional[int]  # 21686


class EpisodeIDs(TypedDict):
    trakt: int  # 406221
    tvdb: int  # 1088061
    imdb: str  # "tt1504148"
    tmdb: int  # 397635
    tvrage: Optional[int]  # None


class EpisodeBare(TypedDict):
    season: int  # 2
    number: int  # 5
    title: str  # "Sister City"


class Episode(EpisodeBare, EpisodeIDs):
    ids: EpisodeIDs


class EpisodeRow(TypedDict):
    type: Literal["episode"]
    id: int  # ids.trakt, will be treated as primary key.
    show_id: int  # Foreign Key
    season: int  # 2
    number: int  # 5
    title: str  # "Sister City"
    trakt_id: int  # 406221
    tvdb_id: int  # 1088061
    imdb_id: str  # "tt1504148"
    tmdb_id: int  # 397635
    tvrage_id: Optional[int]  # None


class CollectedEpisode(Episode):
    collected_at: bool  # "2019-09-24T09:03:22.000Z"
    updated_at: float  # "2019-09-24T09:03:22.000Z"


class CollectedEpisodeRow(TypedDict):
    row_id: str  # Primary Key
    episode_id: int
    collected_at: float  # "2019-09-24T09:03:22.000Z"


class RatedEpisode(Episode):
    id: int  # Primary Key
    episode_id: int
    rating: int  # 9
    rated_at: float  # "2019-09-24T09:03:22.000Z"


class WatchedEpisode(Episode):
    plays: int  # 10
    last_watched_at: float  # "2019-09-24T09:03:22.000Z"
    last_updated_at: float  # "2019-09-24T09:03:22.000Z"


class WatchedEpisodeRow(TypedDict):
    id: int  # Primary Key
    episode_id: int
    total_plays: int  # 10
    last_watched_at: float  # "2019-09-24T09:03:22.000Z"


class HistoryEpisode(Episode, Show):
    id: int
    episode: Episode
    show: Show
    watched_at: float  # "2019-09-24T09:03:22.000Z"
    action: str  # watch
    type: str  # episode


class HistoryEpisodeRow(TypedDict):
    id: int  # Primary Key
    type: Literal["episode"]
    media_id: int
    watched_at: float  # "2019-09-24T09:03:22.000Z"


class MovieIDs(TypedDict):
    trakt: int  # 406221
    slug: str  # "a-quiet-place-2018"
    imdb: str  # "tt1504148"
    tmdb: int  # 397635


class MovieBare(TypedDict):
    title: str  # "A Quiet Place"
    year: int  # 2018


class Movie(MovieBare, MovieIDs):
    ids: MovieIDs


class MovieRow(TypedDict):
    type: Literal["movie"]
    id: int  # ids.trakt, will be treated as primary key.
    title: str  # "A Quiet Place"
    year: int  # 2018
    trakt_id: int  # 293955
    trakt_slug: str  # "a-quiet-place-2018"
    imdb_id: str  # "tt6644200"
    tmdb_id: int  # 447332


class HistoryMovie(Movie):
    id: int
    movie: Movie
    watched_at: float  # "2019-09-24T09:03:22.000Z"
    action: str  # watch
    type: str  # movie


class HistoryMovieRow(TypedDict):
    id: int  # Primary Key
    type: Literal["movie"]
    media_id: int
    watched_at: float  # "2019-09-24T09:03:22.000Z"


class CollectedMovieRow(TypedDict):
    row_id: str  # Primary Key
    movie_id: int
    collected_at: float  # "2019-09-24T09:03:22.000Z"


class CollectedMovie(Movie):
    collected_at: float  # "2019-09-24T09:03:22.000Z"
    updated_at: float  # "2019-09-24T09:03:22.000Z"


class RatedMovie(Movie):
    id: int  # Primary Key
    movie_id: int
    rating: int  # 9
    rated_at: float  # "2019-09-24T09:03:22.000Z"


class WatchedMovie(Movie):
    id: int  # Primary Key
    movie_id: int
    total_plays: int  # 10
    last_watched_at: float  # "2019-09-24T09:03:22.000Z"
