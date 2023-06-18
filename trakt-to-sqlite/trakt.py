from typing import Literal, Optional, TypedDict


class Genre(TypedDict):
    name: str
    slug: str


class MediaGenreRow(Genre):
    media_id: int


class ShowBare(TypedDict):
    title: str  # "Parks and Recreation"
    year: int  # 2009


class ShowIDs(TypedDict):
    trakt: int  # 406221
    slug: str  # "parks-and-recreation"
    tvdb: int  # 1088061
    imdb: str  # "tt1504148"
    tmdb: int  # 397635
    tvrage: Optional[int]  # None


class Show(ShowBare, ShowIDs):
    ids: ShowIDs  # type: ignore


class ExtendedShow(Show):
    overview: str
    first_aired: str
    airs: dict[str, str]
    runtime: int
    certification: str
    network: str
    country: str
    trailer: str
    homepage: str
    status: str
    rating: float
    votes: int
    comment_count: int
    updated_at: str
    language: str
    available_translations: list[str]
    genres: list[Genre]
    aired_episodes: int


class EpisodeBare(TypedDict):
    season: int  # 2
    number: int  # 5
    title: str  # "Sister City"


class EpisodeIDs(TypedDict):
    trakt: int  # 406221
    tvdb: int  # 1088061
    imdb: str  # "tt1504148"
    tmdb: int  # 397635
    tvrage: Optional[int]  # None


class Episode(EpisodeBare, EpisodeIDs):
    ids: EpisodeIDs


class ExtendedEpisode(Episode):
    number_abs: int  # What is this ?
    overview: str
    rating: float
    votes: int
    comment_count: int
    first_aired: str
    updated_at: str
    available_translations: list[str]
    runtime: int


# A season of episodes.
class SeasonBare(TypedDict):
    number: int  # Season number


class SeasonIDs(TypedDict):
    trakt: int  # 406221
    tvdb: int  # 1088061
    tmdb: int  # 397635
    tvrage: Optional[int]  # None


class Season(SeasonBare, SeasonIDs, Episode):
    episodes: list[Episode]


class EpisodeSearch(Episode, Show):  # type: ignore
    type: Literal["episode"]
    score: int
    episode: Episode
    show: Show


class MovieBare(TypedDict):
    title: str  # "A Quiet Place"
    year: int  # 2018


class MovieIDs(TypedDict):
    trakt: int  # 406221
    slug: str  # "a-quiet-place-2018"
    imdb: str  # "tt1504148"
    tmdb: int  # 397635


class Movie(MovieBare, MovieIDs):
    ids: MovieIDs


class ExtendedMovie(Movie):
    tagline: str
    overview: str
    released: str
    runtime: int
    country: str
    trailer: str
    homepage: str
    status: str
    rating: float
    votes: int
    comment_count: int
    updated_at: str
    language: str
    available_translations: list[str]
    genres: list[Genre]
    certification: str


class CollectedEpisode(Episode):
    collected_at: str  # "2019-09-24T09:03:22.000Z"
    updated_at: str  # "2019-09-24T09:03:22.000Z"
    episode: Episode


class RatedEpisode(Episode):
    rated_at: str  # "2019-09-24T09:03:22.000Z"
    rating: int  # 9
    type: Literal["episode"]
    episode: Episode


class RatedShow(Show):
    rated_at: str  # "2019-09-24T09:03:22.000Z"
    rating: int  # 9
    type: Literal["show"]
    show: Show


class WatchedEpisode(Episode):
    plays: int  # 10
    last_watched_at: str  # "2019-09-24T09:03:22.000Z"
    last_updated_at: str  # "2019-09-24T09:03:22.000Z"


class HistoryEpisode(Episode, Show):  # type: ignore
    id: int
    episode: Episode
    show: Show
    watched_at: str  # "2019-09-24T09:03:22.000Z"
    action: str  # watch
    type: str  # episode


class CollectedShow(Show):
    last_collected_at: str  # "2019-09-24T09:03:22.000Z"
    last_updated_at: str  # "2019-09-24T09:03:22.000Z"
    show: Show


class CollectedMovie(Movie):
    collected_at: str  # "2019-09-24T09:03:22.000Z"
    updated_at: str  # "2019-09-24T09:03:22.000Z"
    movie: Movie


class RatedMovie(Movie):
    rated_at: str  # "2019-09-24T09:03:22.000Z"
    rating: int  # 9
    type: Literal["movie"]
    movie: Movie


class WatchedMovie(Movie):
    id: int  # Primary Key
    movie_id: int
    total_plays: int  # 10
    last_watched_at: str  # "2019-09-24T09:03:22.000Z"


class HistoryMovie(Movie):
    id: int
    movie: Movie
    watched_at: str  # "2019-09-24T09:03:22.000Z"
    action: str  # watch
    type: str  # movie


####################################################################################################
# SQLITE ROW DATACLASSES.
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


class ExtendedShowRow(TypedDict):
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
    overview: str
    first_aired: str
    runtime: int
    certification: str
    network: str
    country: str
    trailer: str
    homepage: str
    status: str
    rating: float
    votes: int
    comment_count: int
    language: str
    aired_episodes: int


# Add new genre table.


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


class ExtendedEpisodeRow(TypedDict):
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
    overview: str
    rating: float
    votes: int
    comment_count: int
    first_aired: str
    runtime: int


class MovieRow(TypedDict):
    type: Literal["movie"]
    id: int  # ids.trakt, will be treated as primary key.
    title: str  # "A Quiet Place"
    year: int  # 2018
    trakt_id: int  # 293955
    trakt_slug: str  # "a-quiet-place-2018"
    imdb_id: str  # "tt6644200"
    tmdb_id: int  # 447332


class ExtendedMovieRow(TypedDict):
    type: Literal["movie"]
    id: int  # ids.trakt, will be treated as primary key.
    title: str  # "A Quiet Place"
    year: int  # 2018
    trakt_id: int  # 293955
    trakt_slug: str  # "a-quiet-place-2018"
    imdb_id: str  # "tt6644200"
    tmdb_id: int  # 447332

    tagline: str
    overview: str
    released: str
    runtime: int
    country: str
    trailer: str
    homepage: str
    status: str
    rating: float
    votes: int
    comment_count: int
    language: str
    certification: str


# Add genres table.


class CollectedMediaRow(TypedDict):
    # id: str  # Primary Key
    media_id: int
    collected_at: str  # "2019-09-24T09:03:22.000Z"


class CollectedEpisodeRow(CollectedMediaRow):
    type: Literal["episode"]


class CollectedMovieRow(CollectedMediaRow):
    type: Literal["movie"]


class WatchedEpisodeRow(TypedDict):
    id: int  # Primary Key
    episode_id: int
    total_plays: int  # 10
    last_watched_at: str  # "2019-09-24T09:03:22.000Z"


class HistoryMediaRow(TypedDict):
    id: int  # Primary Key
    media_id: int
    watched_at: str  # "2019-09-24T09:03:22.000Z"


class HistoryEpisodeRow(HistoryMediaRow):
    type: Literal["episode"]


class HistoryMovieRow(HistoryMediaRow):
    type: Literal["movie"]


class RatedMediaRow(TypedDict):
    # id: str  # Primary Key : will be auto generated while writing it to db.
    media_id: int
    rating: int
    rated_at: str  # "2019-09-24T09:03:22.000Z"


class RatedEpisodeRow(RatedMediaRow):
    type: Literal["episode"]


class RatedMovieRow(RatedMediaRow):
    type: Literal["movie"]


class RatedShowRow(RatedMediaRow):
    type: Literal["show"]


class WatchlistMovie(Movie):
    rank: int
    id: int
    listed_at: str
    notes: str
    type: Literal["movie"]
    movie: Movie


class WatchlistShow(Show):
    rank: int
    id: int
    listed_at: str
    notes: str
    type: Literal["show"]
    show: Show


class WatchlistMediaRow(TypedDict):
    id: int  # Primary Key
    media_id: int
    watchlisted_at: str  # "2019-09-24T09:03:22.000Z"


class WatchlistShowRow(WatchlistMediaRow):
    type: Literal["show"]


class WatchlistMovieRow(WatchlistMediaRow):
    type: Literal["movie"]
