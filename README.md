# Picoscope_remote_access
A script for triggering a Picoscope 5442A, Series 5000 remotely is provided using the picosdk-python-wrappers.

## Setup of the PC that is going to be used
- in order to use the picosdk-python-wrappers a python version (not the latest in that case python 3.13 is not compatible!)
- the scripts are run on python 3.9.9
- we need as well the library picosdk-python-wrappers: https://github.com/picotech/picosdk-python-wrappers. Follow the installation guide please.
  
## Running the script
- run picoscope_script.py, by default the data is going to be store locally in the current directory. The directory (path_to_save_locally) can be changed to save the parquet files. There is a second path that can be adjusted to copy the stored data to a different location (my_eos_folder).
- the data is stored in parquet, the name contains the time of the measurement
- the parquets have 9 columns, the data for 4 channels in mV, the time in ns, the units and the timestamps
