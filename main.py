import IOWork
import connectionWork
import sys
from mysql.connector import Error

def main():
    try:
        cw = connectionWork.ConnectionWork()
        cw.schema_initialisation()
        cw.index_creation()
        cw.json_info_uploading()
        cw.views_creation()
        cli = IOWork.CLI()
        cli.run(cw)
    except FileNotFoundError as e:
        print("Configuration or data file missing: %s", e)
        print(f"Error: Missing required file ({e}). Exiting.")
        sys.exit(1)

    except Error as e:
        print("Database failure: %s (code: %s)", e.msg, e.errno)
        print(f"Database error: {e.msg}. ")
        sys.exit(1)

    except Exception as e:
        print("An unexpected error occurred: %s", e)
        print("A fatal error occurred.")
        sys.exit(1)

if __name__ == "__main__":
    main()


