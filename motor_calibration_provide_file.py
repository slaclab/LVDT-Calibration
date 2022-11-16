from os import path
from pydm import Display, PyDMApplication
from pydm.widgets import PyDMRelatedDisplayButton
from qtpy.QtWidgets import QHBoxLayout, QFileDialog, QPushButton
import subprocess

'''
This file is in charge of the GUI for the Provide File Screen of the General Motion Calibration Tool.
To execute this file, call the terminal command "pydm -m '{"MAD":"[MAD]"}' motor_calibration_provide_file.py",
where [MAD] is the device's short name. An example would be pydm -m '{"MAD":"CEDOG-POSY"}' motor_calibration_provide_file.py.
This is the top of the 'flow' for the General Motion Calibration Tool. From this screen, the user is able to access
the Step Size Screen and the Main Screen.
'''

devices_long_to_short = { 
'USEG:HTR:650':'UMHTR',
'WIRE:DIAG0:424':'WSDG01',
'COLL:HTR:615:POSX': 'CEHTR-POSX' ,
'COLL:HTR:615:NEGX': 'CEHTR-NEGX' ,
'COLL:COL0:390:NEGY':'CYC01-NEGY' ,
'COLL:COL0:390:POSY':'CYC01-POSY' ,
'COLL:COL0:470:NEGX':'CXC01-NEGX' ,
'COLL:COL0:470:POSX':'CXC01-POSX' ,
'COLL:COL0:710:POSY':'CYC03-POSY' ,
'COLL:COL0:710:NEGY':'CYC03-NEGY' ,
'COLL:COL0:790:NEGX':'CXC03-NEGX' ,
'COLL:COL0:790:POSX':'CXC03-POSX' ,
'COLL:BC1B:450:POSX':'CE11B-POSX' ,
'COLL:BC1B:450:NEGX':'CE11B-NEGX' ,
'COLL:COL1:390:NEGX':'CYC11-NEGY' ,
'COLL:COL1:390:POSX':'CYC11-POSY' ,
'COLL:COL1:470:NEGX':'CXC11-NEGX' ,
'COLL:COL1:470:POSX':'CXC11-POSX' ,
'COLL:COL1:710:NEGY':'CYC13-NEGY' ,
'COLL:COL1:710:POSY':'CYC13-POSY' ,
'COLL:COL1:790:NEGX':'CXC13-NEGX' ,
'COLL:COL1:790:POSX':'CXC13-POSX' ,
'COLL:BC2B:535:POSX':'CE21B-POSX' ,
'COLL:BC2B:535:NEGX':'CE21B-NEGX' ,
'COLL:DOG:131:POSY':'CEDOG-POSY' ,
'COLL:DOG:131:NEGY':'CEDOG-NEGY' ,
'COLL:BPN21:424:NEGX':'CXBP21-NEGX' ,
'COLL:BPN21:424:POSX':'CXBP21-POSX' ,
'COLL:BPN22:424:NEGY':'CYBP22-NEGY' ,
'COLL:BPN22:424:POSY':'CYBP22-POSY' ,
'COLL:BPN25:424:NEGX':'CXBP25-NEGX' ,
'COLL:BPN25:424:POSX':'CXBP25-POSX' ,
'COLL:BPN22:424:NEGY':'CYBP26-NEGY' ,
'COLL:BPN22:424:POSY':'CYBP26-POSY' ,
'COLL:LI24:805': 'CE24805' ,
'COLL:LTUS:372:NEGX':'CEDL17-NEGX' ,
'WIRE:LI24:705':'WS24' ,
'WIRE:IN10:561':'WS10561' ,
'WIRE:LI11:444':'WS11444' ,
'COLL:LI11:334:L':'CE11334L' ,
'COLL:LI11:334:R':'CE11334R' ,
'WIRE:LI11:614' :'WS11614',
'WIRE:LI11:744':'WS11744' ,
'WIRE:LI12:214':'WS12214' ,
'COLL:LI14:802:L':'CE14802L' ,
'COLL:LI14:802:R':'CE14802R' ,
'WIRE:LI18:944':'WS18944' , 
'WIRE:LI19:144':'WS19144' , 
'WIRE:LI19:244':'WS19244' , 
'WIRE:LI19:344':'WS19344' , 
'WIRE:LI11:612':'WS11612' , 
'COLL:LI19:960:L':'CX1896L' ,
'COLL:LI18:960:R':'CX1896R' ,
'COLL:LI18:960:T':'CY1896T' ,
'COLL:LI18:960:B':'CY1896B' ,
'WIRE:LI20:3179' :'IPWS1',
'WIRE:LI20:3206':'IPWS2' ,
'WIRE:LI20:3229':'IPWS3' ,
'WIRE:LI20:3252':'IPWS4' ,
'COLL:LI20:2085':'C202085' ,
'COLL:LI20:2086':'C202086' ,
'COLL:LI20:2069':'C202069' ,
'COLL:LI20:2070':'C202070' ,
'COLL:LI20:2072':'C202072' ,
'COLL:LI20:2073':'C202073' ,
'OTRS:LI20:3158':'USOTR' ,
'OTRS:LI20:3206':'DSOTR',
'WIRE:IN20:741':'WS04' , 
'WIRE:LI21:285':'WS11' , 
'WIRE:LI21:293':'WS12' , 
'WIRE:LI21:301':'WS13' , 
'WIRE:LI24:705':'WS24' , 
'WIRE:LI27:644':'WS644' , 
'WIRE:LI28:144':'WS144' , 
'WIRE:LI28:444':'WS444' , 
'WIRE:LI28:744':'WS744' , 
}

class ProvideFileDisplay(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(ProvideFileDisplay, self).__init__(parent=parent, args=args, macros=macros)

        self.device_long_name = macros.get("P")
        self.device_short_name = devices_long_to_short.get(self.device_long_name)
        # self.device_short_name = macros.get("MAD")
        # print(self.device_short_name)
        self.TitleLabel.setText(("General Motion Calibration - {}").format(self.device_short_name))
        self.ui.HeaderLabel.setText('Find a .csv file with calibration data or continue with no file.\nFile currently selected: None')

        '''Set up the button that opens a QFileDIalog'''
        self.findFileButton = QPushButton()
        self.findFileButton.setText('Find a file.')
        self.findFileButton.setStyleSheet("background-color: #9fc3f5")
        self.findFileButton.clicked.connect((lambda: self.open_file_dialog()))

        '''Set up the button that continues to the main display w/ selected file'''
        self.fileButton = QPushButton()
        self.fileButton.setText('Continue with selected file.')
        self.fileButton.clicked.connect((lambda: self.file_provided()))
        self.fileButton.setStyleSheet("background-color: #9fc3f5")

        '''Set up the button that continues to the step size display w/ no selected file '''
        self.noFileButton = PyDMRelatedDisplayButton(parent=None, filename='motor_calibration_step_size')
        self.noFileButton.setText('Continue with no file')
        self.noFileButton.macros = ['{"MAD":"' + self.device_short_name + '"}']
        self.noFileButton.setStyleSheet("background-color: #9fc3f5")

        '''For formatting purposes'''    
        self.setup_sublayout()
        self.ui.fileDialog_layout.addWidget(self.noFileButton)

    '''When the fileButton is clicked, a subprocess is launched to open main display'''
    def file_provided(self):
            subprocess.call(['python', '/afs/slac.stanford.edu/u/cd/sarahvo/calibration_workspace/motor_calibration_main_2.py', self.device_short_name, self.filename])

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
            self.fileButton.macros = ['{"MAD":"' + self.device_short_name + '", "FILENAME":"' + self.filename + '"}']
            print(self.filename)

    def ui_filename(self):
        return 'motor_calibration_provide_file.ui'
    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

class MainScreen(PyDMApplication):
    def __init__(self, ui_file=None, macros=None):
        super(MainScreen, self).__init__(ui_file='motor_calibration_provide_file', macros=macros)
    
