import sqlite3

def write_db(table, question, answer):
    con = sqlite3.connect("database/feedback.db")
    cur = con.cursor()
    cur.execute(f"SELECT id FROM {table} WHERE id=(SELECT max(id) FROM {table});")
    id = int(cur.fetchone()[0]) + 1
    cur.execute(f"INSERT INTO {table}(id, question, answer) VALUES({id}, '{question}', '{answer}');")
    con.commit()
    con.close()


def read_db(table, where_statement=None):
    con = sqlite3.connect("database/feedback.db")
    cur = con.cursor()
    if where_statement is not None:
        cur.execute(f"SELECT * FROM {table} WHERE {where_statement}")
    else:
        cur.execute(f"SELECT * FROM {table}")

    result = cur.fetchall()
    print(result)
    con.close()

if __name__ == "__main__":
    write_db('marked_txt', 'Гомо', 'dsa')
    read_db("marked_txt")
