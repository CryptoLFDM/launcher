from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Slot, Qt

from qt_material import QtStyleTools
from Jinja import JinjaMaker


########################################################################
class LauncherUi(QMainWindow, QtStyleTools, JinjaMaker):
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

        self.main.ChiaEnabled.stateChanged.connect(self.DisplayChiaWidget)
        self.main.SmiEnabled.stateChanged.connect(self.DisplaySmiWidget)
        self.main.TRexEnabled.stateChanged.connect(self.SetTrexEnable)
        self.main.CustomProcessEnabled.stateChanged.connect(self.DisplayCustomProcessWidget)

        self.main.windowsRadio.toggled.connect(self.SetOsIsWindows)
        self.main.LinuxRadio.toggled.connect(self.SetOsIsLinux)

        self.main.GenerateJinja.clicked.connect(self.FillJinjaTemplate)

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
        print(self.es_username)
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
    frame = LauncherUi()
    frame.main.ChiaWidget.setHidden(True)
    frame.main.SMIWidget.setHidden(True)
    frame.main.CustomProcessWidget.setHidden(True)
    frame.main.show()
    app.exec()
