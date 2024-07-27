from database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey


class ArtistTrackOrm(Base):
    __tablename__ = "artist_track"

    artist_id: Mapped[int] = mapped_column(
        ForeignKey("artist.id", ondelete="CASCADE"), primary_key=True
    )
    track_id: Mapped[int] = mapped_column(
        ForeignKey("track.id", ondelete="CASCADE"), primary_key=True
    )
