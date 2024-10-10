from os import path, environ
from pydm import Display, PyDMApplication
from pydm.widgets import PyDMRelatedDisplayButton
from qtpy.QtWidgets import QHBoxLayout, QFileDialog, QPushButton
import subprocess
import mc_mad_pv_names


'''
This file is in charge of the GUI for the Provide File Screen of the General Motion Calibration Tool.
To execute this file, call the terminal command "pydm -m '{"MAD":"[MAD]","MOTOR":"[MOTOR]"}' mc_motor_calibration_provide_file.py",
where [MOTOR] is the device's control system name without any attribute and [MAD] is the oracle device name. An example would be pydm -m '{"MAD":"CE21334,"MOTOR":"COLL:LI21:334"}' mc_motor_calibration_provide_file.py.
This is the top of the 'flow' for the General Motion Calibration Tool. From this screen, the user is able to access
the Step Size Screen and the Main Screen.
'''

class ProvideFileDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(ProvideFileDisplay, self).__init__(parent=parent, args=args, macros=macros)

        '''Set initial size of main window'''
        self.resize(325, 325) 

        self.device_name = macros.get("MOTOR")
        self.mad_name = macros.get("MAD")

        '''Set the window title'''
        self.setWindowTitle('LVDT Calibration - {}'.format(self.device_name))

        '''Set the user interface title'''
        self.TitleLabel.setText(("General Motion LVDT Calibration - {}").format(self.device_name))

        self.ui.HeaderLabel.setText('Find a .csv file with calibration data or continue with no file.\nIF no file is selected, motor will be moved through its range at selected intervals and data from motor and LVDT will be collected and a polynomial fit will be generated.\nFile currently selected: None')

        '''Set up the button that opens a QFileDIalog'''
        self.findFileButton = QPushButton()
        self.findFileButton.setText('Find a file')
        self.findFileButton.setStyleSheet("background-color: #9fc3f5")
        self.findFileButton.clicked.connect((lambda: self.open_file_dialog()))

        '''Set up the button that continues to the main display w/ selected file'''
        self.fileButton = QPushButton()
        self.fileButton.setText('Continue with selected file')
        self.fileButton.clicked.connect((lambda: self.file_provided()))
        self.fileButton.setStyleSheet("background-color: #9fc3f5")

        '''Set up the button that continues to the step size display w/ no selected file '''
        self.noFileButton = PyDMRelatedDisplayButton(parent=None, filename='mc_motor_calibration_step_size')
        self.noFileButton.setText('Continue with no file')
        self.noFileButton.macros = ['{"MAD":"' + self.mad_name + '"}','{"MOTOR":"' + self.device_name + '"}']
        self.noFileButton.setStyleSheet("background-color: #9fc3f5")

        '''For formatting purposes'''    
        self.setup_sublayout()
        self.ui.fileDialog_layout.addWidget(self.noFileButton)

    '''When the fileButton is clicked, a subprocess is launched to open main display'''
    def file_provided(self):
        self.next_file = environ.get("TOOLS") + "/script/mc_lvdt_calibration/mc_motor_calibration_main.py" 
        subprocess.call(['python', self.next_file, self.device_name, self.mad_name, self.filename])

    def setup_sublayout(self):
        self.sublayout = QHBoxLayout()
        self.sublayout.addWidget(self.findFileButton)
        self.sublayout.addWidget(self.fileButton)
        self.ui.fileDialog_layout.addLayout(self.sublayout)  

    '''When the findFileButton is clicked, QFileDialog is opened'''
    def open_file_dialog(self):
        self.fileDialog = QFileDialog()
        self.fileDialog.setNameFilter("*.csv")
        self.fileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        self.selected = self.fileDialog.exec()
        # Saves the selected file and displays the name to the screen
        if self.selected:
            self.filename = self.fileDialog.selectedFiles()[0]
            self.ui.HeaderLabel.setText('Find a .csv file with calibration data or continue with no file.\nFile currently selected: {}'.format(self.filename))
            self.fileButton.macros = ['{"MAD":"' + self.mad_name + '", "FILENAME":"' + self.filename + '"}']
            print(self.filename)

    def ui_filename(self):
        return 'mc_motor_calibration_provide_file.ui'
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

class MainScreen(PyDMApplication):
    def __init__(self, ui_file=None, macros=None):
        super(MainScreen, self).__init__(ui_file='mc_motor_calibration_provide_file', macros=macros)
    
