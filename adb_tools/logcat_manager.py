import re
from threading import Thread


class LogcatManager(Thread):

    def __init__(self, device, callback=None):
        super().__init__()
        self.device = device
        self.running = True
        self.callback = callback
        self.last_type = "DEFAULT"

    def run(self) -> None:
        super().run()
        self.start_logcat()

    def start_logcat(self):
        pid = self.device.shell("pidof -s caseonit.metricsapp").strip()
        self.device.shell("logcat", handler=self.dump_logcat_by_line)

    def stop_logcat(self):
        self.running = False

    def print_logcat(self, connection):
        while self.running:
            data = connection.read(1024)
            if not data:
                break

            data = str(data.decode("utf-8"))
            parsed_data = self.parse_data(data)

            if self.callback is not None:
                self.callback(parsed_data)

        connection.close()

    def dump_logcat_by_line(self, connect):
        file_obj = connect.socket.makefile()
        while self.running:
            line = file_obj.readline().strip() + "\n"
            if not line:
                break

            parsed_data = self.parse_line(line)

            if self.callback is not None:
                self.callback(parsed_data)

        file_obj.close()
        connect.close()

    def parse_data(self, data):

        data_split = re.split(r"(\d+-\d+\s\d+:\d+:\d+\.\d+\s+\d+\s+\d+\s+)", data)

        if "" in data_split:
            data_split.remove("")

        parsed_data = []

        for item in data_split:
            if "D MetricsApp:" in item or "D/MetricsApp:" in item:
                log_type = "DEBUG"
            elif "I MetricsApp:" in item or "I/MetricsApp:" in item:
                log_type = "INFO"
            elif "W MetricsApp:" in item or "W/MetricsApp:" in item:
                log_type = "WARNING"
            elif "E MetricsApp:" in item or "E/MetricsApp:" in item:
                log_type = "ERROR"
            else:
                log_type = self.last_type

            self.last_type = log_type
            parsed_data.append({"text": item, "type": log_type})

        return parsed_data

    def parse_line(self, line):

        if "D MetricsApp:" in line or "D/MetricsApp:" in line:
            log_type = "DEBUG"
        elif "I MetricsApp:" in line or "I/MetricsApp:" in line:
            log_type = "INFO"
        elif "W MetricsApp:" in line or "W/MetricsApp:" in line:
            log_type = "WARNING"
        elif "E MetricsApp:" in line or "E/MetricsApp:" in line:
            log_type = "ERROR"
        else:
            log_type = self.last_type

        self.last_type = log_type
        parsed_data = {"text": line, "type": log_type}

        return parsed_data
