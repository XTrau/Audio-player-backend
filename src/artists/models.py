from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class ArtistOrm(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=64))
    image_file_name: Mapped[str | None] = mapped_column(String(length=64))

    albums: Mapped[list["AlbumOrm"]] = relationship(
        back_populates="artists", secondary="artist_album"
    )
    tracks: Mapped[list["TrackOrm"]] = relationship(
        back_populates="artists", secondary="artist_track"
    )
