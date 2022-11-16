from os import path
from pydm import Display, PyDMApplication
# import calibrate_motor_lvdt_modified
import epics
from qtpy.QtWidgets import QPushButton
import subprocess

'''
This file is in charge of the GUI for the Step Size Screen of the General Motion Calibration Tool. In order to execute
this file, call the terminal command "pydm -m '{"MAD":"[MAD]"}' motor_calibration_step_size.py", where [MAD] is the device's
short name. An example would be pydm -m '{"MAD":"CEDOG-POSY"}' motor_calibration_step_size.py.
'''

devices_short_to_long = { 
'UMHTR':'USEG:HTR:650' ,
'WSDG01':'WIRE:DIAG0:424' ,
'CEHTR-POSX':'COLL:HTR:615:POSX' ,
'CEHTR-NEGX':'COLL:HTR:615:NEGX' ,
'CYC01-NEGY':'COLL:COL0:390:NEGY' ,
'CYC01-POSY':'COLL:COL0:390:POSY' ,
'CXC01-NEGX':'COLL:COL0:470:NEGX' ,
'CXC01-POSX':'COLL:COL0:470:PO# SX' ,
'CYC03-POSY':'COLL:COL0:710:POSY' ,
'CYC03-NEGY':'COLL:COL0:710:NEGY' ,
'CXC03-NEGX':'COLL:COL0:790:NEGX' ,
'CXC03-POSX':'COLL:COL0:790:POSX' ,
'CE11B-POSX':'COLL:BC1B:450:POSX' ,
'CE11B-NEGX':'COLL:BC1B:450:NEGX' ,
'CYC11-NEGY':'COLL:COL1:390:NEGX' ,
'CYC11-POSY':'COLL:COL1:390:POSX' ,
'CXC11-NEGX':'COLL:COL1:470:NEGX' ,
'CXC11-POSX':'COLL:COL1:470:POSX' ,
'CYC13-NEGY':'COLL:COL1:710:NEGY' ,
'CYC13-POSY':'COLL:COL1:710:POSY' ,
'CXC13-NEGX':'COLL:COL1:790:NEGX' ,
'CXC13-POSX':'COLL:COL1:790:POSX' ,
'CE21B-POSX':'COLL:BC2B:535:POSX' ,
'CE21B-NEGX':'COLL:BC2B:535:NEGX' ,
'CEDOG-POSY':'COLL:DOG:131:POSY' ,
'CEDOG-NEGY':'COLL:DOG:131:NEGY' ,
'CXBP21-NEGX':'COLL:BPN21:424:NEGX' ,
'CXBP21-POSX':'COLL:BPN21:424:POSX' ,
'CYBP22-NEGY':'COLL:BPN22:424:NEGY' ,
'CYBP22-POSY':'COLL:BPN22:424:POSY' ,
'CXBP25-NEGX':'COLL:BPN25:424:NEGX' ,
'CXBP25-POSX':'COLL:BPN25:424:POSX' ,
'CYBP26-NEGY':'COLL:BPN22:424:NEGY' ,
'CYBP26-POSY':'COLL:BPN22:424:POSY' ,
'CE24805':'COLL:LI24:805' ,
'CEDL17-NEGX':'COLL:LTUS:372:NEGX' ,
'WS24':'WIRE:LI24:705' ,
'WS10561':'WIRE:IN10:561' ,
'WS11444':'WIRE:LI11:444' ,
'CE11334L':'COLL:LI11:334:L' ,
'CE11334R':'COLL:LI11:334:R' ,
'WS11614':'WIRE:LI11:614' ,
'WS11744':'WIRE:LI11:744' ,
'WS12214':'WIRE:LI12:214' ,
'CE14802L':'COLL:LI14:802:L' ,
'CE14802R':'COLL:LI14:802:R' ,
'WS18944':'WIRE:LI18:944' , 
'WS19144':'WIRE:LI19:144' , 
'WS19244':'WIRE:LI19:244' , 
'WS19344':'WIRE:LI19:344' , 
'WS11612':'WIRE:LI11:612' , 
'CX1896L':'COLL:LI19:960:L' ,
'CX1896R':'COLL:LI18:960:R' ,
'CY1896T':'COLL:LI18:960:T' ,
'CY1896B':'COLL:LI18:960:B' ,
'IPWS1':'WIRE:LI20:3179' ,
'IPWS2':'WIRE:LI20:3206' ,
'IPWS3':'WIRE:LI20:3229' ,
'IPWS4':'WIRE:LI20:3252' ,
'C202085':'COLL:LI20:2085' ,
'C202086':'COLL:LI20:2086' ,
'C202069':'COLL:LI20:2069' ,
'C202070':'COLL:LI20:2070' ,
'C202072':'COLL:LI20:2072' ,
'C202073':'COLL:LI20:2073' ,
'USOTR':'OTRS:LI20:3158' ,
'DSOTR':'OTRS:LI20:3206' ,
'WS04':'WIRE:IN20:741' , 
'WS11':'WIRE:LI21:285' , 
'WS12':'WIRE:LI21:293' , 
'WS13':'WIRE:LI21:301' , 
'WS24':'WIRE:LI24:705' , 
'WS644':'WIRE:LI27:644' , 
'WS144':'WIRE:LI28:144' , 
'WS444':'WIRE:LI28:444' , 
'WS744':'WIRE:LI28:744' , 
}

class ProvideStepSizeDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(ProvideStepSizeDisplay, self).__init__(parent=parent, args=args, macros=macros)

        self.device_short_name = macros.get("MAD")
        self.device_name = devices_short_to_long.get(macros.get("MAD"))
        self.egu = ''.join((self.device_name, ':MOTR.EGU'))

        '''Connect Spin Box to MOTR.TWV channel'''
        self.PyDMSpinbox.channel = "ca://{}:MOTR.TWV".format(self.device_name)


        self.TitleLabel.setText(("General Motion Calibration - {}").format(macros.get("MAD")))
        self.PyDMLabel.setText(("Provide a step size in {}. To proceed, hit enter and then click next.").format(epics.caget('{}'.format(self.egu))))
        
        self.macros_string = '{"MAD":"' + macros.get("MAD") + '"}'

        '''Set up the button to go to the main display'''
        self.next_button = QPushButton()
        self.next_button.setText("Next")
        self.next_button.setStyleSheet("background-color: #9fc3f5")
        self.next_button.clicked.connect(lambda: self.next_display())
        self.ui.horizontalLayout.addWidget(self.next_button)

    '''When button is pressed, subprocess is launched to open main screen'''
    def next_display(self): 
        subprocess.call(['python', '/afs/slac.stanford.edu/u/cd/sarahvo/calibration_workspace/motor_calibration_main_2.py', self.device_short_name])

    def ui_filename(self):
        return 'motor_calibration_step_size.ui'
        
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

class MainScreen(PyDMApplication):
    def __init__(self, ui_file=None, macros=None):
        super(MainScreen, self).__init__(ui_file='motor_calibration_main_2.py', macros=macros)
