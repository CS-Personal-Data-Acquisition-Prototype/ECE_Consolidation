# Sensor Data Acquisition Script

This script, `dbScript_schema.py`, is designed to read sensor data from multiple sources, process it, and store it in a SQLite database. It is intended for use in data acquisition systems that involve GPS, accelerometers, gyroscopes, and DAC sensors.

## Features

- **Database Creation**: Automatically creates a SQLite database (`data_acquisition.db`) with a `sensor_data` table to store sensor readings.
- **Sensor Data Simulation**: Generates random GPS, accelerometer, gyroscope, and DAC data for testing purposes.
- **Serial Communication**: Reads data from multiple serial devices, including:
  - Force sensor (`/dev/ttyACM0`)
  - Potentiometers (`/dev/ttyACM2`)
  - 9DOF sensor (`/dev/ttyUSB0`)
- **Data Logging**: Logs sensor data with timestamps and session IDs into the database.

## Table Schema

The `sensor_data` table has the following columns:

- `id`: Auto-incrementing primary key
- `sessionID`: Unique identifier for each session
- `timestamp`: Timestamp of the reading
- `latitude`, `longitude`, `altitude`: GPS coordinates
- `accel_x`, `accel_y`, `accel_z`: Accelerometer readings
- `gyro_x`, `gyro_y`, `gyro_z`: Gyroscope readings
- `dac_1`, `dac_2`, `dac_3`, `dac_4`: DAC sensor readings

## Usage

1. Ensure the required serial devices are connected to the specified ports.
2. Run the script:
```bash
python dbScript_schema.py
```
The script will create the database (if it doesn't already exist) and start reading sensor data.

## Dependencies
- Python 3.x
- Required libraries:
    - serial
    - sqlite3
    - uuid
    - datetime
    - random
Install dependencies using pip if not already installed:

```bash
pip install pyserial
```

## Notes
 - The script includes commented-out sections for additional functionality, such as converting GPS coordinates to decimal format and reading data from a GPS sensor.
 - Modify the serial port paths (/dev/ttyACM0, etc.) as needed for your system.

## Keyboard Interrupt
To stop the script, press Ctrl+C. The script will terminate gracefully.

## Disclaimer
This script is provided as-is and may require modifications to suit specific hardware configurations or data acquisition requirements. 