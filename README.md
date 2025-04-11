# Picoscope_remote_access
A script for triggering a Picoscope 5442A, Series 5000 remotely is provided using the picosdk-python-wrappers.

## Setup of the PC that is going to be used
- In order to use the picosdk-python-wrappers, a Python version is needed (not the latest, in that case Python 3.13 is not compatible!).
- The scripts are run on Python 3.9.9.
- You will also need the library picosdk-python-wrappers: https://github.com/picotech/picosdk-python-wrappers. Please follow the installation guide.

## Running the script
- Run `picoscope_script.py`. By default, the data will be stored locally in the current directory. The directory (`path_to_save_locally`) can be changed to save the Parquet files elsewhere. There is a second path that can be adjusted to copy the stored data to a different location (`my_eos_folder`).
- The data is saved in Parquet format. The filenames contain the time of the measurement.
- The Parquet files have 9 columns: the data for 4 channels in mV, the time in ns, the units, and the timestamps.
