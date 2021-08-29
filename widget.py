from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Slot, Qt

from qt_material import QtStyleTools
from Jinja import JinjaMaker


########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleTools, JinjaMaker):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
        self.main = QUiLoader().load('main.ui', self)

        self.apply_stylesheet(self.main, 'dark_amber.xml')
        self.main.LoadCaCert.clicked.connect(self.OpenFileDirectoryDialog)
        self.main.ModeSombre.stateChanged.connect(self.SwitchUiDesign)

        self.main.LoadCrt.clicked.connect(self.SetChiaCrtPath)
        self.main.LoadKey.clicked.connect(self.SetChiaKeyPath)
        self.main.SmiBinPath.clicked.connect(self.SetSmiBinPath)

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
    frame = RuntimeStylesheets()
    frame.main.show()
    app.exec()
