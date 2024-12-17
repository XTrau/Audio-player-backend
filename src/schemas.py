from albums.schemas import SAlbum
from artists.schemas import SArtist
from tracks.schemas import STrack


class STrackAlbum(STrack):
    album: SAlbum | None = None


class STrackArtists(STrack):
    artists: list[SArtist]


class STrackFullInfo(STrack):
    album: SAlbum | None = None
    artists: list[SArtist]


class SArtistFullInfo(SArtist):
    albums: list[SAlbum]
    tracks: list[STrackFullInfo]


class SAlbumFullInfo(SAlbum):
    artists: list[SArtist]
    tracks: list[STrackArtists]
