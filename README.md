# DeepFRi-and-DiFR
This project contains the required functions to create lists of auto-detected flux ropes and their geoeffectiveness directly from solar wind magnetic field data. This uses a pipeline that has two AI models. The first one that detects the FRs is DeepFRi -- "Deep convolutional neural network FR identification”. The second model that detects the geoeffectiveness of FRs is DicFR -- "Disturbance storm time Dst index classification of identified FRs". 
The 'main.ipynb' shows an example of creating lists of FRs and their geoeffectiveness. This accepts the start and end time of solar wind duration under question. The input and output of the example are kept in ./nrt_wind/test.
The 'plot_main.ipynb' plots the duration of the solar wind magnetic field data interval in question and indicates the auto-detected FRs if found. 
The python files inside the 'nrt_wind' folder contain functions for pre-processing ('Pre_processing.py') solar wind data, DeepFRi ('DeepFRi_test.py') and DicFR ('DicFR_test.py') models and post-processing ('Post-processing.py') the model outputs to prepare autodetected FR lists -- 'List 1', 'List 2' and 'Final list'. 
The folder 'catalog' contains the 'List 1', 'List 2' and 'Final list' created during the model testing period during 2008-2014. The 'Final list' contains the auto-detected geoeffective flux ropes during the mentioned interval.
For more details see the published article titled as Automatic Detection of Large-scale Flux Ropes and Their Geoeffectiveness with a Machine-learning Approach, The Astrophysical Journal, Volume 972, Number 1, DOI 10.3847/1538-4357/ad54c3.
If you decide to use this in your work please cite the article as Citation: Sanchita Pal et al 2024 ApJ 972 94 and reach out the email:sanchita.pal1@outlook.com for possible collaboration.


This pipeline can be directly used at https://colab.research.google.com/. Please use !git clone https://github.com/spal4532/DeepFRi-and-DicFR.git first and set a time window in main.ipynb and then run it to see the automatically identified geoeffective solar wind intervals.
