# %% [markdown]
# # Timeseries

# %% [markdown]
# This notebook will give examples on how to use data from the Norkyst v3 ocean model to make timeseries. Data is accessed through the Norwegian Meteorological Insitute's THREDDS server: https://thredds.met.no/thredds/catalog.html.
# 
# __Python requirements__:
# To access the model output data we will use:
# * `xarray` for for opening and reading the netCDF files, see: https://docs.xarray.dev/en/stable/user-guide/index.html
# * `Matplotlib` for plotting, see: https://matplotlib.org/stable/users/index.html
# * `NumPy` for calculations on arrays, see: https://numpy.org/doc/
# * `xroms` for special functions made for ROMS output files, see: https://xroms.readthedocs.io
# * `Cartopy`for plotting on maps, see: https://scitools.org.uk/cartopy/docs/latest/

# %%
# Importing useful Python packages
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import xarray as xr

# %% [markdown]
# ### Accessing the data
# Data can be found at https://thredds.met.no/thredds/catalog.html.
# Locate project, folder and files. Here we will use OPENDAP url to read in the data.
# To get the OPENDAP URL, click on the desired NetCDF file (.nc). Under the "ACCESS" section, select the OPENDAP URL and then copy the URL located under "DATA URL".
# 
# For more details on the model and data, see the notebook `about_norkystv3.ipynb`.

# %%
# Reading in the path from thredds.met.no, using an OPENDAP url
path = 'https://thredds.met.no/thredds/dodsC/fou-hi/norkystv3_800m_m00_be'

# Opening a netCDF file as xarray dataset
ds = xr.open_dataset(path)

# Viewing the dataset
ds

# %% [markdown]
# For starters, we can with only one line make a simple timeseries plot:

# %%
ds.temperature.isel(time=slice(0,100) ,X=1000, Y=1000, depth=0).plot()

# %% [markdown]
# Further, we will look at examples of how to make timeseries from a given point location within the domain.

# %%
# Location west of Lofoten
loc = [12.72, 68.35]  # longitude, latitude

# %% [markdown]

# The coordinates above were randomly chosen and are not necessarily found explicitly on the model grid. Therefore, we need to find the closest point using the `xroms` function `.argsel2d()`.

# %%
y_idx, x_idx = xroms.argsel2d(ds.lon, ds.lat, loc[0], loc[1])

# %% [markdown]
# Note that the function return the indices in the order `y, x` and _not_ `x, y`.

# %%
print(f'Target location was: {loc}')
print()
print(f'Location found in dataset is: {ds.lon[y_idx, x_idx].values, ds.lat[y_idx, x_idx].values}')

# %% [markdown]
# For illustration purposes, we can include our location on a map:

# %%
fig, ax = plt.subplots(subplot_kw={'projection':ccrs.Mercator()}, constrained_layout=True)

# Plotting the temperature field of the first time step, uppermost z-layer and all lats/lons
ds.temperature[0, 0, :, :].plot(ax=ax, x='lon', y='lat', transform=ccrs.PlateCarree())
ax.set_title('')
# Including a marker for our location
ax.plot(ds.lon[y_idx, x_idx], ds.lat[y_idx, x_idx], '*', transform=ccrs.PlateCarree(), color='black', markersize=7)

# Cosmetics

# Gridlines
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=1, color='lightgray', alpha=0.5, linestyle='--')
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.top_labels = False
gl.right_labels = False

# Adding elements to our map making it prettier
land = cfeature.NaturalEarthFeature(category='physical', name='land', scale='50m', edgecolor='gray', facecolor=cfeature.COLORS['land'])
coastline = cfeature.NaturalEarthFeature(category='physical', name='coastline', scale='50m', edgecolor='gray', facecolor='none')
borders = cfeature.NaturalEarthFeature(category='cultural', name='admin_0_boundary_lines_land', edgecolor= 'gray', scale='50m', facecolor='none')

ax.add_feature(land)
ax.add_feature(coastline)
ax.add_feature(borders)

fig.suptitle('Location of interest shown on map', x=0.5, y=1.05)

# %% [markdown]
# From our target location we can retrieve timeseries of various variables using the indices we found. Here are some examples:

# %%
# Simple raw plot of temperature and salinity for the surface layer

fig, ax = plt.subplots()

# First 100 timesteps, uppermost z-level and indices of y and x of location
ds.temperature[0:100, 0, y_idx, x_idx].plot(ax=ax, color='red', label='Temperature') 
ax.tick_params(axis='y', labelcolor='r')
ax.legend()

ax1 = ax.twinx()  # Sharing x-axis, but different y-axes

# First 100 timesteps, uppermost z-level and indices of y and x of location
ds.salinity[0:100, 0, y_idx, x_idx].plot(ax=ax1, color='blue', label='Salinity')
ax1.tick_params(axis='y', labelcolor='b')
ax1.legend()

# Not very necessary, but removing the default title for a prettier plot:
ax.set_title('')
ax1.set_title('')

fig.suptitle(f'Temperature and salinity at 0 m depth, loc: ({ds.lat[y_idx, x_idx].item():.2f} , {ds.lon[y_idx, x_idx].item():.2f})')

# %% [markdown]
# One could also be intersted in looking into the current speeds and directions at a given location:

# %% [markdown]
# In the dataset we have the velocities of `u_eastward` and `v_northward`, meaning the velocity components on the lat-lon grid. However, if we want to say anything about the speed in a given point, we have to use that the speed is given by the magnitude of the velocity vector:
# 
# $S = |\vec v| = \sqrt{u² + v²}$

# %%
current_speed = np.sqrt(ds.u_eastward[0:100, 0, y_idx, x_idx]**2 + ds.v_northward[0:100, 0, y_idx, x_idx]**2)

# %% [markdown]
# We can also compare the speed of the uppermost water layer to the wind speed as we have `Uwind_eastward` and `Vwind_northward` given in the dataset.

# %%
wind_speed = np.sqrt(ds.Uwind_eastward[0:100, y_idx, x_idx]**2 + ds.Vwind_northward[0:100, y_idx, x_idx]**2)

# %%
fig, ax = plt.subplots()

line0 = current_speed.plot(ax=ax, color='red', label='Current speed')
ax.tick_params(axis='y', labelcolor='r')
ax.set_ylabel('[m/s]')

ax1 = ax.twinx()  # Sharing x-axis, but different y-axes
ax.set_xlabel('Time')

line1 = wind_speed.plot(ax=ax1, color='blue', label='Wind speed')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_ylabel('[m/s]')

lines = line0 + line1
labels = [l.get_label() for l in lines]
ax.legend(lines, labels)

