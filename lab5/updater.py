import sqlite3


def add_block(conn, block_id, view, desc):
    cur = conn.cursor()
    cur.execute("INSERT INTO BLOCKS (id, view, desc) VALUES (?, ?, ?)", (block_id, view, desc))

    cur.execute("INSERT INTO event_stream (type, record_id) VALUES ('block', ?)", (block_id,))

    conn.commit()
    print(f"Блок {block_id} додано в БД та event_stream!")


def add_vote(conn, block_id, voter_id, source_id):
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO VOTES (block_id, voter_id, timestamp, source_id)
                VALUES (?, ?, datetime('now'), ?)
                """, (block_id, voter_id, source_id))

    cur.execute("INSERT INTO event_stream (type, record_id) VALUES ('vote', ?)", (block_id,))

    conn.commit()
    print(f"Голос за блок {block_id} додано!")


if __name__ == "__main__":
    conn = sqlite3.connect('../lab3/mydatabase.db')

    while True:
        choice = input("Що додати? (1 - Блок, 2 - Голос, 0 - Вихід): ")

        if choice == '1':
            b_id = input("Введіть ID блоку (напр. 0xBlk999): ")
            view = int(input("Введіть View (число): "))
            desc = input("Введіть опис: ")
            add_block(conn, b_id, view, desc)

        elif choice == '2':

            b_id = input("Введіть ID блоку, за який голосують: ")
            voter_id = int(input("Введіть ID виборця (PERSONS id): "))
            source_id = int(input("Введіть ID джерела (SOURCES id): "))
            add_vote(conn, b_id, voter_id, source_id)

        elif choice == '0':
            break

    conn.close()