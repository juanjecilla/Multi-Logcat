from threading import Thread

from ppadb.client import Client as AdbClient

from adb_tools.logcat_manager import LogcatManager


class AdbManager(Thread):

    def __init__(self):
        super().__init__()
        self.adb_client = AdbClient(host="127.0.0.1", port=5037)
        self.logcats = []
        self.start()

    def get_current_devices(self):
        devices = self.adb_client.devices()
        return devices

    def get_logcat(self, device, callback=None):
        logcat_manager = LogcatManager(device, callback)
        logcat_manager.start()

        self.logcats.append(logcat_manager)

    def stop_logcat(self, item):
        logcat_manager = self.logcats[item]
        logcat_manager.stop_logcat()

        self.logcats.remove(logcat_manager)

    def get_installed_packages(self, device):
        installed_packages = list(map(lambda x: x.replace("package:", ""), device.shell("cmd package list packages -3").split("\n")))
        return installed_packages

    def execute(self, device, command):
        device.shell("su -c '{}'".format(command), handler=self._print)

    @staticmethod
    def _print(connection):
        while True:
            data = connection.read(1024)
            if not data:
                break
            print(data.decode('utf-8'))

        connection.close()
