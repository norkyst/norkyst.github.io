"""
Timeseries
=============================================================================
"""

# %% [markdown]
# This notebook will give examples on how to use data from the Norkyst v3 ocean model to make timeseries. Data is accessed through the Norwegian Meteorological Insitute's THREDDS server: https://thredds.met.no/thredds/catalog.html.

# %%
# Importing useful Python packages
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

# %%
# Reading in the path from thredds.met.no, using an OPENDAP url
path = 'https://thredds.met.no/thredds/dodsC/fou-hi/norkystv3_800m_m00_be'

# Opening a netCDF file as xarray dataset
ds = xr.open_dataset(path)

# %%
# Example from an arbitrary grid point.
ds.temperature.isel(time=slice(0,100) ,X=1000, Y=1000, depth=0).plot()
plt.show()

