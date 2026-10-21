import io_work
import connection_work
import sys
from mysql.connector import Error


def main():
    try:
        cw = connection_work.ConnectionWork()
        cw.schema_initialisation()
        cw.index_creation()
        cw.json_info_uploading()
        cw.views_creation()
        cli = io_work.CLI()
        cli.run(cw)

    except FileNotFoundError as e:
        print(f"Error: Missing required file ({e}). Exiting.")
        sys.exit(1)

    except Error as e:
        print(f"Database failure: {e.msg} (code: {e.errno})")
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()