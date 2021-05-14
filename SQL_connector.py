import logging
import sqlite3
from datetime import datetime

import settings
from data_loader import DataLoader


class SQLite_saver:
    def __init__(self, connector: sqlite3.Connection):
        self.connector = connector
        self.cursor = self.connector.cursor()
        # self.connector.set_trace_callback(print)


    def close_saver(self):
        self.connector.close()


    def create_documents(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS documents (
                name TEXT,
                protocolid TEXT,
                treat_code TEXT,
                treat_company_id TEXT,
                treat_hash TEXT,
                treat_place TEXT,
                href TEXT,
                author TEXT,
                date TEXT
            );
        '''
        self.cursor.execute(sql)


    def check_dockument(self, data):
        sql = 'SELECT * FROM documents WHERE protocolid = ?'
        self.cursor.execute(sql, (data['protocolid'],))
        return self.cursor.fetchall()


    def add_documents(self, data):
        added_documents = []
        sql = '''
        INSERT INTO documents(
                name,
                protocolid,
                treat_code,
                treat_company_id,
                treat_hash,
                treat_place,
                href,
                author,
                date 
        ) values(?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        for item in data:
            if not self.check_dockument(item):
                self.cursor.execute(sql, (
                    item['name'],
                    item['protocolid'],
                    item['treat_code'],
                    item['treat_company_id'],
                    item['treat_hash'],
                    item['treat_place'],
                    item['href'],
                    item['author'],
                    item['date']
                ))
                self.connector.commit()
                added_documents.append(item)
        if added_documents:
            logging.info(f'Added {len(added_documents)} new documents:')
            for document in added_documents:
                logging.info(f"{document['name']}\t{document['author']}\t{document['date']}")
        else:
            logging.info('no new documents')
        return added_documents


    def get_document(self, id):
        self.cursor.execute('SELECT * FROM documents WHERE protocolid = ?', (id,))
        return self.cursor.fetchall()
        



def main():
    with sqlite3.connect(settings.DB) as sqlite_conn:
        sqlite_saver = SQLite_saver(sqlite_conn)

        sqlite_saver.create_documents()

        dl = DataLoader(settings.URL)
        sqlite_saver.add_documents(dl.get_data())

    # sqlite_saver.close_saver()

if __name__ == '__main__':
    main()