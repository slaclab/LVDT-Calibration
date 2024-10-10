from argparse import ArgumentParser
from epics import caput, caget
from time import sleep
from pandas import read_csv
from numpy import polyfit, polyval, linspace, min, max
import matplotlib.pyplot as plt
import os


"""
1. Move both jaws to their outer limit
    - For NEGY this should be -52mm
    - For POSY this should be +52mm

2. Run Script with python ../mc_calibrate_lvdt.py
    - Required: --device
        - Desc:    Full collimator device name
        - Type:    String
        - Range:   Any collimator

    - Optional: --step
        - Desc:    Step size in EGU of motor
        - Type:    Float
        - Range:   0.0...INF
        - Default: Current tweak setting

    - Optional: --sub
        - Desc:    Old naming convention of LVPOS_SUB
        - Type:    Bool
        - Range:   True...False
        - Default: True

    - Optional: --measurements
        - Desc:    Amount of points to collect at position
        - Type:    Int
        - Range:   1...INF
        - Default: 4

3. Example command line
    - python mc_calibrate_lvdt.py --device COLL:BPN26:424:POSY --step 5 --sub True --measurements 2
"""
def mc_calibrate_lvdt(device: str, step: float, sub: bool, measurements: int) -> None:

    # Device Naming Convention
    coeff_prefix = "LVPOS_SUB" if sub else "LVPOS"
    convention = ["HLS", "TWF", "LLS", "TWR"]
    if "NEG" not in device: convention = convention[2:] + convention[:2]
    
    # Get Previous Params
    curr_twv = float(caget(f'{device}:MOTR.TWV'))
    curr_coeff = [float(caget(f"{device}:{coeff_prefix}.{chr(ord('A') + i)}")) for i in range(7)]

    # Set Tweek Value
    if step is not None: caput(f'{device}:MOTR.TWV', step)

    # Sweep
    with open(f'{device.replace(":","_")}.csv','w') as file:
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
    data = read_csv(f'{device.replace(":","_")}.csv', header=None).to_numpy()

    # Fit
    new_coeff = polyfit(data[:,0], data[:,1], 7)
    x_fit = linspace(min(data[:,0]), max(data[:,0]), 1000)
    y_fit = polyval(new_coeff, x_fit)
    plt.plot(x_fit, y_fit, label='Fitted Polynomial', color='blue')
    plt.scatter(data[:,0], data[:,1], label='Original Data', color='red')
    plt.xlabel('Jaw Position (mm)')
    plt.ylabel('LVDT Feedback (V)')
    plt.legend()
    plt.grid()
    plt.title(f'{device}')
    plt.tight_layout()
    plt.savefig(f'{device.replace(":","_")}.png')
    plt.close()

    # Print Results and Display
    os.system(f'eog {os.path.abspath(os.path.dirname(__file__))}/{device.replace(":","_")}.png')
    print('Old Coefficients     New Coeficients')
    for i in range(7):
        print(f'{curr_coeff[i]:+.3E}             {new_coeff[i]:+.3E}')

        # Preserve Coeff A for Beamline
        if i is not 0: caput(f"{device}:{coeff_prefix}.{chr(ord('A') + i)}", new_coeff[i])
    

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--device', type=str, required=True)
    parser.add_argument('--step', type=float, required=False, default=None)
    parser.add_argument('--sub', type=bool, required=False, default=True)
    parser.add_argument('--measurements', type=int, required=False, default=4)

    args = parser.parse_args()
    mc_calibrate_lvdt(args.device, args.step, args.sub, args.measurements)