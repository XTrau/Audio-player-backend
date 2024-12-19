from sqlalchemy import ForeignKey, String, event, DDL, text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base, new_session


class TrackOrm(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    audio_file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    image_file_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    number_at_album: Mapped[int] = mapped_column(nullable=True)

    album_id: Mapped[int] = mapped_column(ForeignKey("album.id", ondelete="CASCADE"))

    album: Mapped["AlbumOrm"] = relationship(back_populates="tracks")
    artists: Mapped[list["ArtistOrm"]] = relationship(
        back_populates="tracks", secondary="artist_track"
    )

    liked_by: Mapped[list["UserTrackOrm"]] = relationship(
        "UserTrackOrm", back_populates="track"
    )


async def create_track_triggers():
    create_insert_track_track_function_sql = text(
        """
            CREATE OR REPLACE FUNCTION manage_track_numbers_on_insert()
            RETURNS TRIGGER AS $$
            DECLARE
                max_number_at_album INT;
            BEGIN
                SELECT COALESCE(MAX(number_at_album), 0)
                INTO max_number_at_album
                FROM track
                WHERE album_id = NEW.album_id;
                
                IF NEW.number_at_album > max_number_at_album THEN
                    NEW.number_at_album := max_number_at_album + 1;
                ELSE
                    UPDATE track
                    SET number_at_album = number_at_album + 1
                    WHERE album_id = NEW.album_id AND number_at_album >= NEW.number_at_album;
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """
    )

    create_on_delete_track_function_sql = text(
        """
            CREATE OR REPLACE FUNCTION shift_track_numbers_on_delete()
            RETURNS TRIGGER AS $$
            BEGIN
                UPDATE track SET number_at_album = number_at_album - 1
                WHERE album_id = OLD.album_id AND number_at_album > OLD.number_at_album;
                
                RETURN OLD;
            END;
            $$ LANGUAGE plpgsql;
        """
    )

    create_insert_track_trigger_sql = text(
        """
            CREATE OR REPLACE TRIGGER track_insert_trigger
            BEFORE INSERT ON track
            FOR EACH ROW
            EXECUTE FUNCTION manage_track_numbers_on_insert();
        """
    )

    create_on_delete_track_trigger_sql = text(
        """
            CREATE TRIGGER track_delete_trigger
            AFTER DELETE ON track
            FOR EACH ROW
            EXECUTE FUNCTION shift_track_numbers_on_delete();
        """
    )

    async with new_session() as session:
        await session.execute(create_insert_track_track_function_sql)
        await session.execute(create_on_delete_track_function_sql)

        await session.execute(create_insert_track_trigger_sql)
        await session.execute(create_on_delete_track_trigger_sql)

        await session.commit()
