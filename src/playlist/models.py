from sqlalchemy import ForeignKey, func, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class PlaylistOrm(Base):
    __tablename__ = "playlist"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    image_file_name: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now, nullable=False
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now, onupdate=func.now, nullable=False
    )

    tracks: Mapped[list["TrackOrm"]] = relationship(secondary="playlist_tracks")
