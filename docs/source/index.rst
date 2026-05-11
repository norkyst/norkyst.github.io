Norkyst coastal ocean forecasting system
========================================

**Norkyst** is the national coastal ocean forecasting system for Norway, which is based on a specific configuration of the `Regional Ocean Modeling System <https://www.myroms.org/>`_. The forecasting system Norkyst is developed and maintained jointly by the `Institute of Marine Research <https://hi.no>`_ and the `Norwegian Meteorological Institute (MET Norway) <https://met.no>`_.

Norkyst version 3 is now fully operational, and a set of tools for extracting and analysing output data from the model will successively be introduced here. Full model configurations will also be made available. Our aim is to encourage basic and applied research based on model outputs, and also to encourage collaborative developments to improve the forecast system itself.

Contents
--------

.. toctree::
   :maxdepth: 2

   user_guide/index
   gallery/index


Model documentation
-------------------

The scientific basis and technical configuration of Norkyst v.3 are described in detail in the following peer-reviewed publication:

   Christensen, K. H., Albretsen, J., Asplin, L., Frøysa, H. G., Gusdal, Y., Iversen, S. C.,
   Jensen, M. F., Johnsen, I. A., Kristensen, N. M., Sævik, P. N., Sandvik, A. D., Simonsen, M.,
   Skarðhamar, J., Sperrevik, A. K., and Trodahl, M.:
   *"Norkyst" version 3: the coastal ocean forecasting system for Norway*,
   Geosci. Model Dev., 19, 2785–2798,
   https://doi.org/10.5194/gmd-19-2785-2026, 2026.

The paper covers the following key aspects of the system:

**Model domain and grid**
   Norkyst v.3 runs on a curvilinear rotated polar stereographic grid with approximately 800 m
   horizontal resolution (2747 × 1148 grid points) and 40 terrain-following vertical layers.
   The domain extends from the North Sea in the south to the Barents Sea in the north, and
   includes the full Norwegian coastline with its fjords and shelf break.

**Dynamical core**
   The system is based on the `Rutgers version of ROMS <https://github.com/myroms>`_
   (Regional Ocean Modeling System). It uses a split-explicit time stepping scheme with a
   40 s baroclinic and 2 s barotropic time step. Advection of momentum and temperature uses
   the default third-order upwind scheme, while salinity uses the HSIMT scheme. Vertical
   turbulence is handled by the Generic Length Scale (GLS) closure with the CANUTO_A
   stability functions.

**Forcing**
   Atmospheric forcing is provided by the AROME-MetCoOp numerical weather prediction system
   (2.5 km resolution, 1 h output) with gaps filled by ECMWF HRES data. River discharge for
   Norwegian rivers is based on daily measurements from the Norwegian Water Resources and
   Energy Directorate (NVE), distributed to 1760 river outlets. Lateral boundary conditions
   come from the Copernicus Marine Service Arctic (ARC MFC) and Baltic (BAL MFC) monitoring
   and forecasting centres, supplemented by tidal forcing from TPXO9.

**Model evaluation**
   Verification against the gridded CORA in-situ dataset (2015–2022) shows that the model
   closely reproduces observed temperature and salinity distributions in the upper 20 m.
   Temperature errors are generally within 1 °C across most depths and months. Validation
   against seven fixed coastal hydrographic stations (2012–2023) shows high correlations and
   realistic variability, particularly for surface-layer temperature. Fjord circulation in the
   Hardangerfjord is correctly represented for 75–90 % of the evaluation period depending on
   depth.

**Operational setup and data access**
   The system runs once per day and produces 120 h forecasts initialised at 00:00 UTC. Output
   is in netCDF format following CF conventions and FAIR principles. Forecast data are
   available at https://data.met.no/dataset/1250dfdf-975c-4c5e-85d4-745506402f06 and the
   hindcast archive (from 2012 onwards) at
   https://thredds.met.no/thredds/catalog/romshindcast/norkyst_v3/catalog.html.
   The ROMS configuration files are archived at https://doi.org/10.5281/zenodo.16810677.


Indices and tables
==================

* :ref:`genindex`
