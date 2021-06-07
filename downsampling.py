#1)
import pandas as pd   #to read and import info from file
import glob, os
import os.path #to define a path for a specific folder

#2)
#This is to select the path to the folder and the specific file
# and the folder where to save the results
home_dir = "file_path"
df = pd.read_csv(home_dir + 'file_name', skiprows=1)     #this is to read the file / change file name accordingly

#3)
save_dir = "file_path"     #chose where to save the file. It can be the same as home_dir
save_df = save_dir + 'saved_file_name'      #chose the name of the file you want to save

#4)
t = df.loc[:,"Time(s)"]           #this will read the "Time(s)" column
ch405 = df.loc[:,"AIn-1 - Dem (AOut-1)"]    #change accordingly to Input and Output of a specific setup
ch465 = df.loc[:,"AIn-1 - Dem (AOut-2)"]    #change accordingly to Input and Output of a specific setup
t = (t[0:t.size:4])
ch405 = (ch405[0:ch405.size:4])
ch465 = (ch465[0:ch465.size:4])

#5)
t = pd.DataFrame(t)
ch405 = pd.DataFrame(ch405)
ch465 = pd.DataFrame(ch465)
t.insert(1, 'ch405', ch405)
t.insert(2, 'ch465', ch465)

t.to_csv(save_df)
