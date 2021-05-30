# Calcium_peaks_analysis
Python scripts to detect peaks in photometric calcium signal

This code is for analysis of calcium traces recorded thhrough Doric Neuroscience Studio.
The software can record multiple channels. This cose if for recording at two wavelengths: 405nm, isosbestic point for GCaMP6f, used to remove background noise, and 465nm, for detection of calcium changes. 

File 1: downsampling

Record Calcium traces at 120 samples per seconds. Use the following script do reduce to 30samples/sec if your recording does not require high resolution (Calcium peaks are generally 2 to 5 seconds long, so 120samples/sec is not necessary).

1) Import libraries as needed
2) chose the path to file and the file to read. Doric Studio output files come with two header rows. Remove the first row (not needed) with skiprows=1
3) chose the path where to save the file and the name of the file you want to create
4) from the file, select all the columns that you want to downsample. Then reduce from 120 to 30 samples (4 to 1). This code will select and output one sample every 4 rows. In our case 405 corresponds to Analog Input 1 demodulated to Output 1 - AIn-1 - Dem (AOut-1); and 465 corresponds to Analog Input 1 demodulated to Output 2 - AIn-1 - Dem (AOut-2). This will depend on specific connection in your Doric setup. Change accordingly.
5) Create a data frame containing the new (downsampled) columns and save to file previously chosen.

File 2: trace analysis

This code will detect the data of interest and smnooth each trace to remove noise, remove 405 background signal from 465 signal to generate deltaF/F resulting trace, will plot all filter outliers, will plot all traces, will detect and output all peaks and their prominence (amplitude)

1) Import libraries as needed
2) chose the path to file and the file to read.
3) chose the path where to save the file and the name of the file(s) you want to create
4) select columns from file to analyze
5) calculate deltaF/F. First create a rolling average for each trace to reduce noise and smooth the signal. The function .rolling will create a new series in which each sample is averaged with the preceeding x number of samples (rolling value will depend on how clear/noisy is your signal). In this case we average every 125 samples. Then, create a deltaF/F for each individual signal by using this formula dF/F=(F-F0)/F0. Finally, subtract background (405 signal) from the Ca2+ trace (465 signal).
6) Filter outliers (artifact, background noise, excessive banding of the cable that may have affected the signal). This function will eliminate everything above or below a certain standard deviation and substitute it with an average value for the entire trace.
7) find peaks and create a baseline (rolling mean from Ca2+ trace)
8) plot traces. Using bokeh library you can create interactive plots in which you can add and remove which item to show in the plot. You can also zoom in and inspect the plot, and save any format that you need.
9) calculate peak average value, number of peaks, max and min
10) save all information in .csv format
