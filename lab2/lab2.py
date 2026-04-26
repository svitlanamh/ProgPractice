import sqlite3
import time
from pydantic import ValidationError
from lab6.models import Vote, Block


class DuplicateViewError(Exception):
    pass

class DuplicateBlockIdError(Exception):
    pass


chain = []
votes = set()
seen_ids = set()
seen_views = set()


def process_block(block_obj):
    try:
        if block_obj.block_id not in votes:
            print(f"Блок {block_obj.block_id} проігноровано (поки немає голосу).")
            return

        if block_obj.view in seen_views:
            raise DuplicateViewError(f"Конфлікт View: {block_obj.view} вже є!")

        if block_obj.block_id in seen_ids:
            raise DuplicateBlockIdError(f"Конфлікт ID: {block_obj.block_id} вже є!")

        chain.append(block_obj)
        seen_views.add(block_obj.view)
        seen_ids.add(block_obj.block_id)

        print(f"Блок додано: {block_obj.block_id} | View: {block_obj.view}")

    except (DuplicateViewError, DuplicateBlockIdError) as e:
        print(e)


if __name__ == "__main__":
    conn = sqlite3.connect('../lab3/mydatabase.db')
    cur = conn.cursor()

    try:
        while True:
            cur.execute("SELECT id, type, record_id FROM event_stream WHERE is_processed = 0")
            events = cur.fetchall()

            for event_id, event_type, record_id in events:

                try:
                    if event_type == 'vote':
                        vote = Vote(
                            voter_id=1,          # або бери з БД якщо є
                            block_id=record_id,
                            source_id=1
                        )
                        votes.add(vote.block_id)
                        print(f"Голос за {vote.block_id} враховано.")

                    if event_type in ('vote', 'block'):
                        cur.execute("SELECT view FROM BLOCKS WHERE id = ?", (record_id,))
                        row = cur.fetchone()

                        if row:
                            block = Block(
                                block_id=record_id,
                                view=row[0]
                            )
                            process_block(block)

                except ValidationError as e:
                    print(f"❌ Validation error: {e}")

                cur.execute(
                    "UPDATE event_stream SET is_processed = 1 WHERE id = ?",
                    (event_id,)
                )
                conn.commit()

            time.sleep(3)

    except KeyboardInterrupt:
        print("\nЗупинка BlockProcessor...")
    finally:
        conn.close()