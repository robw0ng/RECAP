import sqlite3
import os

class SQLiteTable:
    def __init__(self, dbFile, tableName, fields={'id' : 'INTEGER PRIMARY KEY'}, extraCommands=[]):
        self.tableName = tableName
        self.dbFile = dbFile

        conn = sqlite3.connect(dbFile)
        cursor = conn.cursor()

        column_defs = []
        for col_name, col_type in fields.items():
            column_defs.append(f'"{col_name}" {col_type}')
        
        columns = f'{", ".join(column_defs)}'

        extras = ''
        if extraCommands:
            extras  = f', {", ".join(extraCommands)}'

        create_table_sql = f'CREATE TABLE IF NOT EXISTS "{tableName}" ({columns}{extras})'
        cursor.execute(create_table_sql)

        self.fields = self.columns()

        conn.commit()
        conn.close()

    def insert(self, record):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        placeholders = ', '.join(['?' for _ in record])
        
        cursor.execute(f"INSERT OR REPLACE INTO {self.tableName} VALUES ({placeholders})", tuple(record.values()))
        
        conn.commit()
        conn.close()

    def delete(self, condition=None):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        condition = f'WHERE {condition}' if condition != None else ''
        deleteStatement = f"DELETE FROM {self.tableName} {condition}"

        cursor.execute(deleteStatement)

        conn.commit()
        conn.close()

    def getAllRows(self):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.tableName}")
        results = cursor.fetchall()
        conn.close()
        return results

    def getAllRowsAsDict(self, one=False):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.tableName}")
        r = [dict((cursor.description[i][0], value) \
            for i, value in enumerate(row)) for row in cursor.fetchall()]
        conn.close()
        return (r[0] if r else None) if one else r

    def selectAll(self):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.tableName}")
        results = cursor.fetchall()

        conn.close()
        return [dict(zip(self.fields, row)) for row in results]

    def columns(self):
        columns = []
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        data = cursor.execute(f'''SELECT * FROM {self.tableName}''')

        for column in data.description:
            columns.append(column[0])

        return columns
    
    def drop(self):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {self.tableName}")
        conn.commit()
        conn.close()

    def selectWhere(self, condition):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {self.tableName} WHERE {condition}")
        results = cursor.fetchall

        conn.close()
        return [dict(zip(self.fields, row)) for row in results]
    
    def copyTo(self, dest):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        statement = f'INSERT OR REPLACE INTO {dest.tableName} SELECT * FROM {self.tableName}'
        cursor.execute(statement)

        conn.commit()
        conn.close()

    def update(self, data, condition=None):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        set_values = ', '.join([f"{col} = ?" for col in data.keys()])
        values = tuple(data.values())

        condition = f" WHERE {condition}" if condition else ""

        update_query = f"UPDATE {self.tableName} SET {set_values}{condition}"

        cursor.execute(update_query, values)
        conn.commit()
        conn.close()


class SQLiteDB:
    def __init__(self, dbFile):
        self.dbFile = dbFile
        self.tables = {}

        if not os.path.exists(dbFile):
            conn = sqlite3.connect(dbFile)
            conn.commit()
            conn.close()
    
    def createTable(self, tableName, fields, extras=[]):
        self.tables[tableName] = SQLiteTable(self.dbFile, tableName, fields, extras)
        return self.tables[tableName]

    def tableList(self):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tableList = [row[0] for row in cursor.fetchall()]
        result = [sublist for sublist in tableList]
        conn.close()
        return result

    def getTable(self, tableName):
        if tableName in self.tableList():
            return SQLiteTable(self.dbFile, tableName)

    def dropTable(self, tableName):
        conn = sqlite3.connect(self.dbFile)
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {tableName}")
        conn.commit()
        conn.close()

    def executeQuery(self, query, params=()):
        conn =  sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        cursor.execute(query, params)
        results = cursor.fetchall
        
        conn.commit()
        conn.close()
        return results
    
    def execute(self, query):
        conn =  sqlite3.connect(self.dbFile)
        cursor = conn.cursor()

        cursor.execute(query)
        
        conn.commit()
        conn.close()
        return

    def connect(self):
        conn = sqlite3.connect(self.dbFile)
        return conn