# This Python file uses the following encoding: utf-8
from jinja2 import Environment, FileSystemLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QFileDialog
from PySide6.QtCore import Qt


class JinjaMaker:
    es_username = None
    es_password = None
    es_host_list = [
        "https://grafana.ether-source.fr:9201",
        "https://grafana.ether-source.fr:9202",
        "https://grafana.ether-source.fr:9203"
        ]
    name = None
    telegraf_log_file_path = None
    os_is_windows = True
    os_is_linux = False
    custom_process_enabled = False
    process_list_to_harvest = ["telegraf"]
    nvidia_smi_enabled = False
    nvidia_smi_bin_path = None
    chia_collect_info_enabled = False
    launcher_id = None
    chia_private_full_node_crt_path = None
    chia_private_full_node_key_path = None
    t_rex_enabled = False
    api_lfdm = None
    def __init__(self):
        pass

    def SetEsUsername(self, username):
        self.es_username = username

    def SetEsPassword(self, password):
        self.es_password = password

    def SetSmiBinPath(self):
        self.nvidia_smi_bin_path = QFileDialog.getOpenFileName()

    def SetChiaCrtPath(self):
        self.nvidia_smi_bin_path = QFileDialog.getOpenFileName()

    def SetChiaKeyPath(self):
        self.nvidia_smi_bin_path = QFileDialog.getOpenFileName()

    def SetCustomName(self, customName):
        self.name = customName

    def SetLaucherId(self, launcher_id):
        self.launcher_id = launcher_id

    def SetOsIsWindows(self, radio):
        if radio:
            self.os_windows = True
        else:
            self.os_windows = False

    def SetOsIsLinux(self, radio):
        if radio:
            self.os_linux = True
        else:
            self.os_linux = False

    def SetSmiEnable(self, state):
        if (Qt.Checked == state):
            self.nvidia_smi_enabled = True
        else:
            self.nvidia_smi_enabled = False

    def SetCollectChiaEnable(self, state):
        if (Qt.Checked == state):
            self.chia_collect_info_enabled = True
        else:
            self.chia_collect_info_enabled = False

    def GetCollectChiaEnable(self):
        return self.chia_collect_info_enabled

    def SetTrexEnable(self, state):
        if (Qt.Checked == state):
            self.t_rex_enabled = True
        else:
            self.t_rex_enabled = False

    def SetCustomProcessEnable(self, state):
        if (Qt.Checked == state):
            self.custom_process_enabled = True
        else:
            self.custom_process_enabled = False

    def GetCustomProcessEnable(self):
        return self.custom_process_enabled

    def SetTelegrafLogFilePath(self, telegraf_log_file_path):
        self.telegraf_log_file_path = telegraf_log_file_path

    def AppendToProcessList(self, process_list_to_harvest):
        tmpList = process_list_to_harvest.split(' ')
        for item in tmpList:
            self.process_list_to_harvest.append(item)

    def GenerateTemplate(self):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('telegraf.conf.jinja')
        data_template = {
            "es_username": self.es_username,
            "es_password": self.es_password,
            "es_host_list": self.es_host_list,
            "name": self.name,
            "telegraf_log_file_path": self.telegraf_log_file_path,
            "os_is_windows": self.os_is_windows,
            "os_is_linux": self.os_is_linux,
            "custom_process_enabled": self.custom_process_enabled,
            "process_list_to_harvest": self.process_list_to_harvest,
            "nvidia_smi_enabled": self.nvidia_smi_enabled,
            "nvidia_smi_bin_path": self.nvidia_smi_bin_path,
            "chia_collect_info_enabled": self.nvidia_smi_bin_path,
            "launcher_id": self.launcher_id,
            "chia_private_full_node_crt_path": self.chia_private_full_node_crt_path,
            "chia_private_full_node_key_path": self.chia_private_full_node_key_path,
            "t_rex_enabled": self.t_rex_enabled,
            "api_lfdm": self.api_lfdm,
            }
        output_from_parsed_template = template.render(data_template)
        with open("telegraf.conf", "w") as fh:
            fh.write(output_from_parsed_template)
