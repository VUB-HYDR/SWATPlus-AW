'''
date        : 31/03/2020
description : this is a template for configs

author      : Celray James CHAWANDA
contact     : celray.chawanda@outlook.com
licence     : MIT 2020
'''

config_string = """'''----------------- QSWAT+ Workflow v1.0.4 Settings File --------------'''

# Project Identification
Project_Name          = "{prj_name}"
Model_2_config        = True        # True = get settings from existing model 
                                    # False = get model from current settings

'''---------------------------- File Names ---------------------------'''
# Raster files (Should be projected with the same projection)
Topography            = "{dem_fn}"
Soils                 = "{soil_fn}"
Land_Use              = "{landuse_fn}"


# Database Files
Soil_Lookup           = "{soillookup_fn}"
Landuse_Lookup        = "{landuselookup_fn}"
Usersoil              = "{usersoil_fn}"

# Shape Files
Outlets               = "{outlets_fn}" # it should have same format as in the example

'''---------------------------  Project Options  ----------------------'''
# Watershed Deliniation (1 = Cells)
Ws_Thresholds_Type    = {ws_threshold_type}            
Channel_Threshold     = {channel_threshold}
Stream_Threshold      = {stream_threshold}
Out_Snap_Threshold    = {shap_threshold}                # metres 
Burn_In_Shape         = ""                 # leave as "" if none

#  -------------------  HRU Definition  ------------------
Slope_Classes         = "{slope_classes}"

# HRU creation method   (1 = Dominant landuse, soil, slope , 2 = Dominant HRU,
#                        3 = Filter by Area,                 4 = Target Number of HRUs,
#                        5 = Filter by landuse, soil, slope)

HRU_Filter_Method     = {hru_method}

# Thresholds_Type           (1 = Total Area (ha) , 2 = Percent)
HRU_Thresholds_Type   = {hru_threshold_type}
Land_Soil_Slope_Thres = "{land_soil_slope_thresholds}"    # Thresholds for Landuse, Soil and Slope. Leave as "" if not needed
Target_Area           = {target_area}             # used if HRU_Filter_Method 3 is selected
Target_Value          = {target_value}             # used if HRU_Filter_Method 4 is selected

# Routing and ET and infiltration
ET_Method             = {et_method}           # 1 = Priestley-Taylor, 2 = Penman-Monteith,
                                    # 3 = Hargreaves,      (4 = Observed - Not supported Currently)
Routing_Method        = {routing_method}           # 1 = Variable Storage,        2 = Muskingum
Routing_Timestep      = {routing_timestep}           # 1 = Daily Rainfall/routing, curve number
                                    # 2 = Sub-daily Rainfall/routing, Green & Ampt

# management of reservoirs and landuse
launduse_management_settings = [
    # This entry is an example. Remove the '#' at the begining of each line to activate. Repeat the block to add more

    # {{
    #     "landuse": "agrl",
    #     "mgt_sch": "agric_lu",
    #     "auto_sch1": "fert_rot_1",

    #     "op_sch1": {{"op_typ": "plnt", "date": "29/01", "harvest_part": None, "op_data3": 0, "rot_year": 1}},
    #     "op_sch2": {{"op_typ": "harv", "date": "09/05", "harvest_part": "grain", "op_data3": 0, "rot_year": 1}},
    # }}
]

reservoir_management_settings = [
    # This entry is an example. Remove the '#' at the begining of each line to activate. Repeat the block to add more

    #{{ 
    #     "id": 1,
    #     "set_res_name": "test_reservoir",
    #     "principal_area": 1547,  # m2
    #     "emergency_area": 1747,  # m2
    #     "principal_volume": 1547,  # m3
    #     "emergency_volume": 1847,  # m3
    #     "dtl_name": "my_dtl",
        
    #     # dd/mm/yyyy (the date when the reservoir became operational)
    #     "date_operational": "01/01/1993",

    #     "cond1": {{"main_variable": "vol", "limiting_var": "e-pv", "limit_operator": "=", "alts": ["=", "-"], "constraint": "-14.93"}},
    #     "cond2": {{"main_variable": "vol", "limiting_var": "e-pv", "limit_operator": "<", "alts": [">", "<"], "constraint": "5.93"}},

    #     "act1": {{"name": "over_prin", "action_type": "release", "action_option": "days",  "fp": "cond1", "const1": "1.777", "const2": "1.777", "out_switches": ["y", "y"]}},
    #     "act2": {{"name": "over_emergency", "action_type": "release", "action_option": "days",  "fp": "cond1", "const1": "1.777", "const2": "1.777", "out_switches": ["n", "y"]}},
    #     "act3": {{"name": "flood", "action_type": "release", "action_option": "days",  "fp": "cond1", "const1": "1.777", "const2": "1.777", "out_switches": ["y", "n"]}},
    # }}
]

# model run settings
Start_Year            = {start_year}
End_Year              = {end_year}
Warm_Up_Period        = {warm_up}           # the number of years for running the model without printing output

Print_CSV             = 1           # 0 = no, 1 = yes, selection to output csv files

Print_Objects         = {{           # 1 = daily, 2 = month, 3 = year, 4 = annual average
                                    # default prints yearly results if not specified or if object is not in the list

{print_objects}
                        }}

Executable_Type       = 1             # 1 = Release, 2 = Debug   0 = Don't run

Cal_File              = "{calfile_name}"            # a calibration.cal file with parameters for the calibrated model
                                      # leave as "" if there is no file to be used.

Calibrate               = False       # set to "True" to perform calibration, "False" to skip calibration
Calibration_Config_File = "calibration_config.csv"             # not used if Calibrate is set to False 
Number_of_Runs          =   10        # Set the number of runs for calibration
Number_of_Processes     =   1         # Set the number of parallel processes to make calibration faster

Make_Figures            = False       # set to "True" to create maps, "False" to skip map creation

# Log progress or not? If yes, you will not see updates
Keep_Log                = True        # True or False
'''---------------------------  Settings End  -----------------------'''"""

calibration_config_template = """Parameter,Minimum,Maximum,Change Type,
"1 = pctchg, 2 = abschg, 3 = absval",,,,
File Name:,,observed_flows.csv,,
Channel Number:,,35,,
Timestep:,,2,,"1 = day, 2 = month, 3 = year"
Calibration Variable:,,1,,"1 = flow, 2 = evapotranspiration"
,,,,
Parameter,Min,Max,Change Type,
cn2,-25,25,pctchg,
esco,-0.6,0.6,abschg,
perco,-20,20,pctchg,
awc,-20,20,pctchg,
surlag,-20,20,pctchg,
alpha,-20,20,pctchg,
"""
