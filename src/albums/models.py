from sqlalchemy import String, asc, text, func, select, and_
from sqlalchemy.types import DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship, column_property

from database import Base
from tracks.models import TrackOrm


class AlbumOrm(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    released_at: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    image_file_name: Mapped[str | None] = mapped_column(
        String(255), default=None, nullable=True
    )

    artists: Mapped[list["ArtistOrm"]] = relationship(
        back_populates="albums", secondary="artist_album"
    )

    tracks: Mapped[list["TrackOrm"]] = relationship(
        back_populates="album",
        order_by=asc(text("track_1.number_at_album")),
        cascade="all, delete-orphan",
    )

    track_count = column_property(
        select(func.count(TrackOrm.id))
        .where(TrackOrm.album_id == id)
        .correlate_except(TrackOrm)
        .scalar_subquery()
    )
