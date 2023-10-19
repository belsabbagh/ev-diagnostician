# Estimating RUL of Li-ion Batteries using Deep Learning

## Methodology

A set of four Li-ion batteries (# 5, 6, 7 and 18) were run through 3 different operational profiles (charge, discharge and impedance) at room temperature.
Charging was carried out in a constant current (CC) mode at 1.5A until the battery voltage reached 4.2V and then continued in a constant voltage (CV) mode until the charge current dropped to 20mA.
Discharge was carried out at a constant current (CC) level of 2A until the battery voltage fell to 2.7V, 2.5V, 2.2V and 2.5V for batteries 5 6 7 and 18 respectively.
Impedance measurement was carried out through an electrochemical impedance spectroscopy (EIS) frequency sweep from 0.1Hz to 5kHz. Repeated charge and discharge cycles result in accelerated aging of the batteries while impedance measurements provide insight into the internal battery parameters that change as aging progresses.
The experiments were stopped when the batteries reached end-of-life (EOL) criteria, which was a 30% fade in rated capacity (from 2Ahr to 1.4Ahr).
This dataset can be used for the prediction of both remaining charge (for a given discharge cycle) and remaining useful life (RUL).

### Dataset Description

The dataset was collected by NASA from Li-ion batteries that were run through charge, discharge, and impedance cycles. The charge cycles simulate the battery being charged in a typical application with constant current until the battery reaches a certain voltage. The charging mode changes to constant voltage mode until the charge current drops to a certain current.
The discharge cycles simulate the battery being discharged in a typical application with constant current until the voltage falls to a certain value.
The impedance measurement was chosen as the damage criterion for the batteries and was measured using an electrochemical impedance spectroscopy (EIS) frequency sweep from 0.1Hz to 5kHz.
Each battery ran through an amount of cycles until it reached its end of life (EOL) criteria, which was a 30% fade in rated capacity (from 2Ahr to 1.4Ahr).
