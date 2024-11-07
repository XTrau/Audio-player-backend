from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class TrackOrm(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    audio_file_name: Mapped[str]
    image_file_name: Mapped[str | None]
    album_id: Mapped[int | None] = mapped_column(
        ForeignKey("album.id", ondelete="CASCADE")
    )

    album: Mapped["AlbumOrm"] = relationship(
        back_populates="tracks"
    )
    artists: Mapped[list["ArtistOrm"]] = relationship(
        back_populates="tracks",
        secondary="artist_track"
    )
