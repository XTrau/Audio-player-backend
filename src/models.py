from src.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey


class ArtistOrm(Base):
    __tablename__ = 'artists'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    image_file_name: Mapped[str | None]

    albums: Mapped[list["AlbumOrm"]] = relationship(back_populates="artist")
    tracks: Mapped[list["TrackOrm"]] = relationship(
        back_populates="artists",
        secondary="artists_tracks"
    )


class AlbumOrm(Base):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.id'))
    image_file_name: Mapped[str | None]

    artist: Mapped["ArtistOrm"] = relationship(back_populates="albums", overlaps="albums")
    tracks: Mapped[list["TrackOrm"]] = relationship(back_populates="album")


class ArtistTrackOrm(Base):
    __tablename__ = 'artists_tracks'

    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.id'), primary_key=True)
    track_id: Mapped[int] = mapped_column(ForeignKey('tracks.id'), primary_key=True)


class TrackOrm(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    audio_file_name: Mapped[str]
    image_file_name: Mapped[str | None]
    album_id: Mapped[int | None] = mapped_column(ForeignKey('albums.id'))

    album: Mapped["AlbumOrm"] = relationship(back_populates="tracks")
    artists: Mapped[list["ArtistOrm"]] = relationship(
        back_populates="tracks",
        secondary="artists_tracks"
    )
