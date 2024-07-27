from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class AlbumOrm(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    artist_id: Mapped[int] = mapped_column(ForeignKey("artist.id", ondelete="CASCADE"))
    image_file_name: Mapped[str | None]

    artist: Mapped["ArtistOrm"] = relationship(
        back_populates="albums", overlaps="albums"
    )
    tracks: Mapped[list["TrackOrm"]] = relationship(back_populates="album")
