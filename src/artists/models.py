from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ArtistOrm(Base):
    __tablename__ = 'artist'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    image_file_name: Mapped[str | None]

    albums: Mapped[list["AlbumOrm"]] = relationship(back_populates="artist")
    tracks: Mapped[list["TrackOrm"]] = relationship(
        back_populates="artists",
        secondary="artist_track"
    )