from mariadb import connect


def _get_connection(database_name='forum_system_schema'):
    try:
        conn = connect(
            user='root',
            password='2210',
            host='localhost',
            port=3306,
            database=database_name

        )
        print(f"Connected to the {database_name} database!")

        return conn
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
