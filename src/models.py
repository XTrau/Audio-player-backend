from src.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey


class TrackOrm(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    title: Mapped[str]
    audio_file_name: Mapped[str]
    image_file_name: Mapped[str]

    album: Mapped['AlbumOrm'] = relationship()
    artists: Mapped[list['ArtistOrm']] = relationship()


class ArtistOrm(Base):
    __tablename__ = 'artists'

    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    name: Mapped[str]
    image_file_name: Mapped[str]

    albums: Mapped[list['AlbumOrm']] = relationship()


class AlbumOrm(Base):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    title: Mapped[str]
    artist_id: Mapped[int] = mapped_column(ForeignKey('artists.id'), primary_key=True)
    image_file_name: Mapped[str]

    artist: Mapped['ArtistOrm'] = relationship()
    tracks: Mapped['TrackOrm'] = relationship()
