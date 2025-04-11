# %%
import ctypes
import numpy as np
from picosdk.ps5000a import ps5000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok, mV2adc
import time as time_lib
from datetime import datetime
import os
import pandas as pd
import shutil


# Assuming your data collection and plotting part is inside a function or a block
def collect_data(path_to_save_locally = '.', plots_signal = False):
    # -------------------- SAFETY CHECK BEFORE STARTING --------------------
    print("🔒 Running safety check before opening PicoScope...")

    # Set a flag to indicate whether to proceed
    SAFE_TO_START = True

    # 1. Try to close any previously opened device
    try:
        status = {}
        if 'chandle' in globals():
            print("🔄 Closing previously opened PicoScope handle...")
            status["closeUnit"] = ps.ps5000aCloseUnit(chandle)
            assert_pico_ok(status["closeUnit"])
            del chandle
    except Exception as e:
        print(f"⚠️ Warning: Could not close previous unit. Proceeding anyway.\nDetails: {e}")

    # 2. Additional user-defined safety checks (optional)
    # Example: Check file handles, log files, cleanup temp folders, etc.
    # ...

    # 3. Confirm with the user or log
    if SAFE_TO_START:
        print("✅ Safety check passed. Proceeding with PicoScope setup.")
    else:
        print("❌ Safety check failed. Exiting script.")
        exit()

    # -------------------- BEGIN PICO INITIALIZATION --------------------
    # Create chandle and status ready for use
    chandle = ctypes.c_int16()
    status = {}

    # Open 5000 series PicoScope
    # Resolution set to 12 Bit
    resolution =ps.PS5000A_DEVICE_RESOLUTION["PS5000A_DR_12BIT"]
    # Returns handle to chandle for use in future API functions
    status["openunit"] = ps.ps5000aOpenUnit(ctypes.byref(chandle), None, resolution)

    try:
        assert_pico_ok(status["openunit"])
    except: # PicoNotOkError:

        powerStatus = status["openunit"]

        if powerStatus == 286:
            status["changePowerSource"] = ps.ps5000aChangePowerSource(chandle, powerStatus)
        elif powerStatus == 282:
            status["changePowerSource"] = ps.ps5000aChangePowerSource(chandle, powerStatus)
        else:
            raise

        assert_pico_ok(status["changePowerSource"])
    # Set up channel A
    # handle = chandle
    channel = ps.PS5000A_CHANNEL["PS5000A_CHANNEL_A"]
    # enabled = 1
    coupling_type = ps.PS5000A_COUPLING["PS5000A_DC"]
    chARange = ps.PS5000A_RANGE["PS5000A_20V"]
    # analogue offset = 0 V
    status["setChA"] = ps.ps5000aSetChannel(chandle, channel, 1, coupling_type, chARange, 0)
    assert_pico_ok(status["setChA"])
    #print('assert_pico_ok(status["setChA"])', assert_pico_ok(status["setChA"]))

    # Set up channel B
    # handle = chandle
    channel = ps.PS5000A_CHANNEL["PS5000A_CHANNEL_B"]
    # enabled = 1
    # coupling_type = ps.PS5000A_COUPLING["PS5000A_DC"]
    chBRange = ps.PS5000A_RANGE["PS5000A_2V"]
    # analogue offset = 0 V
    status["setChB"] = ps.ps5000aSetChannel(chandle, channel, 1, coupling_type, chBRange, 0)
    assert_pico_ok(status["setChB"])
    #print('assert_pico_ok(status["setChB"])', assert_pico_ok(status["setChB"]))

    # Set up channel C
    # handle = chandle
    channel = ps.PS5000A_CHANNEL["PS5000A_CHANNEL_C"]
    # enabled = 1
    # coupling_type = ps.PS5000A_COUPLING["PS5000A_DC"]
    chBRange = ps.PS5000A_RANGE["PS5000A_2V"]
    # analogue offset = 0 V
    status["setChC"] = ps.ps5000aSetChannel(chandle, channel, 1, coupling_type, chBRange, 0)
    assert_pico_ok(status["setChC"])
    #print('assert_pico_ok(status["setChC"])', assert_pico_ok(status["setChC"]))

    # Set up channel D
    # handle = chandle
    channel = ps.PS5000A_CHANNEL["PS5000A_CHANNEL_D"]
    # enabled = 1
    # coupling_type = ps.PS5000A_COUPLING["PS5000A_DC"]
    chDRange = ps.PS5000A_RANGE["PS5000A_2V"]
    # analogue offset = 0 V
    status["setChD"] = ps.ps5000aSetChannel(chandle, channel, 1, coupling_type, chDRange, 0)
    assert_pico_ok(status["setChD"])
    #print('assert_pico_ok(status["setChD"])', assert_pico_ok(status["setChD"]))


    # find maximum ADC count value
    # handle = chandle
    # pointer to value = ctypes.byref(maxADC)
    maxADC = ctypes.c_int16()
    status["maximumValue"] = ps.ps5000aMaximumValue(chandle, ctypes.byref(maxADC))
    assert_pico_ok(status["maximumValue"])
    #print('assert_pico_ok(status["maximumValue"]), assert_pico_ok(status["maximumValue"])')

    # Set up an advanced trigger
    adcTriggerLevelA = 1 #mV2adc(500, chARange, maxADC)
    adcTriggerLevelB = 1 #mV2adc(500, chARange, maxADC)
    adcTriggerLevelC = 1 #mV2adc(500, chARange, maxADC)
    adcTriggerLevelD = 1 #mV2adc(500, chARange, maxADC)


    triggerProperties = (ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2 * 4)()
    triggerProperties[0] = ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2(adcTriggerLevelA,
                                                                10,
                                                                0,
                                                                10,
                                                                ps.PS5000A_CHANNEL["PS5000A_CHANNEL_A"])
                                                                
    triggerProperties[1] = ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2(adcTriggerLevelB,
                                                                10,
                                                                0,
                                                                10,
                                                                ps.PS5000A_CHANNEL["PS5000A_CHANNEL_B"])
                                                                
    triggerProperties[2] = ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2(adcTriggerLevelC,
                                                                10,
                                                                0,
                                                                10,
                                                                ps.PS5000A_CHANNEL["PS5000A_CHANNEL_C"])
                                                                
    triggerProperties[3] = ps.PS5000A_TRIGGER_CHANNEL_PROPERTIES_V2(adcTriggerLevelD,
                                                                10,
                                                                0,
                                                                10,
                                                                ps.PS5000A_CHANNEL["PS5000A_CHANNEL_D"])
                                                            
                                                                
    status["setTriggerChannelPropertiesV2"] = ps.ps5000aSetTriggerChannelPropertiesV2(chandle, ctypes.byref(triggerProperties), 4, 0)
    assert_pico_ok(status["setTriggerChannelPropertiesV2"])
    #print('assert_pico_ok(status["setTriggerChannelPropertiesV2"])', assert_pico_ok(status["setTriggerChannelPropertiesV2"]))

    triggerConditionsA = ps.PS5000A_CONDITION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_A"],
                                                            ps.PS5000A_TRIGGER_STATE["PS5000A_CONDITION_TRUE"])
    triggerConditionsB = ps.PS5000A_CONDITION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_B"],
                                                            ps.PS5000A_TRIGGER_STATE["PS5000A_CONDITION_TRUE"])
    triggerConditionsC = ps.PS5000A_CONDITION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_C"],
                                                            ps.PS5000A_TRIGGER_STATE["PS5000A_CONDITION_TRUE"])
    triggerConditionsD = ps.PS5000A_CONDITION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_D"],
                                                            ps.PS5000A_TRIGGER_STATE["PS5000A_CONDITION_TRUE"])
    clear = 1
    add = 2
                                                            
    status["setTriggerChannelConditionsV2_A"] = ps.ps5000aSetTriggerChannelConditionsV2(chandle, ctypes.byref(triggerConditionsA), 1, (clear + add))
    assert_pico_ok(status["setTriggerChannelConditionsV2_A"])
    #print('assert_pico_ok(status["setTriggerChannelConditionsV2_A"])', assert_pico_ok(status["setTriggerChannelConditionsV2_A"]))
    status["setTriggerChannelConditionsV2_B"] = ps.ps5000aSetTriggerChannelConditionsV2(chandle, ctypes.byref(triggerConditionsB), 1, (add))
    assert_pico_ok(status["setTriggerChannelConditionsV2_B"])
    #print('assert_pico_ok(status["setTriggerChannelConditionsV2_B"])', assert_pico_ok(status["setTriggerChannelConditionsV2_B"]))
    status["setTriggerChannelConditionsV2_C"] = ps.ps5000aSetTriggerChannelConditionsV2(chandle, ctypes.byref(triggerConditionsC), 1, (add))
    assert_pico_ok(status["setTriggerChannelConditionsV2_C"])
    #print('assert_pico_ok(status["setTriggerChannelConditionsV2_C"])', assert_pico_ok(status["setTriggerChannelConditionsV2_C"]))
    status["setTriggerChannelConditionsV2_D"] = ps.ps5000aSetTriggerChannelConditionsV2(chandle, ctypes.byref(triggerConditionsD), 1, (add))
    assert_pico_ok(status["setTriggerChannelConditionsV2_D"])
    #print('assert_pico_ok(status["setTriggerChannelConditionsV2_D"])', assert_pico_ok(status["setTriggerChannelConditionsV2_D"]))

    triggerDirections = (ps.PS5000A_DIRECTION * 4)()
    triggerDirections[0] = ps.PS5000A_DIRECTION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_A"], 
                                                                ps.PS5000A_THRESHOLD_DIRECTION["PS5000A_RISING_OR_FALLING"], 
                                                                ps.PS5000A_THRESHOLD_MODE["PS5000A_LEVEL"])
    triggerDirections[1] = ps.PS5000A_DIRECTION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_B"], 
                                                                ps.PS5000A_THRESHOLD_DIRECTION["PS5000A_RISING_OR_FALLING"], 
                                                                ps.PS5000A_THRESHOLD_MODE["PS5000A_LEVEL"])
    triggerDirections[2] = ps.PS5000A_DIRECTION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_C"], 
                                                                ps.PS5000A_THRESHOLD_DIRECTION["PS5000A_RISING_OR_FALLING"], 
                                                                ps.PS5000A_THRESHOLD_MODE["PS5000A_LEVEL"])
    triggerDirections[3] = ps.PS5000A_DIRECTION(ps.PS5000A_CHANNEL["PS5000A_CHANNEL_D"], 
                                                                ps.PS5000A_THRESHOLD_DIRECTION["PS5000A_RISING_OR_FALLING"], 
                                                                ps.PS5000A_THRESHOLD_MODE["PS5000A_LEVEL"])
    status["setTriggerChannelDirections"] = ps.ps5000aSetTriggerChannelDirectionsV2(chandle, ctypes.byref(triggerDirections), 4)
    assert_pico_ok(status["setTriggerChannelDirections"])


    # Get timebase information
    # Warning: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
    # To access these Timebases, set any unused analogue channels to off.
    # handle = chandle
    ############
    
    # Desired sample rate (1 MS/s)
    desired_sample_rate = 500000  # 1 MS/s
    duration = 3
    maxSamples = duration * desired_sample_rate
    preTriggerSamples = 10000  # Example value
    #maxSamples = preTriggerSamples + postTriggerSamples
    
    # Set the max number of samples to capture
    #maxSamples = 2000000

    # Step 1: Find the timebase corresponding to 1 MS/s
    timebase = 8 * 16   # Example; verify or adjust to get the (128) 0.5 MS/s rate
    timeIntervalns = ctypes.c_float()  # Time interval between samples (ns)
    returnedMaxSamples = ctypes.c_int32()

    # Get the timebase info for the selected timebase
    status["getTimebase2"] = ps.ps5000aGetTimebase2(chandle, timebase, maxSamples, ctypes.byref(timeIntervalns), ctypes.byref(returnedMaxSamples), 0)
    assert_pico_ok(status["getTimebase2"])

    # Calculate the actual sample rate
    sample_rate = 1 / (timeIntervalns.value * 1e-9)  # Convert time interval to seconds and calculate rate
    #print(f"Timebase {timebase} gives a sample rate of {sample_rate} samples per second.")

    # Step 2: Adjust preTriggerSamples and postTriggerSamples as needed
    postTriggerSamples = maxSamples - preTriggerSamples


    # Step 4: Collect the data (assuming block mode)
    # You would follow this by collecting the data, handling the trigger, and analyzing the results.
    # Example: Fetch data and process (you would need to implement your data collection part here)

    ############
    
    status["runBlock"] = ps.ps5000aRunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, None, 0, None, None)
    assert_pico_ok(status["runBlock"])
    #print('assert_pico_ok(status["runBlock"])', assert_pico_ok(status["runBlock"]))
    
    # Check for data collection to finish using ps5000aIsReady
    ready = ctypes.c_int16(0)
    check = ctypes.c_int16(0)
    while ready.value == check.value:
        status["isReady"] = ps.ps5000aIsReady(chandle, ctypes.byref(ready))
        #print(f"Ready status: {ready.value}")



    # Create buffers ready for assigning pointers for data collection
    bufferAMax = (ctypes.c_int16 * maxSamples)()
    bufferAMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example
    bufferBMax = (ctypes.c_int16 * maxSamples)()
    bufferBMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example


    bufferCMax = (ctypes.c_int16 * maxSamples)()
    bufferCMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example
    bufferDMax = (ctypes.c_int16 * maxSamples)()
    bufferDMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example

    # Set data buffer location for data collection from channel A
    # handle = chandle
    

    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Channel A
    source = ps.PS5000A_CHANNEL["PS5000A_CHANNEL_A"]
    # pointer to buffer max = ctypes.byref(bufferAMax)
    # pointer to buffer min = ctypes.byref(bufferAMin)
    # buffer length = maxSamples
    # segment index = 0
    # ratio mode = PS5000A_RATIO_MODE_NONE = 0
    status["setDataBuffersA"] = ps.ps5000aSetDataBuffers(chandle, source, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxSamples, 0, 0)
    assert_pico_ok(status["setDataBuffersA"])

    # Set data buffer location for data collection from channel B
    # handle = chandle


    # Channel B
    source = ps.PS5000A_CHANNEL["PS5000A_CHANNEL_B"]
    # pointer to buffer max = ctypes.byref(bufferBMax)
    # pointer to buffer min = ctypes.byref(bufferBMin)
    # buffer length = maxSamples
    # segment index = 0
    # ratio mode = PS5000A_RATIO_MODE_NONE = 0
    status["setDataBuffersB"] = ps.ps5000aSetDataBuffers(chandle, source, ctypes.byref(bufferBMax), ctypes.byref(bufferBMin), maxSamples, 0, 0)
    assert_pico_ok(status["setDataBuffersB"])


    #Channel C
    source = ps.PS5000A_CHANNEL["PS5000A_CHANNEL_C"]
    # pointer to buffer max = ctypes.byref(bufferBMax)
    # pointer to buffer min = ctypes.byref(bufferBMin)
    # buffer length = maxSamples
    # segment index = 0
    # ratio mode = PS5000A_RATIO_MODE_NONE = 0
    status["setDataBuffersC"] = ps.ps5000aSetDataBuffers(chandle, source, ctypes.byref(bufferCMax), ctypes.byref(bufferCMin), maxSamples, 0, 0)
    assert_pico_ok(status["setDataBuffersC"])


    #Channel D
    source = ps.PS5000A_CHANNEL["PS5000A_CHANNEL_D"]
    # pointer to buffer max = ctypes.byref(bufferBMax)
    # pointer to buffer min = ctypes.byref(bufferBMin)
    # buffer length = maxSamples
    # segment index = 0
    # ratio mode = PS5000A_RATIO_MODE_NONE = 0
    status["setDataBuffersD"] = ps.ps5000aSetDataBuffers(chandle, source, ctypes.byref(bufferDMax), ctypes.byref(bufferDMin), maxSamples, 0, 0)
    assert_pico_ok(status["setDataBuffersD"])

    # create overflow loaction
    overflow = ctypes.c_int16()
    # create converted type maxSamples
    cmaxSamples = ctypes.c_int32(maxSamples)

    # Retried data from scope to buffers assigned above
    # handle = chandle
    # start index = 0
    # pointer to number of samples = ctypes.byref(cmaxSamples)
    # downsample ratio = 0
    # downsample ratio mode = PS5000A_RATIO_MODE_NONE
    # pointer to overflow = ctypes.byref(overflow))
    status["getValues"] = ps.ps5000aGetValues(chandle, 0, ctypes.byref(cmaxSamples), 0, 0, 0, ctypes.byref(overflow))
    assert_pico_ok(status["getValues"])


    # convert ADC counts data to mV
    adc2mVChAMax =  adc2mV(bufferAMax, chARange, maxADC)
    adc2mVChBMax =  adc2mV(bufferBMax, chBRange, maxADC)
    adc2mVChCMax =  adc2mV(bufferCMax, chARange, maxADC)
    adc2mVChDMax =  adc2mV(bufferDMax, chBRange, maxADC)

    # Create time data
    time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)

    # Stop the scope
    # handle = chandle
    status["stop"] = ps.ps5000aStop(chandle)
    assert_pico_ok(status["stop"])

    # Close unit Disconnect the scope
    # handle = chandle
    status["close"]=ps.ps5000aCloseUnit(chandle)
    assert_pico_ok(status["close"])

    # display status returns
    #print(status)
    if plots_signal:
        path_signal = 'signal'
        os.makedirs(path_signal, exist_ok = True)
        plt.figure(figsize = (7,5), dpi = 300)
        # plot data from channel A and B
        plt.plot(time/1e9, adc2mVChAMax[:], label = 'Channel A')
        plt.plot(time/1e9, adc2mVChBMax[:], label = 'Channel B')
        plt.plot(time/1e9, adc2mVChCMax[:], label = 'Channel C')
        plt.plot(time/1e9, adc2mVChDMax[:], label = 'Channel D', alpha = 0.5)
        plt.xlabel('Time (s)', size = 16)
        plt.legend()
        plt.grid(True)
        plt.title(f'{timestamp_str} time {round(sample_rate/1e6, 2)} MS/s', size = 20)
        plt.ylabel('Voltage (mV)', size = 16)
        plt.savefig(f'{path_signal}/signal_{timestamp_str}.png')
        plt.show()
   
    # Save to parquet
    mydict = {'adc2mVChAMax': adc2mVChAMax, 'adc2mVChBMax': adc2mVChBMax, 'adc2mVChCMax':adc2mVChCMax, 'adc2mVChDMax': adc2mVChDMax, 'time': time}
    df = pd.DataFrame(mydict)
    df['sampling_rate'] = sample_rate
    df['time_unit'] = 'ns'
    df['voltage_unit'] = 'mV'
    df['timestamp'] = f'{timestamp_str}'
    
    #print(timestamp_str)
    
    os.makedirs(f'{path_to_save_locally}', exist_ok=True)
    path_last = f'{path_to_save_locally}/aquisition_{timestamp_str}.parquet'
    df.to_parquet(path_last, engine = 'pyarrow')
    return path_last
    #print("Collecting data...") 
# Main loop for acquisition every 10 minutes

picoscope_flag = True
my_eos_folder = 'try'
os.makedirs(my_eos_folder, exist_ok=True)
while True:
    #a = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #print(a)
    if picoscope_flag:
        latest_file = collect_data(path_to_save_locally='.')  # Collect data
        # Copy to destination folder
        dest_path = os.path.join(my_eos_folder, latest_file)
        shutil.copy(latest_file, dest_path)
        print(f"Copied to {dest_path}")
    # Wait for 10 minutes (600 seconds)
    #print("Waiting for next acquisition cycle...")
    time_lib.sleep(5)  # 10 minutes in seconds

# %%
