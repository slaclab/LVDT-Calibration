from os import path
from pydm import Display, PyDMApplication
# import calibrate_motor_lvdt_modified
import epics
from qtpy.QtWidgets import QPushButton
import subprocess
import mc_mad_pv_names

'''
This file is in charge of the GUI for the Step Size Screen of the General Motion Calibration Tool. In order to execute
this file, call the terminal command "pydm -m '{"MAD":"[MAD]"}' motor_calibration_step_size.py", where [MAD] is the device's
short name. An example would be pydm -m '{"MAD":"CEDOG-POSY"}' motor_calibration_step_size.py.
'''

class ProvideStepSizeDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(ProvideStepSizeDisplay, self).__init__(parent=parent, args=args, macros=macros)

        self.device_short_name = macros.get("MAD")
        self.device_name = mc_mad_pv_names.devices_mad_to_pv_name.get(macros.get("MAD"))
        self.egu = ''.join((self.device_name, ':MOTR.EGU'))

        '''Connect Spin Box to MOTR.TWV channel'''
        self.PyDMSpinbox.channel = "ca://{}:MOTR.TWV".format(self.device_name)

        self.TitleLabel.setText(("General Motion Calibration - {}").format(macros.get("MAD")))
        self.PyDMLabel.setText(("Provide a step size in {}. To proceed, you must first hit ENTER on the keyboard and then click NEXT.").format(epics.caget('{}'.format(self.egu))))
        
        self.macros_string = '{"MAD":"' + macros.get("MAD") + '"}'

        '''Set up the button to go to the main display'''
        self.next_button = QPushButton()
        self.next_button.setText("Next")
        self.next_button.setStyleSheet("background-color: #9fc3f5")
        self.next_button.clicked.connect(lambda: self.next_display())
        self.ui.horizontalLayout.addWidget(self.next_button)

    '''When button is pressed, subprocess is launched to open main screen'''
    def next_display(self): 
        subprocess.call(['python', '/usr/local/lcls/tools/pydm/display/mc/LVDT-Calibration/mc_motor_calibration_main.py', self.device_short_name])

    def ui_filename(self):
        return 'mc_motor_calibration_step_size.ui'
        
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

class MainScreen(PyDMApplication):
    def __init__(self, ui_file=None, macros=None):
        super(MainScreen, self).__init__(ui_file='mc_motor_calibration_main.py', macros=macros)
