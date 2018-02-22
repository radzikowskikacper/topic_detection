import json
from brandbastion.core.data import DATA_PATH, cursor, cnx
from langdetect import detect


def load_from_file(fname):
    with open('{}/{}'.format(DATA_PATH, fname)) as f:
        for line in f:
            line = json.loads(line)
            try:
                if detect(line['text']) == 'en':
                    yield line
            except:
                pass

def load_from_database(ids = None):
    query = 'SELECT * FROM comments'
    if ids:
        query += ' WHERE tag_id IN ({})'.format(','.join([str(id) for id in ids]))
        query += ' ORDER BY FIELD(tag_id, {})'.format(','.join([str(id) for id in ids]))

    cursor.execute(query)

    for row in cursor:
        yield row

def save_to_database(fname):
    mm = load_from_file(fname)
    query = 'INSERT INTO comments(tag_id, text) VALUES '
    i = 0
    for line in mm:
        i += 1
        query += '({}, "{}"),'.format(i, line['text'].replace('"', '\\"'))
    query = query[:-1]
    cursor.execute(query)
    cnx.commit()

def add_to_db(comment):
    query = 'INSERT INTO comments(tag_id, text) SELECT MAX(tag_id) + 1, {} FROM comments'.format(comment)
    cursor.execute(query)
    cnx.commit()

def close_db():
    cursor.close()
    cnx.close()