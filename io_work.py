import connection_work
import file_work
from file_work import export_to_json, export_to_xml
from views_queries import views_queries_dict

class CLI:

    def __init__(self):
        self.json_format = '.json'
        self.xml_format = '.xml'

    command_list = ("Commands list:\n"
                    "help - show command list\n"
                    "students - path to students file\n"
                    "rooms - path to the rooms file\n"
                    "format - choose an output format and query to download\n"
                    "q to quit")

    def run(self, cw : connection_work.ConnectionWork):
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
                    file_work.get_students_file_path()
                case "rooms":
                    file_work.get_rooms_file_path()
                case "format":
                    self._choose_format(cw)
                case _:
                    print("Unknown command. Type 'help' for options.")

    def _choose_format(self,cw : connection_work.ConnectionWork):
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

    def _choose_query(self, cw: connection_work.ConnectionWork, format: str):
        output_path = f'data/result{format}'
        # Output descriptions to corresponding views
        print("Results to download:")
        for i in range(len(views_queries_dict)):
            # Gets values from dict into a list
            descriptors = [*views_queries_dict.values()]
            print(f"{i + 1} - {descriptors[i]}")
        query = input().strip()
        try:
            query = int(query) - 1
            if (0 > query) or (query > len(views_queries_dict)):
                print("Not an available query number.")
                return
        except ValueError:
            print("Not a number.")
            return
        data = cw.get_info_for_download(query)
        print("Unload started...")
        if format == self.json_format:
           export_to_json(data, output_path)
        elif format == self.xml_format:
            export_to_xml(data,"rooms", "room", output_path)
        print("Unload finished...")