#1)
import pandas as pd   #to read and import info from file
import glob, os
import os.path #to define a path for a specific folder
import scipy as sp
from scipy.signal import find_peaks, peak_prominences, peak_widths #to find peaks and export prominences
import numpy as np   
from bokeh.io import output_notebook, show  #this and following for interactive plots
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper, PrintfTickFormatter
from bokeh.models.tickers import FixedTicker
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot
from bokeh import __version__ as bp
from IPython import __version__ as ipython_version
output_notebook()     #this will ensure that all plots are open in the same page. Without this plots will open in a new window

#2)
home_dir = "file_path"
df = pd.read_csv(home_dir + 'file_name.csv') #this is to read the file

#3)
ca_file = home_dir + 'analyzed_trace_file_name.csv'
prom_file = home_dir + 'prominence_saved_file_name.csv'

#4)
t = df.loc[:,"Time(s)"]   #change name of the columns accordingly
ch405 = df.loc[:,"ch405"]      #change name of the columns accordingly
ch465 = df.loc[:,"ch465"]      #change name of the columns accordingly

#5) calculating deltaF / F = (F - F0) / F0
bg = ((ch405 - ch405.rolling(window=125).mean())/ch405.rolling(window=125).mean()).rolling(window=25).mean()
norm = ((ch465 - ch465.rolling(window=125).mean())/ch465.rolling(window=125).mean()).rolling(window=25).mean()
dFF = (norm - bg)

#6) filter outliers
mean = np.mean(dFF, axis=0)
sd = np.std(dFF, axis=0)
ca = np.where((dFF>(mean + (10 * sd))), mean, dFF)
ca = np.where((ca<(mean - (2 * sd))), mean, ca)
ca = pd.Series(ca)

#7)
peaks, _ = find_peaks(ca, height=None, threshold=None, distance=120, prominence=(0.03, 0.5), width=None, wlen=None, rel_height=None, plateau_size=None)
base = ca.rolling(window=500).mean()

#8) include as many lines you need in the plot. It can be just the final normalized dF/F trace
p = figure(plot_height=450, plot_width=800)   #this will decide the size of the plot. 
p.line(t, ch405, legend="405", line_width=0.5)    #this will plot one trace. Deafult color is blue. Add line_color for chosing a differnt one
p.line(t, ch465, legend="465", line_width=0.5)   #the first value is the x axis (time), the second value is the trace
p.line(t, bg, legend="Norm405", line_width=0.5, line_color='blue')
p.line(t, norm, legend="Norm465", line_width=0.5, line_color='green')
p.line(t, dFF, legend="dFF", line_width=0.5, line_color='gray')
p.line(t, ca, legend="ca", line_width=0.5)
p.line(t, base, legend="baseline", line_width=2, line_color='orange')
p.xgrid.grid_line_color = None   #this will remove the grid
p.ygrid.grid_line_color = None
p.circle(t[peaks], ca[peaks], legend='Ca_peaks', fill_color="orange", size=5)    #this will create a circle at each identified peak
p.xaxis.axis_label = 'time(s)'    #this will add a label
p.yaxis.axis_label = 'Norm. F'
p.legend.click_policy="hide"     #this will allow you to hide specific traced from the plot after you created (interactive legend)
show(p)     #this will show the plot

#9) output the info about peak events and save to csv
prom = peak_prominences(ca, peaks)[0]     #this will calculate the prominence (amplitude) of each peak
pks_t = t.loc[peaks]      #this will identify the corresponding time (from column time) for each peak
s = pd.DataFrame(prom)       #this will create a data frame that can be analyzed
sd = pd.DataFrame(s.describe())   #this will analyze the series and calculated average value, max, min, total cound of events

#10) group into one file and save
t = pd.DataFrame(t)
ch405 = pd.DataFrame(ch405)
ch465 = pd.DataFrame(ch465)
bg = pd.DataFrame(bg)
norm = pd.DataFrame(norm)
dFF = pd.DataFrame(dFF)
ca = pd.DataFrame(ca)
ca_base = pd.DataFrame(base)
pks = pd.DataFrame(pks)
t.insert(1, 'ch405', ch405)
t.insert(2, 'ch465', ch465)
t.insert(3, 'background', bg)
t.insert(4, 'ch465_norm', norm)
t.insert(5, 'dFF', dFF)
t.insert(6, 'ca', ca)
t.insert(7, 'ca_base', ca_base)
t.insert(8, 'ca_noBase', pks)
t.to_csv(ca_file)        #save traces
sd.to_csv(prom_file)       #save peaks info
