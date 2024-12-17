from database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey


class ArtistTrackOrm(Base):
    __tablename__ = "artist_track"

    artist_id: Mapped[int] = mapped_column(
        ForeignKey("artist.id", ondelete="CASCADE"), primary_key=True
    )
    track_id: Mapped[int] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE"), primary_key=True
    )


class ArtistAlbumOrm(Base):
    __tablename__ = "artist_album"

    artist_id: Mapped[int] = mapped_column(
        ForeignKey("artist.id", ondelete="CASCADE"), primary_key=True
    )
    album_id: Mapped[int] = mapped_column(
        ForeignKey("album.id", ondelete="CASCADE"), primary_key=True
    )


class TrackPlaylistOrm(Base):
    __tablename__ = "playlist_tracks"

    track_id: Mapped[int] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE"), primary_key=True
    )

    playlist_id: Mapped[int] = mapped_column(
        ForeignKey("playlist.id", ondelete="CASCADE"), primary_key=True
    )


class UserTrackOrm(Base):
    __tablename__ = "liked_tracks"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    track_id: Mapped[int] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE"), primary_key=True
    )

class UserPlaylistOrm(Base):
    __tablename__ = "liked_playlists"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    track_id: Mapped[int] = mapped_column(
        ForeignKey("playlist.id", ondelete="CASCADE"), primary_key=True
    )

