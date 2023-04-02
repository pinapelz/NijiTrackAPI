import mysql.connector
from mysql.connector import Error, errorcode
from collections import namedtuple


HistoricalSubData = namedtuple("HistoricalSubData", ["sub_count", "date"])
RankData = namedtuple("RankData", ["rank", "member_count"])


class SQLHandler:
    def __init__(self, host_name: str, user_name: str, user_password: str, database_name: str):
        self.host_name = host_name
        self.username = user_name
        self.password = user_password
        self.database_name = database_name
        self.connection = self._create_server_connection(
            host_name, user_name, user_password)
        self._load_database(database_name)

    def _create_server_connection(self, host_name: str, user_name: str, user_password: str, exclude=None) -> mysql.connector:
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
        return connection

    def _create_database(self, cursor: str, database_name: str):
        try:
            cursor.execute(
                f"CREATE DATABASE {database_name} DEFAULT CHARACTER SET 'utf8'")
        except Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

    def _load_database(self, database_name: str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"USE {database_name}")
            print(f"Database {database_name} loaded successfully")
        except Error as err:
            print(f"Database {database_name} does not exist")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self._create_database(cursor, database_name)
                print(f"Database {database_name} created successfully")
                self.connection.database = database_name
            else:
                print(err)
                exit(1)

    def get_subcount(self, table_key: str, iso_date: str):
        iso_date = iso_date.replace("T", " ")
        iso_date = iso_date.replace("Z", "")
        cursor = self.connection.cursor()
        # sql query to get the subcount nearest to the iso_date
        query = f"SELECT subscriber_count, timestamp FROM {table_key} WHERE timestamp <= '{iso_date}' ORDER BY timestamp DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        sub_count = result[0]
        db_date = result[1]
        db_date = db_date.isoformat()
        return HistoricalSubData(sub_count, db_date)
    
    def get_current_rank(self, channel_id: str):
        cursor = self.connection.cursor()
        query = """
            SELECT COUNT(*) AS rank
            FROM subscriber_data
            WHERE subscriber_count > (SELECT subscriber_count FROM subscriber_data WHERE channel_id = %s)
        """
        cursor.execute(query, (channel_id,))
        result = cursor.fetchone()
        # get total number of rows in table
        cursor.execute("SELECT COUNT(*) FROM subscriber_data")
        member_count = cursor.fetchone()[0]
        data = RankData(result[0] + 1, member_count)
        return data
    
    def get_current_subscriber_count(self, channel_id: str):
        cursor = self.connection.cursor()
        query = "SELECT subscriber_count FROM subscriber_data WHERE channel_id = %s"
        cursor.execute(query, (channel_id,))
        result = cursor.fetchone()
        return result[0]