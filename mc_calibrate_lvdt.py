from argparse import ArgumentParser
from epics import caput, caget
from time import sleep
from pandas import read_csv
from numpy import polyfit, polyval, linspace, min, max
from datetime import datetime
import matplotlib.pyplot as plt
import os


"""
1. Move both jaws to their outer limit
    - For NEGY this should be -52mm
    - For POSY this should be +52mm
2. Example command line
    - python mc_calibrate_lvdt.py --device COLL:BPN26:424:POSY --step 5 --sub True --measurements 4
"""
def mc_calibrate_lvdt(device: str, step: float, sub: bool, measurements: int) -> None:

    # Path Reconciliation
    now = datetime.now()
    now_fmt = now.strftime('%b-%d-%Y-%I-%M%p')
    cal_path = os.environ.get('PHYSICS_DATA') + '/genMotion/lvdt/' + device.replace(':','_')
    if not os.path.isdir(cal_path): os.mkdir(cal_path)
    data_file_name =  f'{cal_path}/DATA_{now_fmt}.csv'
    plot_file_name = f'{cal_path}/PLOT_{now_fmt}.png'
    coef_file_name = f'{cal_path}/Coefficients.txt'

    # Device Naming Convention
    coeff_prefix = 'LVPOS_SUB' if sub else 'LVPOS'
    convention = ['HLS', 'TWF', 'LLS', 'TWR']
    if "NEG" not in device: convention = convention[2:] + convention[:2]
    
    # Get Previous Params
    curr_twv = float(caget(f'{device}:MOTR.TWV'))
    curr_coeff = [float(caget(f"{device}:{coeff_prefix}.{chr(ord('A') + i)}")) for i in range(7)]

    # Set Tweek Value
    if step is not None: caput(f'{device}:MOTR.TWV', step)

    # Sweep
    with open(data_file_name,'w') as file:
        for j in range(2):
            while not bool(caget(f'{device}:MOTR.{convention[0 + 2*j]}')):
                for i in range(measurements):
                    sleep(1)
                    motor_pos = float(caget(f'{device}:MOTR.RBV'))
                    lvdt_pos = float(caget(f'{device}:LVRAW'))
                    file.write(f'{motor_pos},{lvdt_pos}\n')
                caput(f'{device}:MOTR.{convention[1 + 2*j]}', 1, wait=True, timeout=10)

    # Reset Tweek Value
    caput(f'{device}:MOTR.TWV', curr_twv)

    # Read Data
    data = read_csv(data_file_name, header=None).to_numpy()

    # Fit
    new_coeff = polyfit(data[:,0], data[:,1], 7)
    x_fit = linspace(min(data[:,0]), max(data[:,0]), 1000)
    y_fit = polyval(new_coeff, x_fit)
    plt.plot(x_fit, y_fit, label='Fitted Polynomial', color='blue')
    plt.scatter(data[:,0], data[:,1], label='Original Data', color='red')
    plt.xlabel('Jaw Position (mm)'); plt.ylabel('LVDT Feedback (V)')
    plt.legend(); plt.grid(); plt.title(f'{device}'); plt.tight_layout()
    plt.savefig(plot_file_name)
    plt.close()

    # Print Results and Display
    os.system(f'eog {plot_file_name}')
    user_input = input("Apply Coefficients? (y/n):").strip().upper()
    with open(coef_file_name,'a') as file:
        file.write(f'{now_fmt}  ')
        for i in range(7):
            file.write(f'{new_coeff[i]:+.6E}  ')
            if i is not 0 and user_input in ['y','Y']:
                    caput(f"{device}:{coeff_prefix}.{chr(ord('A') + i)}", new_coeff[i])
        file.write('\n')
    

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--device', type=str, required=True, help='full PV name of collimator')
    parser.add_argument('--step', type=float, required=False, default=None, help='step size in egu')
    parser.add_argument('--sub', type=bool, required=False, default=True, help='naming convention if LVPOS_SUB')
    parser.add_argument('--measurements', type=int, required=False, default=4, help='measurements at each position')

    args = parser.parse_args()
    mc_calibrate_lvdt(args.device, args.step, args.sub, args.measurements)