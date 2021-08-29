# This Python file uses the following encoding: utf-8
from jinja2 import Environment, FileSystemLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QFileDialog


class JinjaMaker:
    es_username = None
    es_password = None
    es_host_list = None
    name = None
    telegraf_log_file_path = None
    os_is_windows = False
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

    def SetSmiBinPath(self, path):
        self.nvidia_smi_bin_path = QFileDialog.getOpenFileName()

    def SetChiaCrtPath(self, path):
        self.nvidia_smi_bin_path = QFileDialog.getOpenFileName()

    def SetChiaKeyPath(self, path):
        self.nvidia_smi_bin_path = QFileDialog.getOpenFileName()

    def generate_file():
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('test.html')
        output_from_parsed_template = template.render(foo='Hello World!')
        print(output_from_parsed_template)
        # to save the results
        with open("my_new_file.html", "w") as fh:
            fh.write(output_from_parsed_template)
