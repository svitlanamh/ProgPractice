import sqlite3

class Block:
    def __init__(self, block_id, view, desc=None):
        self.block_id = block_id
        self.view = view
        self.desc = desc

    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT id, view, desc FROM BLOCKS")
        return cursor.fetchall()


class Person:
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr

    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT name, addr FROM PERSONS")
        return cursor.fetchall()


class Source:
    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT ip_addr, country_code FROM SOURCES")
        return cursor.fetchall()


class Vote:
    @staticmethod
    def get_all_with_join(cursor):
        query = """
                SELECT PERSONS.name, BLOCKS.view, SOURCES.country_code
                FROM VOTES
                         JOIN PERSONS ON VOTES.voter_id = PERSONS.id
                         JOIN BLOCKS ON VOTES.block_id = BLOCKS.id
                         JOIN SOURCES ON VOTES.source_id = SOURCES.id \
                """
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    conn = sqlite3.connect('../lab3/mydatabase.db')
    cur = conn.cursor()

    people = Person.get_all(cur)
    for p in people:
        print(f"Ім'я - {p[0]}")
    print('\n')
    votes = Vote.get_all_with_join(cur)
    for v in votes:
        print(f"{v[0]} - блок {v[1]}")

    conn.close()