import sqlite3
from multiprocessing import Process
import os
import signal

conn = sqlite3.connect('Modules/dump.db')
c = conn.cursor()
# conn.row_factory = sqlite3.Row

c.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    event TEXT,
    details TEXT
)
''')


def log_event(event, details):
    '''Adds log, event is one word, details follow, order by id and datetime'''
    c.execute(
        "INSERT INTO logs (timestamp, event, details) VALUES (datetime('now'), ?, ?)", (event, details))
    conn.commit()


def get_logs(start=0, amt=1):
    '''Returns list of logs in descending order (index), start is index (0 most recent), number of logs from startis amt'''
    res = conn.execute(
        f"SELECT * FROM logs ORDER BY id DESC LIMIT {amt} OFFSET {start}")
    return res.fetchall()


def clear_table():
    '''Clears the table'''
    c.execute("DELETE FROM logs")
    conn.commit()
    c.execute("DELETE FROM sqlite_sequence WHERE name='logs'")
    conn.commit()


if __name__ == "__main__":
    # Example usage
    clear_table()
    log_event('test_event', "test Commit")
    log_event('test_event2', "test second commit")
    log_event('test_event3', "top level commit")
    logs = get_logs(start=0, amt=3)
    print(logs, logs[0][2])


# def update_logs():
#     global dump_process, dump_id
#     if dump_process == None or not dump_process.is_alive():
#         dump_process = Process(target=_write_to_file)
#         dump_id = dump_process.pid
#         print(dump_id)
#         dump_process.start()
#     else:
#         print("Continuous call to update logs")