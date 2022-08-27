import pymysql
from api.src.Config import Config
from api.src.common.Object import Singleton


def get_db() -> pymysql.connections.Connection:
    db = pymysql.connect(
        user=Config.instance().MYSQL_USER,
        passwd=Config.instance().MYSQL_PASSWD,
        host=Config.instance().MYSQL_HOST,
        db=Config.instance().MYSQL_DB,
        charset=Config.instance().MYSQL_CHARSET,
        port=Config.instance().MYSQL_PORT,
    )
    return db


def get_cursor(db: pymysql.connections.Connection) -> pymysql.cursors.DictCursor:
    return db.cursor(pymysql.cursors.DictCursor)


class SQLUtil(Singleton):
    def __init__(self):
        super().__init__()
        self.logging = False
        self.debug = False

    def open(self, *commands):
        db = get_db()
        cursor = get_cursor(db)
        ret = []
        for command in commands:
            result = command(cursor)
            if result:
                ret.append(result)
        if not self.debug:
            db.commit()
        else:
            db.rollback()
        db.close()
        return ret

    def executeCommand(self, sql: str, args=None) -> any:
        def _execute(cursor: any):
            if self.logging:
                print(sql + " // " + str(args))
            if args is not None:
                result = cursor.execute(sql, tuple(args))
            else:
                result = cursor.execute(sql)
            if self.logging:
                print(result)
            return None

        return _execute

    def fetchallCommand(self):
        def _fetchall(cursor: any):
            return cursor.fetchall()

        return _fetchall

    def execute(self, sql: str, args=None) -> any:
        return self.open(
            self.executeCommand(sql=sql, args=args),
            self.fetchallCommand()
        )[0]


if __name__ == '__main__':
    sql_util = SQLUtil.instance()
    print(sql_util.execute(sql='select * from perfumes'))
