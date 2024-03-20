# DeepFRi-and-DiFR
This project contains the required functions to create lists of auto-detected flux ropes and their geoeffectiveness directly from solar wind magnetic field data.
The 'main.ipynb' shows an example of how to create lists of FRs and their geoeffectiveness. This accepts the start and end time of solar wind duration under question.
The 'plot_main.ipynb' plots the duration of the solar wind magnetic field data interval in question and indicates the auto-detected FRs if found. 
The python files inside the `nrt_wind' folder contain functions for pre-processing ('Pre_processing.py') solar wind data, DeepFRi ('DeepFRi.py') and DiFR ('DiFR.py') models and preparing autodotected FR lists -- 'List 1', 'List 2' and 'Final list' ('Prepare_list.py'). 
For more details on the codes see the paper attached.
The folder `catalog' contains the 'List 1', 'List 2' and 'Final list' created during the model testing period during 2008-2014. 
