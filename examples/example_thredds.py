"""
Read variables from a model along the trajectories of drifters.
=============================================================================
"""

import xarray as xr
import cf_xarray as _
import pyproj
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

#%%
# Open the Norkyst800 model
nk = xr.open_dataset(
    'https://thredds.met.no/thredds/dodsC/sea/norkyst800m/1h/aggregate_be')
print(nk)

#%%
# Use cf-xarray to get the CRS
gm = nk.cf['grid_mapping']
nk_crs = pyproj.CRS.from_cf(gm.attrs)
print(nk_crs)

# Converting to Cartopy is not possible to do automatically, unfortunately, so we define it manually:
ncrs = ccrs.Stereographic(true_scale_latitude=60,
                          central_latitude=90,
                          central_longitude=70,
                          false_easting=3192800,
                          false_northing=1784000)
#%%
# Plot northward surface current
plt.axes(projection=ncrs)
# plt.axes(projection=ccrs.Mercator())
nk.isel(time=-1, depth=0).v_northward.plot.imshow(
    transform=ncrs)  # TODO: SUPPLY CORRECT TRANSFORM HERE!

plt.scatter(5.32,
            60.4,
            10,
            transform=ccrs.PlateCarree(),
            marker='*',
            label='Bergen')

plt.legend()
plt.show()
