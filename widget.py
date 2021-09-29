from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QProcess, QFile, QIODevice, QTextStream
from PySide6.QtGui import QIcon


try:
    from PySide2.QtWinExtras import QtWin
    myappid = 'lfdm.ether-source.distributed'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

from qt_material import QtStyleTools
from Jinja import JinjaMaker
from PlotCheck import PlotCheck
import logging
import re
from ssl import create_default_context
from elasticsearch import Elasticsearch
from datetime import datetime
import time
import pytz
import yaml
import ressources


class GuiLogger(logging.Handler):
    def emit(self, record):
        self.edit.append_line(self.format(record))


class LauncherUi(QMainWindow, QtStyleTools, JinjaMaker, PlotCheck):
    es = None

    def __init__(self):
        """"""
        super().__init__()
        self.p = None
        self.main = QUiLoader().load(':/ui/main.ui', self)

        self.apply_stylesheet(self.main, 'dark_amber.xml')
        self.main.LoadCaCert.clicked.connect(self.OpenFileDirectoryDialog)
        self.main.ModeSombre.stateChanged.connect(self.SwitchUiDesign)

        self.main.LoadCrt.clicked.connect(self.SetChiaCrtPath)
        self.main.LoadKey.clicked.connect(self.SetChiaKeyPath)
        self.main.SmiBinPath.clicked.connect(self.SetSmiBinPath)

        self.main.ChiaEnabled.stateChanged.connect(self.DisplayChiaWidget)
        self.main.SmiEnabled.stateChanged.connect(self.DisplaySmiWidget)
        self.main.TRexEnabled.stateChanged.connect(self.SetTrexEnable)
        self.main.CustomProcessEnabled.stateChanged.connect(self.DisplayCustomProcessWidget)

        self.main.windowsRadio.toggled.connect(self.SetOsIsWindows)
        self.main.LinuxRadio.toggled.connect(self.SetOsIsLinux)

        self.main.GenerateJinja.clicked.connect(self.FillJinjaTemplate)

        self.main.RunPlotCheck.clicked.connect(self.RunPlotCheck)
        self.main.ChiaBinPath.clicked.connect(self.SetChiaBinPath)

        self.main.challengeSlider.valueChanged.connect(self.GetChallengeSliderValue)

    def write_to_es(self, index, body):
        try:
            self.es.index(index=index, body=body)
        except Exception as e:
            print(e)

    def es_connection(self, user, password, es_host):
        # Connect to the elastic cluster
        context = None
        fd = QFile(self.ca_path)
        if fd.open(QIODevice.ReadOnly | QFile.Text):
            context = create_default_context(cadata=QTextStream(fd).readAll())
            fd.close()
        self.es = Elasticsearch(
            [es_host + ":9201", es_host + ":9202", es_host + ":9203"],
            http_auth=(user, password),
            scheme="https",
            ssl_context=context,
        )

    def log_mapping(self, raw):
        return raw

    def epur_str(self, s):
        fd = QFile(':/config/config.yml')
        cred = None
        if fd.open(QIODevice.ReadOnly | QFile.Text):
            cred = yaml.safe_load(QTextStream(fd).readAll())

        self.es_connection(cred['es_username'], cred['es_password'], 'https://grafana.ether-source.fr')
        date_regex = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}.\d{2}.\d{3}'
        cleaned_string = re.sub(date_regex, '', s)
        cleaned_string = cleaned_string.replace("chia.plotting.plot_tools", "")
        cleaned_string = cleaned_string.replace("chia.plotting.check_plots", "")
        cleaned_string = cleaned_string.replace(": INFO", "")
        cleaned_string = re.sub(' +', ' ', cleaned_string)
        log_array = cleaned_string.split('\n')
        testing_plot = {}
        for log in log_array:
            if 'Found plot' in log:
                splited_log = log.split(' ')
                self.countPlot(splited_log[5])
                self.main.Plotcount.setText('{} plots found'.format(self.plot_count))
                self.write_to_es('plot_check', {'plot_name': splited_log[3],
                                                'plot_found': True,
                                                "@timestamp": datetime.fromtimestamp(time.time(), pytz.UTC).isoformat(),
                                                'pseudo': self.main.Username.text()
                                                })
            elif 'valid plots, total size' in log:
                splited_log = log.split(' ')
                self.write_to_es('plot_check', {'total_plot_tested_valid': splited_log[1],
                                                'size tested_valid': splited_log[6],
                                                "@timestamp": datetime.fromtimestamp(time.time(), pytz.UTC).isoformat(),
                                                'pseudo': self.main.Username.text()
                                                })
            elif 'invalid plots found' in log:
                splited_log = log.split(' ')
                self.write_to_es('plot_check', {'total_plot_tested_invalid': splited_log[1],
                                                "@timestamp": datetime.fromtimestamp(time.time(), pytz.UTC).isoformat(),
                                                'pseudo': self.main.Username.text()
                                                })
            elif 'WARNING' in log and log.endswith(".plot"):
                splited_log = log.split(' ')
                self.write_to_es('plot_check', {'invalid_plot_path': splited_log[1],
                                                "@timestamp": datetime.fromtimestamp(time.time(), pytz.UTC).isoformat(),
                                                'pseudo': self.main.Username.text()
                                                })
            elif 'Testing plot' in log:
                splited_log = log.split(' ')
                self.plot_tested = self.plot_tested + 1
                self.tmp_plot_name = splited_log[3]
            elif 'Proofs' in log:
                splited_log = log.split(' ')
                testing_plot['proof_found'] = int(splited_log[2])
                testing_plot['proof_challenge'] = int(splited_log[4].replace(',', ''))
                testing_plot['time_checked'] = float(splited_log[5])
                testing_plot['pseudo'] = self.main.Username.text()
                testing_plot['plot_tested'] = True
                testing_plot['plot_name'] = self.tmp_plot_name
                testing_plot["@timestamp"] = datetime.fromtimestamp(time.time(), pytz.UTC).isoformat()
                self.main.PlotChecked.setText('{} plots checked'.format(self.plot_tested))
                self.write_to_es('plot_check', testing_plot)
                testing_plot = {}
            elif 'Loaded a total' in log:
                splited_log = log.split(' ')
                self.write_to_es('plot_check', {'plots_count': int(splited_log[5]),
                                                'count_time': float(splited_log[12]),
                                                'plots_size': float(splited_log[9]),
                                                'pseudo': self.main.Username.text(),
                                                "@timestamp": datetime.fromtimestamp(time.time(), pytz.UTC).isoformat()})
        return cleaned_string

    def message(self, s):
        s = s.replace('[32m', '')
        s = s.replace('[33m', '')
        s = s.replace('[0m', '')
        s = self.epur_str(s)
        self.log_mapping(s)
        self.main.PLotCheckLogText.appendPlainText("{}".format(self.log_mapping(s)))

    def RunPlotCheck(self):
        self.p = QProcess()
        self.p.readyReadStandardOutput.connect(self.handle_stdout)
        self.p.readyReadStandardError.connect(self.handle_stderr)
        self.p.stateChanged.connect(self.handle_state)
        self.p.finished.connect(self.process_finished)
        self.p.start("{}".format(self.chia_bin_path[0]), ["plots", "check", "-n", "{}".format(self.challenge)])
        self.OpenGrafanaUrl()

    def GetChallengeSliderValue(self, state):
        self.challenge = self.main.challengeSlider.value()
        self.main.challengeLabel.setText("Nombre de challenge : {}".format(self.challenge))

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        self.message("Processus plot check: {}".format(states[state]))

    def process_finished(self):
        self.message("Plot check terminé ! :)")
        self.p = None

    def DisplayChiaWidget(self, state):
        self.main.ChiaWidget.setHidden(not state)
        self.SetCollectChiaEnable(state)

    def DisplaySmiWidget(self, state):
        self.main.SMIWidget.setHidden(not state)
        self.SetSmiEnable(state)

    def DisplayCustomProcessWidget(self, state):
        self.main.CustomProcessWidget.setHidden(not state)
        self.SetCustomProcessEnable(state)

    def FillJinjaTemplate(self):
        self.SetEsUsername(self.main.UsernameEs.text())
        self.SetEsPassword(self.main.PasswordEs.text())
        self.SetCustomName(self.main.CustomName.text())
        if self.GetCollectChiaEnable():
            self.SetLaucherId(self.main.LauncherId.text())
        if self.GetCustomProcessEnable():
            self.AppendToProcessList(self.main.ProcessInput.text())
        self.GenerateTemplate()

    def button_clicked(self):
        dialog = QFileDialog()
        ca_dir = dialog.getExistingDirectory(self)
        self.main.CaDisplayPath.setText(ca_dir)

    def OpenFileDirectoryDialog(self):
        dialog = QFileDialog()
        ca_dir = dialog.getExistingDirectory(self)
        self.main.CaDisplayPath.setText(ca_dir)

    def SwitchUiDesign(self, state):
        if (Qt.Checked == state):
            self.apply_stylesheet(self.main, 'dark_amber.xml')
        else:
            self.apply_stylesheet(self.main, 'light_amber.xml')


if __name__ == "__main__":
    app = QApplication()
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon(':/ico/lfdm.ico'))
    frame = LauncherUi()
    frame.main.ChiaWidget.setHidden(True)
    frame.main.SMIWidget.setHidden(True)
    frame.main.CustomProcessWidget.setHidden(True)
    frame.main.show()
    app.exec()
