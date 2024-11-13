from sqlalchemy import String
from sqlalchemy.types import DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class AlbumOrm(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=64), nullable=False)

    released_at: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    image_file_name: Mapped[str | None] = mapped_column(
        String(length=64), default=None, nullable=True
    )

    artists: Mapped[list["ArtistOrm"]] = relationship(
        back_populates="albums", secondary="artist_album"
    )

    tracks: Mapped[list["TrackOrm"]] = relationship(back_populates="album")
