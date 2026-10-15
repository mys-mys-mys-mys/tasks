import connectionWork
import fileWork
from fileWork import export_to_json, export_to_xml

class CLI:
    def __init__(self):
        self.query_to_unload = 1
        self.json_format = '.json'
        self.xml_format = '.xml'

    command_list = ("Commands list:\n"
                    "help - show command list\n"
                    "students - path to students file\n"
                    "rooms - path to the rooms file\n"
                    "format - choose an output format and query to download\n"
                    "q to quit")

    def run(self, cw):
        print(self.command_list)
        while 1:
            command = input().strip().lower()
            match command:
                case "help":
                    print(self.command_list)
                case "q":
                    print("Quitting...")
                    break
                case "students":
                    fileWork.get_students_file_path()
                case "rooms":
                    fileWork.get_rooms_file_path()
                case "format":
                    self._choose_format(cw)
                case _:
                    print("Unknown command. Type 'help' for options.")

    def _choose_format(self,cw : connectionWork.ConnectionWork):
        print("Input format to unload in:\n"
              "xml - choose unloading info in xml format\n"
              "json - choose unloading info in json format")
        unload_format = input().strip().lower()
        match unload_format:
            case "xml":
                self._choose_query(cw, '.xml')
            case "json":
                self._choose_query(cw, '.json')
            case _:
                print("Not an available format to unload in. Possible options: json or xml.")

    def _choose_query(self, cw: connectionWork.ConnectionWork, format: str):
        queries = {
            "1": (
                "list of rooms and the number of students in each of them",
                cw.get_rooms_count_students,
            ),
            "2": (
                "5 rooms with the smallest average age of students",
                cw.get_smallest_avg_age,
            ),
            "3": (
                "5 rooms with the largest difference in the age of students",
                cw.get_largest_age_diff,
            ),
            "4": (
                "list of rooms where different-sex students live",
                cw.get_rooms_with_diff_sex,
            ),
        }
        output_path = f'./result{format}'

        print("Query results to download:")
        for key, (description, _) in queries.items():
            print(f"{key} - {description}")

        query = input().strip()

        if query not in queries:
            print("Not an available query number.")
            return

        _, fetch_data = queries[query]
        data = fetch_data()

        print("Unload started...")
        if format == self.json_format:
           export_to_json(data, output_path)
        elif format == self.xml_format:
            export_to_xml(data,"rooms", "room", output_path)
        print("Unload finished...")
