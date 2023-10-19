BATTERY_DISCHARGE_DEGRADATION = {
    "title": "Discharge Degradation",
    "xlabel": "Cycle",
    "ylabel": "Ratio to initial value",
    "legend": ["Capacity", "Rectified_Impedance", "Re", "Rct"],
}

CYCLE_DISCHARGE_CURVE = {
    "title": "Discharge Curve",
    "y": "Voltage_measured",
    "xlabel": "Time (s)",
    "ylabel": "Voltage (V)",
    "legend": ["Voltage"],
}

CYCLE_CHARGE_CURVE = {
    "title": "Charge Curve",
    "y": "Current_measured",
    "xlabel": "Time (s)",
    "ylabel": "Current (A)",
    "legend": ["Current"],
}

BATTERY_IMPEDANCE_CURVE = {
    "title": "Impedance Curve",
    "x": "Cycle_number",
    "y": ["Rectified_Impedance", "Re", "Rct"],
    "xlabel": "Cycle",
    "ylabel": "Impedance (Ohm)",
    "legend": ["Rectified_Impedance", "Re", "Rct"],
}

BATTERY_IMPEDANCE_CURVE_WITH_CAPACITY = {
    "title": "Impedance Curve",
    "y": ["Rectified_Impedance", "Capacity"],
    "xlabel": "Cycle",
    "legend": ["Rectified_Impedance", "Capacity"],
}
