#!/usr/bin/env python
# coding: utf-8

# # NE512 TMQ v2 - Test Case
# 
# This turorial illustrates using VCS and DV3D (CDAT tools) to create a 3D plot of E3SM ne512 regridded data. The goal of this test case is to determine if the CDAT tools can handle the larger file sizes presented by ne512 data.
# 
# [Download the Jupyter Notebook](https://cdat.llnl.gov/Jupyter-notebooks/scientific/ne512_Test_Case/ne512_TMQ_v2_Test_Case.ipynb)
# 
# [Download the Python file](https://cdat.llnl.gov/Jupyter-notebooks/scientific/ne512_Test_Case/ne512_TMQ_v2_Test_Case.py)
# 
# Only members of the E3SM project can access the data file for this notebook. To download the file, on NERSC, navigate to the following directory - /global/project/projectdirs/acme/www/hdavis/ne512/ - and download the data file:
# **add-ne512-grids.FC5AV1C-H01A.ne512np4_360x720cru_ne512np4.cori-knl_intel.1024x17x8.ifs-hindcast.20190610-1542.cam.h1.2016-08-01-00000.360x720cru_3D_all_hind.nc**
# 
# **Make sure the data file is in the same location/folder as the Jupyter Notebook and Python file.** The data file is a bit big at ~5.4 GB, so some of the commands in this notebook can take a little while to run. 
# 
# The CDAT software was developed by LLNL and this notebook was created and the example code was updated on December 17, 2019. This work was performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344.

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#To-Interact-with-the-3D-image..." data-toc-modified-id="To-Interact-with-the-3D-image...-1">To Interact with the 3D image...</a></span></li><li><span><a href="#Open-the-data-file" data-toc-modified-id="Open-the-data-file-2">Open the data file</a></span></li><li><span><a href="#Initialize-the-VCS-canvas" data-toc-modified-id="Initialize-the-VCS-canvas-3">Initialize the VCS canvas</a></span></li><li><span><a href="#Set-the-DV3D-settings" data-toc-modified-id="Set-the-DV3D-settings-4">Set the DV3D settings</a></span></li><li><span><a href="#Load-TMQ-data" data-toc-modified-id="Load-TMQ-data-5">Load TMQ data</a></span></li><li><span><a href="#Create-the-3D-plot" data-toc-modified-id="Create-the-3D-plot-6">Create the 3D plot</a></span></li><li><span><a href="#Save-a-2D-image-of-the-3D-plot" data-toc-modified-id="Save-a-2D-image-of-the-3D-plot-7">Save a 2D image of the 3D plot</a></span></li></ul></div>

# ## To Interact with the 3D image... 
# You will ultimately need to run the Python code in this notebook in a command line window, not within this notebook. One possible work flow is:
# 1. Step through this notebook line by line to make sure everything works (you are running an environment with the needed packages, the code is working for you with the sample data, etc.).
# 2. Once everything is working, either use the Python file we've provided above or save this notebook as a Python file by clicking on File (within the JupyterLab interface) > Export Notebook As... > Export Notebook to Executable Script.
# 3. If you save/export the script from this notebook, you will need to edit the .py file to remove the "#" symbol infront of the x.interact() command near the bottom of the file. (If you download the python script directly, no editing is necessary.)
# 4. Open a new command line window and activate your favorite CDAT environment (for testing this notebook, I used a CDAT 8.1 mesalib environment, but you could also use a [jupyter-vcdat environment after installing VCDAT](https://github.com/CDAT/jupyter-vcdat/wiki/Deploy). **(Note: When you run the Python script to create the interactive window of the 3D data, make sure you are using a "regular" version of the conda environment - NOT a mesalib version - since you will need to see the window that opens as the Python script runs. (Mesalib environments suppress this window.))**
# 5. Navigate to where the Python script is stored and type the following at the prompt: 
# ``` 
# python -i ne512_TMQ_v2_Test_Case.py
# ```
# The generic interactive Python command is:
# ```
# python -i Name_of_Your_Notebook.py
# ```
# 
# 
# A separate window should open where you can adjust the sliders and click on the "Configure" button to access more features of the plot. Click and drag on the center of the plot to change the angle at which you are viewing the data.
# 
# To exit the interactive mode, close the window and type control-D within your command line window to fully exit the interactive mode and to get your command prompt back. (If for some reason control-D does not work, try control-Z.)
# 
# 
# An alternate work flow is to accomplish all the steps above in a command line window without using JupyterLab or the Jupyter Notebook.

# In[1]:


import vcs, cdms2, sys


# ## Open the data file
# Ben Hillman provided data files from a ne512 run regridded from E3SM's native grid to latitude and longitude. 
# 
# The variables were all 2D and since I wanted to test if VCS and DV3D could handle the larger file size of a 3D ne512 run, I added a random 3D component to the TMQ data for test purposes. 
# 
# **TMQ is the total (vertically integrated) precipitable water.** 
# 
# The name of this 3D test data file is "add-ne512-grids.FC5AV1C-H01A.ne512np4_360x720cru_ne512np4.cori-knl_intel.1024x17x8.ifs-hindcast.20190610-1542.cam.h1.2016-08-01-00000.360x720cru_3D_all_hind.nc"

# In[2]:


f=cdms2.open("./add-ne512-grids.FC5AV1C-H01A.ne512np4_360x720cru_ne512np4.cori-knl_intel.1024x17x8.ifs-hindcast.20190610-1542.cam.h1.2016-08-01-00000.360x720cru_3D_all_hind.nc")


# ## Initialize the VCS canvas
# In this example, the VCS canvas is called "x".

# In[3]:


x = vcs.init()


# ## Set the DV3D settings
# Choose various DV3D settings for the type of plot you want to make.

# In[4]:


dv3d = vcs.get3d_scalar()


# In[5]:


dv3d.ToggleVolumePlot = vcs.on


# In[6]:


dv3d.Camera={'Position': (-161, -171, 279), 'ViewUp': (.29, 0.67, 0.68), 'FocalPoint': (146.7, 8.5, -28.6)}


# ## Load TMQ data
# 
# The variable "v" holds the 3D TMQ (total (vertically integrated) precipitable water) test data.

# In[7]:


v = f["TMQ"]


# The next line determines the min and max of values for the "v" variable in our NetCDF file. It might take a while for this line to run.

# In[8]:


import genutil
genutil.minmax(v)


# Modify the ScaleColormap to cover the min and max values of the data.

# In[9]:


dv3d.VerticalScaling = 4.0 
dv3d.ScaleColormap = [0.07, 169.0, 1] 
dv3d.ScaleTransferFunction =  [0.07, 169.0, 1]


# NOTE: when running the Python script outside of the Jupyter notebook in order to interact with the data visualization, I received the following error when I tried to adjust the "Range Max" slider which controls the maximum data value that is shown on the 3D plot:
# ```
# "Warning: In ../Rendering/VolumeOpenGL2/vtkOpenGLVolumeOpacityTable.h, line 191
# vtkObject (0x7fad03973b90): This OpenGL implementation does not support the required texture size of 32768.
# Falling back to maximum allowed, 16384.This may cause an incorrect color table mapping."
# ```

# ## Create the 3D plot
# Plotting the data takes a while.

# In[10]:


x.plot( v, dv3d )


# If you want to save a python script from this notebook to run outside the notebook, save the script then edit it to un-comment out the following line so you can interact with the 3D image in the window that opens after running the x.plot( v, dv3d ) command.

# In[11]:


x.interact()


# ## Save a 2D image of the 3D plot
# When working inside a notebook, saving the above image to a separate .png file could be useful if you want to look at the image outside of the notebook. The line of code below will save the plot to a .png file in the same directory as this notebook.
# 
# If running the code in this notebook from the corresponding Python script, comment out or delete the following line of code since in the direct Python interface, saving to a .png file results in an all black .png file. If you want a 2D image of a particular view you've created while interacting with the 3D image, taking a screenshot is a good option.

# In[12]:


#x.png("ne512_test_TMQ_v2.png")

