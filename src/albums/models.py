from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class AlbumOrm(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    image_file_name: Mapped[str | None]

    artists: Mapped[list["ArtistOrm"]] = relationship(
        back_populates="albums", secondary="artist_album"
    )
    tracks: Mapped[list["TrackOrm"]] = relationship(
        back_populates="album"
    )
