from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QFileDialog
from subprocess import check_output
import sys


class PlotCheck:
    chia_bin_path = None
    plot_count = 0
    plot_tested = 0
    proof = 0
    warning = 0
    k32_num = 0
    k33_num = 0
    k34_num = 0
    k35_num = 0
    ca_path = ':/cafile/ether-source.pem'
    tmp_plot_name = ''

    def __init__(self):
        pass

    def SetChiaBinPath(self):
        self.chia_bin_path = QFileDialog.getOpenFileName()
        #self.chia_bin_path = ('C:/Users/flori/Desktop/chia-blockchain/app-1.1.2/resources/app.asar.unpacked/daemon/chia.exe', 'test')

    def countPlot(self, type):
        self.plot_count += 1
        if type == 'k32':
            self.k32_num += 1
        elif type == 'k33':
            self.k33_num += 1
        elif type == 'k34':
            self.k34_num += 1
        elif type == 'k35':
            self.k35_num += 1
