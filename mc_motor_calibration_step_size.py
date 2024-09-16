from os import path, environ
from pydm import Display, PyDMApplication
# import calibrate_motor_lvdt_modified
import epics
from qtpy.QtWidgets import QPushButton
import subprocess

'''
This file is in charge of the GUI for the Step Size Screen of the General Motion Calibration Tool. In order to execute
this file, call the terminal command "pydm -m '{"MAD":"[MAD]","MOTOR":"[MOTOR]"}' motor_calibration_step_size.py", where [MAD] is the device's
MAD name and [MOTOR] is device's control system name without any attribute. An example would be pydm -m '{"MAD":"CEDOG-POSY","MOTOR":"COLL:DOG:655:POSY"}' motor_calibration_step_size.py.
'''

class ProvideStepSizeDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(ProvideStepSizeDisplay, self).__init__(parent=parent, args=args, macros=macros)

        '''Set initial title of step size window'''
        self.setWindowTitle('LVDT Calibration - {}'.format(macros.get("MAD")))

        self.mad_name = macros.get("MAD")
        self.device_name = macros.get("MOTOR")
        self.egu = ''.join((self.device_name, ':MOTR.EGU'))

        '''Connect Spin Box to MOTR.TWV channel'''
        self.PyDMSpinbox.channel = "ca://{}:MOTR.TWV".format(self.device_name)

        self.TitleLabel.setText(("General Motion Calibration - {}").format(self.mad_name))
        self.PyDMLabel.setText(("Provide a step size in {}. This will be the interval at which data will be collected.\nTo proceed, you must first press ENTER on the keyboard and then click NEXT.").format(epics.caget('{}'.format(self.egu))))
        
        self.macros_string = '{"MAD":"' + macros.get("MAD") + '"}'

        '''Set up the button to go to the main display'''
        self.next_button = QPushButton()
        self.next_button.setText("Next")
        self.next_button.setStyleSheet("background-color: #9fc3f5")
        self.next_button.clicked.connect(lambda: self.next_display())
        self.ui.horizontalLayout.addWidget(self.next_button)

    '''When button is pressed, subprocess is launched to open main screen'''
    def next_display(self):
        self.next_file = environ.get("TOOLS") + "/script/mc_lvdt_calibration/mc_motor_calibration_main.py" 
        subprocess.call(['python', self.next_file , self.mad_name , self.device_name])

    def ui_filename(self):
        return 'mc_motor_calibration_step_size.ui'
        
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

class MainScreen(PyDMApplication):
    def __init__(self, ui_file=None, macros=None):
        super(MainScreen, self).__init__(ui_file='mc_motor_calibration_main.py', macros=macros)
