import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys

from pydm import Display
from pydm.widgets import PyDMLabel

import sys
import epics
import time
import datetime
import os
import csv

from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QApplication
from qtpy import QtWidgets

import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
#from colorama import Fore, Back, Style
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt#from colorama import Fore, Back, Style
import meme.names

'''
This file sets up the GUI for the main display for the General Motion Calibration Tool. It is also responsible for
the execution of the data collection and data analysis. This file utilizes multithreading in order to properly handle
real time GUI updates during motor movement. To execute this screen on its own, enter the terminal command
'python motor_calibration_main_2.py [MAD]', where [MAD] is the device's name (one of the short names on the left side
of the devices list below). 
*Warning: Execution of this screen alone does not allow you to provide a .csv file or step size. In order to provide such
information for the program, call one of the prior screens of the 'flow'.*
*Warning: Pushing 1 to extract all for collimators was deleted from this file and, if to be readded, must also be tested.*
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

'''
 Defines the signals available from a running worker thread.
'''
class WorkerSignals(QObject):
 
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

'''
Worker thread:Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
'''
class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit() # Done

class MainWindow(Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(MainWindow, self).__init__(parent=parent, args=args, macros=macros)

        # [EDIT FOR YOUR PERSONAL CONFIGURATIONS] Global Variable that holds the directory where data is to be saved
        self.path = '/u/gu/allyc/work/project' # During testing, this was /u/gu/allyc/work/project. Should be $PHYSICS_DATA/genMotion/lvdtCal or whatever user wants it to be

        # Variables to be used throughout UI
        self.device_short_name = macros.get("MAD")
        self.device_name = devices_short_to_long.get(self.device_short_name)
        self.motor_egu = epics.caget(('{}:MOTR.EGU').format(self.device_name))
        self.lvraw_egu = epics.caget(('{}:LVRAW.EGU').format(self.device_name))
        self.motor_twv = epics.caget(('{}:MOTR.TWV').format(self.device_name))
        self.motor_hlm = ''.join((self.device_name, ':MOTR.HLM'))
        self.motor_llm =''.join((self.device_name, ':MOTR.LLM'))
        self.filename = macros.get("FILENAME")
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

        # Set up header according to whether or not data collection will occur
        if ("FILENAME" in macros):
            self.filename = macros.get("FILENAME")
            self.csv_file = open(self.filename)
            self.header_text_1 = "File {} provided. Press 'Start Data Analysis' button to continue".format(self.filename)
            self.header_text_2 = " "
        else:
            self.filename = '{}_{}.csv'.format(self.device_name, self.timestamp)
            self.csv_file = os.path.join(self.path, self.filename)
            # Handle the case that device is a collimator and display must show both positive and negative motors
            if ((self.device_name)[:4] == 'COLL'):
                x_or_y = self.device_name[-1]
                pos_or_neg = ''
                if (self.device_name[-4:-1] == 'POS'):
                    pos_or_neg = 'NEG'
                else: pos_or_neg = 'POS'
                self.other_motor =     self.device_name[:-4] + pos_or_neg + x_or_y
                self.header_text_1 =  'No input file specified. Data will be collected at every {} {}. Data will be saved to {}. Calibration data is saved in {}. High and Low limits will be saved and restored at the end of data collections.'.format(self.motor_twv, self.motor_egu, self.filename, self.path)
                self.header_text_2 = 'Save High Limit value: {}\nSave Low Limit value: {}\nPrevious POS motor position: {} {} \nPrevious NEG motor position: {} {}'.format(epics.caget('{}:MOTR.HLM'.format(self.device_name)), epics.caget('{}:MOTR.LLM'.format(self.device_name)), epics.caget('{}:MOTR.RBV'.format(self.device_name)), self.motor_egu, epics.caget('{}:MOTR.RBV'.format(self.other_motor)), self.motor_egu)
            else:
                self.header_text_1 = 'No input file specified. Data will be collected at every {} {}. Data will be saved to {}. Calibration data is saved in $PHYSICS_DATA/genMotion/lvdtCal. High and Low limits will be saved and restored at the end of data collections.'.format(self.motor_twv, self.motor_egu, self.filename)
                self.header_text_2 = 'Save High Limit value: {} \nSave Low Limit value: {}\nPrevious motor position: {} {}'.format(epics.caget('{}:MOTR.HLM'.format(self.device_name)), epics.caget('{}:MOTR.LLM'.format(self.device_name)), epics.caget('{}:MOTR.RBV'.format(self.device_name)), self.motor_egu)

        # Intialize the main status label
        self.main_status = QLabel("Data collection has not begun yet.")

        # Initalize the button that starts data collection
        self.collection_button = QPushButton("Start Data Collection.")
        self.collection_button.setStyleSheet("background-color: #9fc3f5")
        self.collection_button.pressed.connect(self.data_collection)

        # Initialize the button that starts data analysis
        self.analysis_button = QPushButton()
        self.analysis_button.setText("Start Data Analysis.")
        self.analysis_button.setStyleSheet("background-color: #9fc3f5")
        self.analysis_button.clicked.connect(lambda: self.data_analysis())

        # Initalize the error analysis table
        self.err_table = QTableWidget()
        self.err_table.setRowCount(6)
        self.err_table.setColumnCount(4)
        for i in range(6):
            for j in range(4):
                self.err_table.setItem(i, j, QTableWidgetItem("N/A"))
        self.err_table.horizontalHeader().setStretchLastSection(True)
        self.err_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setup_ui()
        self.show()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Set up frame
        self.frame = QFrame()
        self.frame.setStyleSheet("QFrame#frame{\n"
"    border: 1px solid: #FF17365D;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_layout = QtWidgets.QVBoxLayout(self.frame)
        self.main_layout.addWidget(self.frame)

        self.setup_title()
        self.setup_header()
        # self.frame_layout.addWidget(self.main_status)
        self.frame_layout.addWidget(self.collection_button)
        self.setup_statuses()
        self.frame_layout.addWidget(self.analysis_button)
        self.sublayout = QHBoxLayout()
        self.frame_layout.addLayout(self.sublayout)
        self.setup_degrees()
        self.setup_coefs()
        self.setup_default_err()

    '''Setup the general title shared between all three screens'''
    def setup_title(self):
        self.title = PyDMLabel()
        title_text = 'General Motion Calibration - {}'.format(macros.get("MAD"))
        self.title.setText(title_text)
        
        self.title.setStyleSheet("QLabel {\n"
                                 " qproperty-alignment:AlignCenter;\n"
                                 " border: 1px solid #FF17365D;\n"
                                 " border-top-left-radius: 15px;\n"
                                 " border-top-right-radius: 15px;\n"
                                 " background-color: #FF17365D;\n"
                                 " padding: 5px 0px;\n"
                                 " color: rgb(255, 255, 255);\n"
                                 " max-height: 25px;\n"
                                 " font-size: 14px;\n"
                                 "}")
                                 
        self.frame_layout.addWidget(self.title)    

    '''Set up header labels based on texts previously initialized'''
    def setup_header(self):
        self.header_label_1 = self.create_label(self.frame_layout, self.header_text_1, True)
        self.header_label_1.setWordWrap(True)
        self.header_label_2 = self.create_label(self.frame_layout, self.header_text_2)

    '''Set up labels that show the status of data collection, MoVAL, LVRAW, and RBV'''
    def setup_statuses(self):
        self.left_layout = QVBoxLayout()
        self.main_status.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.status_label = PyDMLabel()
        self.status_label.setText('Data Collection Status:')
        self.status_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.left_layout.addWidget(self.status_label)
        self.moval_label = PyDMLabel()
        self.moval_label.setText('MoVAL ({}):'.format(self.motor_egu))
        self.moval_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.left_layout.addWidget(self.moval_label)
        self.lvraw_label = PyDMLabel()
        self.lvraw_label.setText('LVRAW ({}):'.format(self.lvraw_egu))
        self.lvraw_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.left_layout.addWidget(self.lvraw_label)
        self.rbv_label = PyDMLabel()
        self.rbv_label.setText('RBV ({}):'.format(self.motor_egu))
        self.rbv_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.left_layout.addWidget(self.rbv_label)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.main_status)
        self.moval_status = PyDMLabel()
        self.moval_status.channel = "ca://{}:MOTR.VAL".format(self.device_name)
        self.moval_status.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.right_layout.addWidget(self.moval_status)
        self.lvraw_status = PyDMLabel()
        self.lvraw_status.channel = "ca://{}:LVRAW".format(self.device_name)
        self.lvraw_status.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.right_layout.addWidget(self.lvraw_status)
        self.rbv_status = PyDMLabel()
        self.rbv_status.channel = "ca://{}:MOTR.RBV".format(self.device_name)
        self.rbv_status.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.right_layout.addWidget(self.rbv_status)

        self.statuses_layout = QHBoxLayout()
        self.statuses_layout.addLayout(self.left_layout)
        self.statuses_layout.addLayout(self.right_layout)
        self.statuses_layout.addStretch(1)
        self.frame_layout.addLayout(self.statuses_layout)

    '''Set up a table to show the RMSE of the best polynomial fits for various degrees'''
    def setup_degrees(self):
        self.degrees_frame = QVBoxLayout()
        self.degrees_label = QLabel('LOOCV on polynomials w/ different degrees:')
        self.degrees_frame.addWidget(self.degrees_label)
        self.degrees_table = self.create_table(8, 1, self.degrees_frame)
        vert_header = ['Degree 0', 'Degree 1', 'Degree 2', 'Degree 3', 'Degree 4', 'Degree 5', 'Degree 6', 'Degree 7']
        hori_header = ['RMSE']
        self.degrees_table.setHorizontalHeaderLabels(hori_header)
        self.degrees_table.setVerticalHeaderLabels(vert_header)
        self.sublayout.addLayout(self.degrees_frame)

    '''Set up a table to show the coefficients of the best polynomial'''
    def setup_coefs(self):
        self.coefs_frame = QVBoxLayout()
        self.coefs_label = QLabel('Coefficients for the polynomial of the best degree:')
        self.coefs_frame.addWidget(self.coefs_label)
        self.coefs_table = self.create_table(8, 3, self.coefs_frame)
        hori_headers = ['Previous Coefficients', 'Difference (New - Previous)', 'New Coefficients']
        vert_headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.coefs_table.setHorizontalHeaderLabels(hori_headers)
        self.coefs_table.setVerticalHeaderLabels(vert_headers)
        self.coefs_update_label = self.create_label(self.coefs_frame,'The current coefficients have not been pushed.', True)
        self.push_coefs_button = QPushButton()
        self.push_coefs_button.setText('Push Current Coefficients')
        self.push_coefs_button.setStyleSheet("background-color: #9fc3f5")

        # Set up button that allows user to push current coefficients to EPICS
        self.push_coefs_button.clicked.connect((lambda: self.push_cur_coefs(self.coefs_update_label)))
        self.coefs_frame.addWidget(self.push_coefs_button)
        self.sublayout.addLayout(self.coefs_frame)


    '''Set up the error analysis table that shows for each point, LVDT voltage, estimated posiiton, actual position, and error'''
    def setup_default_err(self):
        self.err_frame = QVBoxLayout()
        self.err_label = QLabel('Error analysis:')
        # self.err_label.setFont(self.bold)
        self.err_frame.addWidget(self.err_label)
        self.err_frame.addWidget(self.err_table)
        err_hori_headers = ['LVDT volt. ({})'.format(self.lvraw_egu), 'Est. position ({})'.format(self.motor_egu), 'Act. position ({})'.format(self.motor_egu), 'Error ({})'.format(self.motor_egu)]
        self.err_table.setHorizontalHeaderLabels(err_hori_headers)
        self.frame_layout.addLayout(self.err_frame)

    '''General function to easily create labels'''    
    def create_label(self, frame, text, box = False):
        self.label = PyDMLabel()
        self.label.setText(text)
        self.label.setGeometry(0, 0, 8, 8)
        frame.addWidget(self.label)
        if (box==True):
            self.label.setFrameShape(QtWidgets.QFrame.Box)
        return self.label    

    '''General function to easily create tables'''    
    def create_table(self, rows, cols, frame):
        self.table = QTableWidget()
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)
        for i in range(rows):
            for j in range(cols):
                self.table.setItem(i, j, QTableWidgetItem("N/A"))
        # self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        frame.addWidget(self.table)
        return self.table

    '''General function to easily format tables'''
    def format_table(self, table):
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  

    '''Push the current coefficients to EPICS and save the old coefficients to a .txt file.
    This function is only called when push_coefs_button is clicked. '''
    def push_cur_coefs(self, label):
        self.old_coef_file = '{}_{}_OLD.txt'.format(self.device_name, self.timestamp)
        self.old_coef_file = os.path.join(self.path, self.old_coef_file)
        label.setText("The current coefficients have been pushed. Saving old coefficients to {}.".format(self.old_coef_file))
        self.old_coefs = self.get_prev_coefs()
        with open(self.old_coef_file, 'w') as f:
            self.lines = []
            for i in range(len(self.old_coefs)):
                letter = chr(65 + i)
                a = str((letter, self.old_coefs[i]))
                self.lines.append(a)
            f.writelines('\n'.join(self.lines))
        f.close()  

    '''Function which retrieves the previous coefficients.
    This is used to display previous coefficients and compare them to the new coefficients'''
    def get_prev_coefs(self):
        self.list_of_coefs = []
        for c in list(map(chr, range(ord('A'), ord('H') + 1))):
            self.tuple = (self.device_name, ':LVPOS_SUB.', c)
            self.sub_pv_name = ''.join(self.tuple)
            self.sub_pv_val = epics.caget(self.sub_pv_name)
            self.list_of_coefs.append(self.sub_pv_val)
        return self.list_of_coefs

    '''Function which displays collected data for the error analysis. Occurs after data analysis button is pressed.
    '''
    def display_error_analysis(self, lvdt, pos, pos_est):
        self.err_table.setRowCount(len(lvdt))
        for i in range(len(lvdt)):
            self.err_table.setItem(i, 0, QTableWidgetItem(str(lvdt[i])))
            self.err_table.setItem(i, 1, QTableWidgetItem(str(pos_est[i])))
            self.err_table.setItem(i, 2, QTableWidgetItem(str(pos[i])))
            self.err_table.setItem(i, 3, QTableWidgetItem(str(pos_est[i] - pos[i])))
        self.err_table.resizeColumnsToContents()
        self.err_table.resizeRowsToContents()
        self.err_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.err_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  

    def progress_fn(self, n):
        self.main_status.setText(n)

    def thread_complete(self):
        print("THREAD COMPLETE!")
        # self.l.setText("Done.")

    '''Function that initalizes a worker thread for the motor movement and data collection. Called after data collection button is pressed. '''
    def data_collection(self):
        # Pass the function to execute
        worker = Worker(self.move_motor_generate_csv) # Any other args, kwargs are passed to the run function
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    ''' Function that is called after the launch of a new thread. Handles motor movement, data collection/output,
    and status update on the screen.
    '''
    def move_motor_generate_csv(self, progress_callback):            
        self.faultack = ''.join((self.device_name, ':FAULTACK.PROC'))
        epics.caput('{}'.format(self.faultack), 1)
        # progress_callback.emit('Moving To High Limit.')
        self.main_status.setText('Moving To High Limit before Data Collection.')
        self.moveToHILimit()
        # progress_callback.emit('At High Limit.')
        self.main_status.setText('At High Limit. Beginning Data Collection.')
        self.prev_hlm = epics.caget(self.motor_hlm) 
        self.prev_llm = epics.caget(self.motor_llm) 
              # New Limits
        epics.caput('{}'.format(self.motor_hlm), 0)
        epics.caput('{}'.format(self.motor_llm), 0)
        time.sleep(5)
        with open(self.csv_file, 'w') as f:
            self.writer = csv.writer(f, delimiter=" ")
            epics.caput('{}'.format(self.faultack), 1)
            self.main_status.setText("Moving To Low Limit.")
            self.lowLimitCheck(self.writer)
            self.main_status.setText("At Low Limit. Wait.")
            time.sleep(5)
            self.main_status.setText("Moving To High Limit.")
            epics.caput('{}'.format(self.faultack), 1)
            self.highLimitCheck(self.writer)
            self.main_status.setText("At High Limit. Done.")
        f.close()
        epics.caput('{}'.format(self.motor_hlm), self.prev_hlm)
        epics.caput('{}'.format(self.motor_llm), self.prev_llm)

    
    '''Function that performs data analysis and updates display. Called after data anlysis button is pressed.'''
    def data_analysis(self):
        # Initalize a .png of best fit line and data points
        self.output_fig = '{}_{}.png'.format(self.device_name,self.timestamp)
        self.output_fig = os.path.join(self.path, self.output_fig)

        # Gather data from .csv file
        self.data = np.genfromtxt(self.csv_file)
        self.ordered = self.data[np.argsort(self.data[:,0])]
        self.lvdt_v, self.position_mm = self.ordered.T

        # Find best degree based on lowest RMSE
        self.baseline = cv(self.lvdt_v, self.position_mm, 0)
        self.curr_deg = self.best_deg = 1
        self.curr_err = self.best_err = self.baseline
        while self.curr_deg < min(8, len(self.lvdt_v)) and self.curr_err <= self.baseline:
            self.curr_err = cv(self.lvdt_v, self.position_mm, self.curr_deg)
            if self.curr_err < self.best_err:
                self.best_deg, self.best_err = self.curr_deg, self.curr_err
            self.degrees_table.setItem(0, self.curr_deg - 1, QTableWidgetItem(str(self.curr_err)))
            self.curr_deg += 1

        self.degrees_table.resizeColumnsToContents()
        self.degrees_table.resizeRowsToContents()
        self.degrees_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.degrees_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.p, self.rmse = fit(self.lvdt_v, self.position_mm, self.lvdt_v, self.position_mm, self.best_deg)
        
        # Generate a .txt file of the new coefficients
        self.coef_file = '{}_{}.txt'.format(self.device_name, self.timestamp)
        self.coef_file = os.path.join(self.path, self.coef_file)
        self.cur_coefs = []
        with open(self.coef_file, 'w') as f:
            self.lines = []
            for i in range(len(self.p)):
                letter = chr(65 + i)
                self.cur_coef = self.p[-i - 1]
                self.coefs_table.setItem(i, 2, QTableWidgetItem(str(self.cur_coef)))
                self.cur_coefs.append(self.cur_coef)
                a = str((letter, self.cur_coef))
                self.lines.append(a)
            f.writelines('\n'.join(self.lines))
        f.close()

        # Display new coefficients
        for i in range (8 - len(self.p)):
            self.cur_coefs.append(0)
        for i in range (len(self.cur_coefs)):
            self.coefs_table.setItem(i, 2, QTableWidgetItem(str(self.cur_coefs[i])))

        # Display old coefficients and the difference between the old and new
        self.old_coefs = self.get_prev_coefs()
        for i in range(len(self.old_coefs)):
            self.coefs_table.setItem(i, 0, QTableWidgetItem(str(self.old_coefs[i])))
            self.coefs_table.setItem(i, 1, QTableWidgetItem(str(self.cur_coefs[i] - self.old_coefs[i])))

        self.coefs_table.resizeColumnsToContents()
        self.coefs_table.resizeRowsToContents()
        self.coefs_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.coefs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Display error analysis
        self.position_mm_est = np.polyval(self.p, self.lvdt_v)
        self.r2 = r2_score(self.position_mm, self.position_mm_est)
        self.err = self.position_mm_est - self.position_mm
        self.display_error_analysis(self.lvdt_v, self.position_mm, self.position_mm_est)

        # Complete generation of .png file
        self.x = np.linspace(-10, 10, 100)
        self.y = np.polyval(self.p, self.x)
        plt.grid()
        plt.plot(self.x, self.y)
        plt.plot(self.lvdt_v, self.position_mm, 'o', markersize=4)
        plt.title('Position vs. LVDT Voltage')
        plt.xlabel('LVDT analog input voltage (V)')
        plt.ylabel('Motor position (mm)')
        plt.text(-4.5, 110, poly_str(self.p), fontsize=8)
        plt.text(-4.5, 105, '$R^2={:.4f}$'.format(self.r2), fontsize=8)
        print('Saving graph to {}...'.format(self.output_fig))
        plt.savefig(self.output_fig, dpi=300)

    '''--- The functions below handle how to make the motor move in tweak steps and gather data at every tweak value.
    Futhermore, the functions handle the statistical math that goes behind finding the best fit polynomial.---'''

    def moveToHILimit(self):
        '''Moves motor to high limit before starting data
        collection '''    
        moveToHighLimit = ''.join((self.device_name,':MOTRHI'))
        motordmov       = ''.join((self.device_name, ':MOTR.DMOV'))

        epics.caput('{}'.format(moveToHighLimit), 1)
        while ((epics.caget(motordmov))==0):
            continue
        if (epics.caget(motordmov) == 1):
            print('Done. At High Limit. Pause.')
            # time.sleep(5)

    def lowLimitCheck(self, writer):
        '''Checks if motor hit low limit       
        '''
        lowlimit_status = ''.join((self.device_name, ':MOTR.LLS'))
        motordmov        = ''.join((self.device_name, ':MOTR.DMOV'))
        motortwr         = ''.join((self.device_name, ':MOTR.TWR'))
        motorpos         = ''.join((self.device_name, ':MOTR.VAL'))

        while ((epics.caget(lowlimit_status)) == 0):
            epics.caput('{}'.format(motortwr), 1)
            print("yes")
            time.sleep(.25)
            if (epics.caget(motordmov) == 0):
                while ((epics.caget(motordmov))==0):
                    # epics.caput('{}'.format(motortwr), 1)
                    continue
                else:
                    print('Done')
                    motorpos_rbv     = ''.join((self.device_name, ':MOTR.RBV'))
                    motor_lvdt       = ''.join((self.device_name, ':LVRAW'))
                    print('MoVAL at ',epics.caget(motorpos))
                    RBV   = epics.caget(motorpos_rbv) 
                    LVRAW = epics.caget(motor_lvdt) 
                    print('DMOV at ',epics.caget(motordmov))
                    rows = [LVRAW,RBV]
                    print(rows)
                    writer.writerow(rows)
                    time.sleep(1)
        print('Device on Low Limit. ')

    def moveReverse(self, writer):
        '''Move motor reverse by TWK amount       
        '''
        motortwr         = ''.join((self.device_name, ':MOTR.TWR'))
        motordmov        = ''.join((self.device_name, ':MOTR.DMOV'))
        motorpos         = ''.join((self.device_name, ':MOTR.VAL'))
        motoract         = ''.join((self.device_name, ':MOTR.RBV'))

        rows = []
        if (epics.caget(motordmov) == 0 or epics.caget(motoract) == 0):
            epics.caput('{}'.format(motortwr), 1)
            '''
            if ((epics.caget(motorpos) - epics.caget(motoract)) < (-1 * self.motor_twv)):
                print("changing value")
                val = epics.caget(motorpos) + epics.caget(self.motor_twv)
                epics.caput('{}'.format(motorpos), val)
            '''

            while ((epics.caget(motordmov))==0):
                # epics.caput('{}'.format(motortwr), 1)
                continue
            else:
                print('Done')
                motorpos_rbv     = ''.join((self.device_name, ':MOTR.RBV'))
                motor_lvdt       = ''.join((self.device_name, ':LVRAW'))
                print('MoVAL at ',epics.caget(motorpos))
                RBV   = epics.caget(motorpos_rbv) 
                LVRAW = epics.caget(motor_lvdt) 
                print('DMOV at ',epics.caget(motordmov))
                rows = [LVRAW,RBV]
                print(rows)
                writer.writerow(rows)
                # time.sleep(1)

    def highLimitCheck(self, writer):
        '''Checks if motor hit high limit       
        '''
        highlimit_status = ''.join((self.device_name, ':MOTR.HLS'))
        motordmov        = ''.join((self.device_name, ':MOTR.DMOV'))
        motortwf         = ''.join((self.device_name, ':MOTR.TWF'))
        motorpos         = ''.join((self.device_name, ':MOTR.VAL'))

        while ((epics.caget(highlimit_status)) == 0):
            epics.caput('{}'.format(motortwf), 1)
            print("yes")
            time.sleep(.25)
            if (epics.caget(motordmov) == 0):
                while ((epics.caget(motordmov))==0):
                    # epics.caput('{}'.format(motortwr), 1)
                    continue
                else:
                    print('Done')
                    motorpos_rbv     = ''.join((self.device_name, ':MOTR.RBV'))
                    motor_lvdt       = ''.join((self.device_name, ':LVRAW'))
                    print('MoVAL at ',epics.caget(motorpos))
                    RBV   = epics.caget(motorpos_rbv) 
                    LVRAW = epics.caget(motor_lvdt) 
                    print('DMOV at ',epics.caget(motordmov))
                    rows = [LVRAW,RBV]
                    print(rows)
                    writer.writerow(rows)
                    # time.sleep(1)

            # self.moveReverse(writer)
            # print("moveReverse starting")
            # time.sleep(3)
        print('Device on High Limit. ')

    def moveForward(self, writer):
        '''Move motor forward by TWK amount       
        '''
        motortwf         = ''.join((self.device_name, ':MOTR.TWF'))
        motordmov        = ''.join((self.device_name, ':MOTR.DMOV'))
        motorpos         = ''.join((self.device_name, ':MOTR.VAL'))

        epics.caput('{}'.format(motortwf), 1)
        rows = []

        if (epics.caget(motordmov) == 0):
            while ((epics.caget(motordmov))==0):
                continue
            else:
                print('Done')
                motorpos_rbv     = ''.join((self.device_name, ':MOTR.RBV'))
                motor_lvdt       = ''.join((self.device_name, ':LVRAW'))
                print('MoVAL at ',epics.caget(motorpos))
                RBV   = epics.caget(motorpos_rbv) 
                LVRAW = epics.caget(motor_lvdt) 
                print('DMOV at ',epics.caget(motordmov))
                rows=[LVRAW,RBV]
                print(rows)
                writer.writerow(rows)
                time.sleep(1)
            
def cv(x, y, deg):
        loo = LeaveOneOut()
        rmse_arr = np.array([])
        for train_index, test_index in loo.split(x):
            x_train, x_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]
            p, rmse = fit(x_train, y_train, x_test, y_test, deg)
            rmse_arr = np.append(rmse_arr, rmse)
        return np.mean(rmse_arr**2)

def fit(x_train, y_train, x_test, y_test, deg):
        p = np.polyfit(x_train, y_train, deg)
        y_est = np.polyval(p, x_test)
        rmse = sqrt(mean_squared_error(y_test, y_est))
        return p, rmse

def poly_str(p):
    '''Returns a matplotlib string representing a polynomial with coefficients p'''
    string = '$y={:.4f}{}'.format(p[0], pow_str(len(p) - 1))
    for i in range(1, len(p)):
        string += '{:+.4f}{}'.format(p[i], pow_str(len(p) - 1 - i))

    return string + '$'

def pow_str(n):
    '''Returns a string representing x^n'''
    if n == 0:
        return ''

    if n == 1:
        return 'x'

    return 'x^{}'.format(n)

device = sys.argv[1]
if (len(sys.argv)  == 3):
    file = sys.argv[2]
    macros = {"MAD": device, "FILENAME": file}
else:
    macros = {"MAD": device}
# print(macros.get("MAD"))
app = QApplication([])
# window = MainWindow()
window = MainWindow(macros = macros)
app.exec_()