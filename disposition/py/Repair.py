from json import dumps

class Repair:

    def __init__(self):
        self.create_all_environment_file()

    def create_all_environment_file(self):
        environment = {
            "Version": __import__('sys').version,
            "platform": __import__('sys').platform,
            }

        with open("./disposition/py/environment.json", "w", encoding="utf-8") as f:
            f.write(dumps(environment, indent=2))

        def create_other(data, file_name):
            data.sort(key=len, reverse=True)
            with open('./disposition/py/' + file_name+ ".json", "w") as f:
                f.write(dumps({file_name : data}, indent=2))

        def create_keyword():
            data = {}
            data["keyword"] = list(__import__("keyword").kwlist)
            data["builtins"] = list(dir(__builtins__))
            data["dir_sys"] = list(dir("sys"))
            data["lineComment"] = "#"
            with open('./disposition/py/keyword.json', "w") as f:
                f.write(dumps(data, indent=2))

        create_keyword()

        print("[Repair over]")


if __name__ == '__main__':
    demo = Repair()
