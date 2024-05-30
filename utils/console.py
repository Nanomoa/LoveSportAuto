import datetime


class Console:
    def __init__(self):
        self.SUCCESS = "\033[32m"
        self.WARNING = "\033[33m"
        self.INFO = "\033[34m"
        self.ERROR = "\033[31m"
        self.END = "\033[0m"

    @staticmethod
    def write_line(content):
        print("[{}] AutoLoveSports: {}".format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            content
        ))

    def write_line_color(self, color, content):
        print("[{}] AutoLoveSports: {}".format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            color + content + self.END
        ))

    def success(self, content):
        self.write_line_color(self.SUCCESS, content)

    def warning(self, content):
        self.write_line_color(self.WARNING, content)

    def info(self, content):
        self.write_line_color(self.INFO, content)

    def error(self, content):
        self.write_line_color(self.ERROR, content)
