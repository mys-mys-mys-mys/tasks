import io_work
import connection_work
import sys
from mysql.connector import Error

def main():
    # try:
        cw = connection_work.ConnectionWork()
        cw.schema_initialisation()
        cw.index_creation()
        cw.json_info_uploading()
        cw.views_creation()
        cli = io_work.CLI()
        cli.run(cw)

        #weird printing
    # except FileNotFoundError as e:
    #     print("Configuration or data file missing: %s", e)
    #     print(f"Error: Missing required file ({e}). Exiting.")
    #     sys.exit(1)
    #
    # except Error as e:
    #     print("Database failure: %s (code: %s)", e.msg, e.errno)
    #     print(f"Database error: {e.msg}. ")
    #     sys.exit(1)
    #
    # except Exception as e:
    #     print("An unexpected error occurred: %s", e)
    #     print("A fatal error occurred.")
    #     sys.exit(1)

if __name__ == "__main__":
    main()


