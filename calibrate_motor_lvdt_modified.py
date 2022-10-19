# This file has all the functions from calibrate_motor_lvdt.py

from __future__ import print_function
import epics
import time
import datetime
import os
import csv
import sys
import getopt
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QApplication
from pydm.widgets import PyDMLabel
import numpy as np
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
#from colorama import Fore, Back, Style
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

devices = { 
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

def fit(x_train, y_train, x_test, y_test, deg):
    '''Fits a polynomial of a specified degree to the training data
       and computes the RMSE of the polynomial on the test data
    '''
    p = np.polyfit(x_train, y_train, deg)
    y_est = np.polyval(p, x_test)
    rmse = sqrt(mean_squared_error(y_test, y_est))
    return p, rmse

def cv(x, y, deg):
    '''Determines the overall RMSE from leave-one-out cross-validation'''
    loo = LeaveOneOut()
    rmse_arr = np.array([])
    for train_index, test_index in loo.split(x):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]
        p, rmse = fit(x_train, y_train, x_test, y_test, deg)
        rmse_arr = np.append(rmse_arr, rmse)
    return np.mean(rmse_arr**2)

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

def moveToHILimit(prefix):
    '''Moves motor to high limit before starting data
       collection 
    '''
    # Originally, prefix was 'value'???
    print("IN moveToHILimit")
    moveToHighLimit = ''.join((prefix,':MOTRHI'))

    highLimitStatus = ''.join((prefix, ':MOTR.HLS'))
    motordmov       = ''.join((prefix, ':MOTR.DMOV'))

    epics.caput('{}'.format(moveToHighLimit), 1)
    while ((epics.caget(motordmov))==0):
        continue
        print('Waiting ')
        print('DMOV at ',epics.caget(motordmov))
        QApplication.processEvents()

    if (epics.caget(motordmov) == 1):
        print('Done. At High Limit. Pause.')
        time.sleep(5)

def highLimitCheck(prefix):
    '''Checks if motor hit high limit       
    '''
    print("In highLimitCheck")
    highlimit_status = ''.join((prefix, ':MOTR.HLS'))

    while ((epics.caget(highlimit_status)) == 0):
        moveForward(prefix)
        QApplication.processEvents()
    print('Device on High Limit ')

def lowLimitCheck(prefix):
    print("IN lowLimitCheck")
    '''Checks if motor hit low limit       
    '''
    lowlimit_status = ''.join((prefix, ':MOTR.LLS'))

    while ((epics.caget(lowlimit_status)) == 0):
        moveReverse(prefix)
        QApplication.processEvents()

    print('Device on Low Limit. ')

def moveReverse(prefix):
    '''Move motor reverse by TWK amount       
    '''
    print("IN moveReverse")
    motortwr         = ''.join((prefix, ':MOTR.TWR'))
    motordmov        = ''.join((prefix, ':MOTR.DMOV'))

    epics.caput('{}'.format(motortwr), 1)
    while ((epics.caget(motordmov))==0):
        continue
        print('Waiting ')
        print('DMOV at ',epics.caget(motordmov))
    if (epics.caget(motordmov) == 1):
        print('Done')
        motorpos         = ''.join((prefix, ':MOTR.VAL'))
        motorpos_rbv     = ''.join((prefix, ':MOTR.RBV'))
        motor_lvdt       = ''.join((prefix, ':LVRAW'))
        print('MoVAL at ',epics.caget(motorpos))
        RBV   = epics.caget(motorpos_rbv) 
        LVRAW = epics.caget(motor_lvdt) 
        print('DMOV at ',epics.caget(motordmov))
        time.sleep(5)
    # rows=[LVRAW,RBV]
    # writer.writerow(rows)

def moveForward(prefix):
    '''Move motor forward by TWK amount       
    '''
    print("IN moveForward")
    motortwf         = ''.join((prefix, ':MOTR.TWF'))
    motordmov        = ''.join((prefix, ':MOTR.DMOV'))
    epics.caput('{}'.format(motortwf), 1)
    while ((epics.caget(motordmov))==0):
        continue
        print('Waiting ')
        print('DMOV at ',epics.caget(motordmov))
    if (epics.caget(motordmov) == 1):
        print('Done')
        motorpos         = ''.join((prefix, ':MOTR.VAL'))
        motorpos_rbv     = ''.join((prefix, ':MOTR.RBV'))
        motor_lvdt       = ''.join((prefix, ':LVRAW'))
        print('MoVAL at ',epics.caget(motorpos))
        RBV   = epics.caget(motorpos_rbv) 
        LVRAW = epics.caget(motor_lvdt) 
        print('DMOV at ',epics.caget(motordmov))
        time.sleep(5)
    # rows=[LVRAW,RBV]
    # writer.writerow(rows)

def usage(prog_name):
    print("\n%s: Provides a best fit polynomial co-efficient" % prog_name)
    print("Collect position v/s LVDT data for a motor")
    print("Usage:")
    print("   %s -h  Shows this usage message" % prog_name)
    print("   %s -m  The MAD name of device. eg: CXBP34" % prog_name)
    print("   %s -i  Input file name. Provide data set in format eg: [MOTR LVRAW]" % prog_name)
    print(" ")
'''
def getPrevCoefs():
    # Originally devices.get(mad_name)
    device = devices.get('CEDOG-POSY')
    row = 0
    list_of_coefs = []
    for c in list(map(chr, range(ord('A'), ord('H') + 1))):
        tuple = (device, ':LVPOS_SUB.', c)
        sub_pv_name = ''.join(tuple)
        sub_pv_val = epics.caget(sub_pv_name)
        list_of_coefs.append(sub_pv_val)
    return list_of_coefs
'''

