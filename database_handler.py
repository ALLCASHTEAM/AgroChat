import sqlite3

def write_db_txt( question, answer, marked):
    con = sqlite3.connect("database/feedback.db")
    cur = con.cursor()

    if marked:
        cur.execute(f"SELECT id FROM marked_txt WHERE id=(SELECT max(id) FROM marked_txt);")
    id = int(cur.fetchone()[0]) + 1
    cur.execute(f"INSERT INTO marked_txt(id, question, answer) VALUES({id}, '{question}', '{answer}');")
    con.commit()
    con.close()

def write_db_img():
    pass


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
    write_db_txt('marked_txt', 'Гомо', 'dsa')
    read_db("marked_txt", where_statement="id = 2")
