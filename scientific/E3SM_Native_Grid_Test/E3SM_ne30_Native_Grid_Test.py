#!/usr/bin/env python
# coding: utf-8

# # E3SM ne30 Native Grid Test
# 
# This turorial using VCS and DV3D (CDAT tools) to create a 3D plot of temperature data on E3SM's ne30 native grid.
# 
# [Download the Jupyter Notebook](https://cdat.llnl.gov/Jupyter-notebooks/scientific/E3SM_ne30_Native_Grid_Test/E3SM_ne30_Native_Grid_Test.ipynb)
# 
# [Download the Python file](https://cdat.llnl.gov/Jupyter-notebooks/scientific/E3SM_ne30_Native_Grid_Test/E3SM_ne30_Native_Grid_Test.py)
# 
# The CDAT software was developed by LLNL and this notebook was created and the example code was updated on December 17, 2019. This work was performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344.

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#To-Interact-with-the-3D-image..." data-toc-modified-id="To-Interact-with-the-3D-image...-1">To Interact with the 3D image...</a></span></li><li><span><a href="#Get-the-tutorial-data" data-toc-modified-id="Get-the-tutorial-data-2">Get the tutorial data</a></span></li><li><span><a href="#Open-the-CMIP6-data-file" data-toc-modified-id="Open-the-CMIP6-data-file-3">Open the CMIP6 data file</a></span></li><li><span><a href="#Initialize-the-VCS-canvas" data-toc-modified-id="Initialize-the-VCS-canvas-4">Initialize the VCS canvas</a></span></li><li><span><a href="#Set-the-DV3D-settings" data-toc-modified-id="Set-the-DV3D-settings-5">Set the DV3D settings</a></span></li><li><span><a href="#Choose-a-variable-to-plot" data-toc-modified-id="Choose-a-variable-to-plot-6">Choose a variable to plot</a></span></li><li><span><a href="#Create-the-3D-plot" data-toc-modified-id="Create-the-3D-plot-7">Create the 3D plot</a></span></li><li><span><a href="#Save-a-2D-image-of-the-3D-plot" data-toc-modified-id="Save-a-2D-image-of-the-3D-plot-8">Save a 2D image of the 3D plot</a></span></li></ul></div>

# ## To Interact with the 3D image...
# 
# You will ultimately need to run the Python code in this notebook in a command line window, not within this notebook. One possible work flow is:
# 
# 1. Step through this notebook line by line to make sure everything works (you are running an environment with the needed packages, the code is working for you with the sample data, etc.).
# 2. Once everything is working, either use the Python file we've provided above or save this notebook as a Python file by clicking on File (within the JupyterLab interface) > Export Notebook As... > Export Notebook to Executable Script.
# 3. If you save/export the script from this notebook, you will need to edit the .py file to remove the "#" symbol infront of the x.interact() command near the bottom of the file. (If you download the python script directly, no editing is necessary.)
# 4. Open a new command line window and activate your favorite CDAT environment (for testing this notebook, I used a CDAT 8.1 mesalib environment, but you could also use a [jupyter-vcdat environment after installing VCDAT](https://github.com/CDAT/jupyter-vcdat/wiki/Deploy). **(Note: When you run the Python script to create the interactive window of the 3D data, make sure you are using a "regular" version of the conda environment - NOT a mesalib version - since you will need to see the window that opens as the Python script runs. (Mesalib environments suppress this window.))**
# 5. Navigate to where the Python script is stored and type the following at the prompt:
# ```
# python -i E3SM_ne30_Native_Grid_Test.py
# ```
# The generic interactive Python command is:
# ```
# python -i Name_of_Your_Notebook.py
# ```
# 
# A separate window should open where you can adjust the sliders and click on the "Configure" button to access more features of the plot. Click and drag on the center of the plot to change the angle at which you are viewing the data.
# 
# To exit the interactive mode, close the window and type control-D within your command line window to fully exit the interactive mode and to get your command prompt back. (If for some reason control-D does not work, try control-Z.)
# 
# An alternate work flow is to accomplish all the steps above in a command line window without using JupyterLab or the Jupyter Notebook.

# In[1]:


import vcs, cdms2, sys


# ## Get the tutorial data
# This tutorial uses the E3SM model version 1, 1 degree (standard resolution (ne30)) CMIP6 data which is available on NERSC's HPSS storage system. See the [V1 1 Deg CMIP6 Data on HPSS](https://e3sm.org/data/get-e3sm-data/released-e3sm-data/v1-1-deg-data-cmip6/v1-1-deg-cmip6-data-on-hpss/) post on the E3SM.org website to download the data.
# 
# The data file for this tutorial is "20180129.DECKv1b_piControl.ne30_oEC.edison.cam.h0.0500-01.nc" from the CMIP6 standard resolution (ne30) piControl run. 
# 
# The grid file used is "ne30np4_latlon.091226.nc". To download this grid file, go to https://portal.nersc.gov/project/acme/hdavis/ and click on the "ne30np4_latlon.091226.nc" file whcih should automatically download via your browser. To facilitate running this notebook, the CMIP6 data file can also be downloaded from this same location.
# 
# Make sure both the data file and the grid file are in the same directory as this notebook before proceeding with running the notebook.

# ## Open the CMIP6 data file
# The variable "f" (for file) references the data file.

# In[2]:


f=cdms2.open("20180129.DECKv1b_piControl.ne30_oEC.edison.cam.h0.0500-01.nc")


# ## Initialize the VCS canvas
# In this example the variable "x" is the VCS canvas.

# In[3]:


x = vcs.init()


# ## Set the DV3D settings
# Choose various DV3D settings for the type of plot you want to make.

# In[4]:


dv3d = vcs.get3d_scalar()


# In[5]:


dv3d.ToggleVolumePlot = vcs.on
dv3d.ToggleSphericalProj = vcs.on


# In[6]:


dv3d.Camera={'Position': (-161, -171, 279), 'ViewUp': (.29, 0.67, 0.68), 'FocalPoint': (146.7, 8.5, -28.6)}


# ## Choose a variable to plot
# The next line of code shows us all the data variables within the CMIP6 netCDF file.

# In[7]:


print(sorted(f.variables.keys()))


# The variable we'll plot in this tutorial is temperature, T which is in degrees Kelvin. The next line assigns the temperature data (T) to the "v" variable.

# In[8]:


v = f["T"]


# To ensure the color scale of our plot covers the minimum and maximum values of the data, we'll first determine min and max values, then modify the colormap scale.
# 
# Both VCS and Genutil have minmax functions. Here we'll use VCS's minmax function, but if you'd like to use Genutil's function instead, comment out the first line of code and un-comment the second and third lines. 

# In[9]:


vcs.minmax(v)

#import genutil
#genutil.minmax(v)


# Modify the ScaleColormap to cover the min and max values of the data.

# In[10]:


dv3d.VerticalScaling = 1.5 
dv3d.ScaleColormap = [184.0, 308.0, 1] 
dv3d.ScaleTransferFunction =  [184.0, 308.0, 1]


# ## Create the 3D plot

# In[11]:


x.plot( v, dv3d, grid_file="ne30np4_latlon.091226.nc")


# If you want to interact with the 3D plot, save a python script from this notebook to run outside the notebook, then edit the python script to un-comment out the following line. Use a non-mesalib conda environment when running the Python script so you can interact with the 3D image in the window that opens after running the x.plot( v, dv3d ) command.

# In[12]:


x.interact()


# ## Save a 2D image of the 3D plot
# When working inside a notebook, saving the above image to a separate .png file could be useful if you want to look at the image outside of the notebook. The line of code below will save the plot to a .png file in the same directory as this notebook. 
# 
# If running the code in this notebook from the corresponding Python script, comment out or delete the following line of code since in the direct Python interface, saving to a .png file results in an all black .png file. If you want a 2D image of a particular view you've created while interacting with the 3D image, we recommend taking a screenshot.

# In[13]:


#x.png("native_T_sphere.png")

