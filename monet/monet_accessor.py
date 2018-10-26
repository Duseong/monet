"MONET Accessor"

from __future__ import absolute_import, division, print_function
from builtins import object
import pandas as pd
import xarray as xr


def rename_latlon(ds):
    if 'latitude' in ds.coords:
        return ds.rename({'latitude': 'lat', 'longitude': 'lon'})
    elif 'lat' in ds.coords:
        return ds.rename({'lat': 'latitude', 'lon': 'longitude'})


@xr.register_dataarray_accessor('monet')
class MONETAccessor(object):
    """Short summary.

    Parameters
    ----------
    xray_obj : type
        Description of parameter `xray_obj`.

    Attributes
    ----------
    obj : type
        Description of attribute `obj`.

    """

    def __init__(self, xray_obj):
        self.obj = xray_obj

    def stratify(self, levels, vertical, axis=1):
        """Short summary.

        Parameters
        ----------
        levels : type
            Description of parameter `levels`.
        vertical : type
            Description of parameter `vertical`.
        axis : type
            Description of parameter `axis`.

        Returns
        -------
        type
            Description of returned object.

        """
        from .util.resample import resample_stratify
        out = resample_stratify(self.obj, levels, vertical, axis=1)
        return out

    def window(self, lat_min, lon_min, lat_max, lon_max):
        obj2 = self.obj.copy()
        obj2.coords['x'] = obj2.x.to_index()
        obj2.coords['y'] = obj2.y.to_index()
        con = (obj2.longitude >= lon_min) & (obj2.longitude <= lon_max) & (
            obj2.latitude <= lat_max) & (obj2.latitude >= lat_min)
        index = obj2.where(con, drop=True)
        x, y = index.coords['x'], index.coords['y']
        return self.obj.sel(x=x, y=y)

    def interp_constant_lat(self, lat=None, **kwargs):
        """Interpolates the data array to constant longitude.

            Parameters
            ----------
            lon : float
                Latitude on which to interpolate to

            Returns
            -------
            DataArray
                DataArray of at constant longitude

            """
        from .util.interp_util import constant_1d_xesmf
        from .util.resample import resample_xesmf
        from numpy import linspace, ones, asarray
        try:
            if lat is None:
                raise RuntimeError
        except RuntimeError:
            print('Must enter lat value')
        longitude = linspace(self.obj.longitude.min(),
                             self.obj.longitude.max(), len(self.obj.y))
        latitude = ones(longitude.shape) * asarray(lat)
        self.obj = rename_latlon(self.obj)

        output = constant_1d_xesmf(latitude=latitude, longitude=longitude)
        out = resample_xesmf(self.obj, output, **kwargs)
        return rename_latlon(out)

    def interp_constant_lon(self, lon=None, **kwargs):
        """Interpolates the data array to constant longitude.

            Parameters
            ----------
            lon : float
                Latitude on which to interpolate to

            Returns
            -------
            DataArray
                DataArray of at constant longitude

            """
        from .util.interp_util import constant_1d_xesmf
        from .util.resample import resample_xesmf
        from numpy import linspace, ones
        try:
            if lon is None:
                raise RuntimeError
        except RuntimeError:
            print('Must enter lon value')
        latitude = linspace(self.obj.latitude.min(), self.obj.latitude.max(),
                            len(self.obj.y))
        longitude = ones(latitude.shape) * lon
        self.obj = rename_latlon(self.obj)

        output = constant_1d_xesmf(latitude=latitude, longitude=longitude)

        out = resample_xesmf(self.obj, output, **kwargs)
        return rename_latlon(out)

    def nearest_latlon(self, lat=None, lon=None, cleanup=True, **kwargs):
        """Uses xesmf to intepolate to a given latitude and longitude.  Note
        that the conservative method is not available.

        Parameters
        ----------
        lat : type
            Description of parameter `lat`.
        lon : type
            Description of parameter `lon`.
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        from .util.interp_util import lonlat_to_xesmf
        from .util.resample import resample_xesmf
        try:
            if lat is None or lon is None:
                raise RuntimeError
        except RuntimeError:
            print('Must provide latitude and longitude')
        kwargs = self._check_kwargs_and_set_defaults(**kwargs)
        self.obj = rename_latlon(self.obj)
        target = lonlat_to_xesmf(longitude=lon, latitude=lat)
        output = resample_xesmf(self.obj, target, **kwargs)
        if cleanup:
            output = resample_xesmf(self.obj, target, cleanup=True, **kwargs)
        return rename_latlon(output.squeeze())

    @staticmethod
    def _check_kwargs_and_set_defaults(**kwargs):
        if 'reuse_weights' not in kwargs:
            kwargs['reuse_weights'] = False
        if 'method' not in kwargs:
            kwargs['method'] = 'bilinear'
        if 'periodic' not in kwargs:
            kwargs['periodic'] = False
        if 'filename' not in kwargs:
            kwargs['filename'] = 'monet_xesmf_regrid_file.nc'
        return kwargs

    def cartopy(self):
        """Short summary.

        Returns
        -------
        type
                Returns a cartopy.crs.Projection for this dataset

        """
        from .grids import get_optimal_cartopy_proj
        return get_optimal_cartopy_proj(self.lat, self.lon, self.proj4_srs)

    def quick_map(self, map_kwarg={}, **kwargs):
        """Short summary.

        Parameters
        ----------
        map_kwarg : type
            Description of parameter `map_kwarg`.
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        from .plots.mapgen import draw_map
        from matplotlib.pyplot import tight_layout
        import cartopy.crs as ccrs
        import seaborn as sns
        sns.set_context('talk', font_scale=.9)
        if 'crs' not in map_kwarg:
            map_kwarg['crs'] = ccrs.PlateCarree()
        ax = draw_map(**map_kwarg)
        self.obj.plot(
            x='longitude',
            y='latitude',
            ax=ax,
            transform=ccrs.PlateCarree(),
            **kwargs)
        ax.outline_patch.set_alpha(0)
        tight_layout()
        return ax

    # def _check_and_fix_coords(self):
    #     if not self.obj.coords:
    #         # get the lat lons from the swath or area def
    #         lon, lat = self.obj.area.get_lonlats()
    #         self.obj.coords['longitude'] = lon
    #         self.obj.coords['latitude'] = lat

    def _check_swath_def(self, defin):
        """checks if it is a pyresample SwathDefinition or AreaDefinition.

        Parameters
        ----------
        defin : type
            Description of parameter `defin`.

        Returns
        -------
        type
            Description of returned object.

        """
        from pyresample.geometry import SwathDefinition
        if isinstance(defin, SwathDefinition):
            return True
        else:
            return False

    def remap_data(self, dataarray, grid=None, **kwargs):
        """remaps from another grid to the current grid of self using pyresample.
        it assumes that the dimensions are ordered in ROW,COL,CHANNEL per
        pyresample docs

        Parameters
        ----------
        grid : pyresample grid (SwathDefinition or AreaDefinition)
            Description of parameter `grid`.
        da : ndarray or xarray DataArray
            Description of parameter `dset`.
        radius_of_influence : float or integer
            radius of influcence for pyresample in meters.

        Returns
        -------
        xarray.DataArray
            resampled object on current grid.

        """
        from .util import resample
        from .grids import get_generic_projection_from_proj4
        # check to see if grid is supplied
        target = get_generic_projection_from_proj4(
            self.obj.latitude, self.object.longitude, self.obj.proj4_srs)
        source_grid = get_generic_projection_from_proj4(
            dataarray.latitude, dataarray.longitude, dataarray.proj4_srs)
        if grid is None:  # grid is assumed to be in da.area
            out = resample.resample_dataset(dataarray, source_grid, target,
                                            **kwargs)
        else:
            out = resample.resample_dataset(dataarray, grid, target, **kwargs)
        return out

    def remap_xesmf(self, dataarray, method='bilinear', **kwargs):
        """remaps from another grid to the current grid of self using xesmf

        Parameters
        ----------
        daaarray : ndarray or xarray DataArray
            Description of parameter `dset`.
        radius_of_influence : float or integer
            radius of influcence for pyresample in meters.

        Returns
        -------
        xarray.DataArray
            resampled object on current grid.

        """
        from .util import resample
        # check to see if grid is supplied
        target = self.obj
        out = resample.resample_xesmf(
            dataarray, target, method=method, **kwargs)
        return out

    def combine_point(self, data, col=None, **kwargs):
        """Short summary.

        Parameters
        ----------
        data : type
            Description of parameter `data`.
        col : type
            Description of parameter `col`.
        radius : type
            Description of parameter `radius`.

        Returns
        -------
        type
            Description of returned object.

        """
        from .models.combinetool import combine_da_to_df_xesmf
        # point source data
        if isinstance(data, pd.DataFrame):
            try:
                if col is None:
                    raise RuntimeError
                return combine_da_to_df_xesmf(
                    self.obj, data, col=col, **kwargs)
            except RuntimeError:
                print('Must enter col ')
        elif isinstance(data, xr.Dataset) or isinstance(data, xr.DataArray):
            print('do spatial transform')
        else:
            print('d must be either a pd.DataFrame or xr.DataArray')


@xr.register_dataset_accessor('monet')
class MONETAccessorDataset(object):
    """Short summary.

    Parameters
    ----------
    xray_obj : type
        Description of parameter `xray_obj`.

    Attributes
    ----------
    obj : type
        Description of attribute `obj`.

    """

    def __init__(self, xray_obj):
        self.obj = xray_obj

    def remap_data(self, data, grid=None, **kwargs):
        """Short summary.

        Parameters
        ----------
        data : type
            Description of parameter `data`.
        grid : type
            Description of parameter `grid`.
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        try:
            if isinstance(data, xr.DataArray):
                self._remap_dataarray(data, grid=grid, **kwargs)
            elif isinstance(data, xr.Dataset):
                self._remap_dataset(data, grid=None, **kwargs)
            else:
                raise TypeError
        except TypeError:
            print('data must be an xarray.DataArray or xarray.Dataset')

    def remap_xesmf(self, data, **kwargs):
        """Short summary.

        Parameters
        ----------
        data : type
            Description of parameter `data`.
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        print(data)
        # try:
        if isinstance(data, xr.DataArray):
            self._remap_xesmf_dataarray(data, **kwargs)
        elif isinstance(data, xr.Dataset):
            self._remap_xesmf_dataset(data, **kwargs)
        else:
            raise TypeError
        # except TypeError:
        #     print('data must be an xarray.DataArray or xarray.Dataset')

    def _remap_xesmf_dataset(self,
                             dset,
                             filename='monet_xesmf_regrid_file.nc',
                             **kwargs):

        skip_keys = ['latitude', 'longitude', 'time', 'TFLAG']
        vars = pd.Series(dset.variables)
        loop_vars = vars.loc[~vars.isin(skip_keys)]
        dataarray = dset[loop_vars[0]]
        da = self._remap_xesmf_dataarray(
            dataarray, self.obj, filename=filename, **kwargs)
        if da.name in self.obj.variables:
            da.name = da.name + '_y'
        self.obj[da.name] = da
        for i in loop_vars[1:]:
            dataarray = dset[i]
            self._remap_xesmf_dataarray(
                dataarray, filename=filename, reuse_weights=True, **kwargs)

    def _remap_xesmf_dataarray(self,
                               dataarray,
                               method='bilinear',
                               filename='monet_xesmf_regrid_file.nc',
                               **kwargs):
        """Resample the DataArray to the dataset object.

        Parameters
        ----------
        dataarray : type
            Description of parameter `dataarray`.

        Returns
        -------
        type
            Description of returned object.

        """
        from .util import resample
        target = self.obj
        out = resample.resample_xesmf(
            dataarray, target, method=method, filename=filename, **kwargs)
        print(out)
        if out.name in self.obj.variables:
            out.name = out.name + '_y'
        self.obj[out.name] = out
        return out

    def _remap_dataset(self, dset, grid=None, **kwargs):
        """Resample the entire dset (xarray.Dataset) to the current dataset object.

        Parameters
        ----------
        dset : xarray.Dataset
            Description of parameter `dataarray`.

        Returns
        -------
        type
            Description of returned object.

        """
        # from .util import resample
        # target = self.obj.area
        skip_keys = ['latitude', 'longitude', 'time', 'TFLAG']
        vars = pd.Series(dset.variables)
        loop_vars = vars.loc[~vars.isin(skip_keys)]
        # get the first one in the loop and get the resample_cache data
        dataarray = dset[loop_vars[0]]

        da, resample_cache = self._remap_dataarray(
            dataarray, grid=grid, return_neighbor_info=True, **kwargs)
        if da.name in self.obj.variables:
            da.name = da.name + '_y'
        self.obj[da.name] = da
        for i in loop_vars[1:]:
            dataarray = dset[i]
            da, resample_cache = self._remap_dataarray(
                dataarray, grid=grid, resample_cache=resample_cache, **kwargs)
            if da.name in self.obj.variables:
                da.name = da.name + '_y'
            self.obj[da.name] = da

    def _remap_dataarray(self, dataarray, grid=None, **kwargs):
        """Resample the DataArray to the dataset object.

        Parameters
        ----------
        dataarray : type
            Description of parameter `dataarray`.

        Returns
        -------
        type
            Description of returned object.

        """
        from .util import resample
        if grid is None:  # grid is assumed to be in da.area
            out = resample.resample_dataset(dataarray.chunk(), self.obj,
                                            **kwargs)

        else:
            dataarray.attrs['area'] = grid
            out = resample.resample_dataset(dataarray.chunk(), self.obj,
                                            **kwargs)
        return out

    def nearest_latlon(self, lat=None, lon=None, **kwargs):
        """Short summary.

        Parameters
        ----------
        lat : type
            Description of parameter `lat`.
        lon : type
            Description of parameter `lon`.
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        vars = pd.Series(self.obj.variables)
        skip_keys = ['latitude', 'longitude', 'time', 'TFLAG']
        loop_vars = vars.loc[~vars.isin(skip_keys)]
        kwargs = self._check_kwargs_and_set_defaults(**kwargs)
        kwargs['reuse_weights'] = True
        orig = self.obj[loop_vars.iloc[0]].monet.nearest_latlon(
            lat=lat, lon=lon, cleanup=False, **kwargs)
        dset = orig.to_dataset()
        dset.attrs = self.obj.attrs.copy()
        for i in loop_vars[1:-1].values:
            dset[i] = self.obj[i].monet.nearest_latlon(
                lat=lat, lon=lon, cleanup=False, **kwargs)
        i = loop_vars.values[-1]
        dset[i] = self.obj[i].monet.nearest_latlon(
            lat=lat, lon=lon, cleanup=True, **kwargs)
        return dset

    @staticmethod
    def _check_kwargs_and_set_defaults(**kwargs):
        if 'reuse_weights' not in kwargs:
            kwargs['reuse_weights'] = False
        if 'method' not in kwargs:
            kwargs['method'] = 'bilinear'
        if 'periodic' not in kwargs:
            kwargs['periodic'] = False
        if 'filename' not in kwargs:
            kwargs['filename'] = 'monet_xesmf_regrid_file.nc'
        return kwargs

    def interp_constant_lat(self, lat=None, **kwargs):
        """Short summary.

        Parameters
        ----------
        lat : type
            Description of parameter `lat`.
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        vars = pd.Series(self.obj.variables)
        skip_keys = ['latitude', 'longitude', 'time', 'TFLAG']
        loop_vars = vars.loc[~vars.isin(skip_keys)]
        kwargs = self._check_kwargs_and_set_defaults(**kwargs)
        kwargs['reuse_weights'] = True
        orig = self.obj[loop_vars.iloc[0]].monet.interp_constant_lat(
            lat=lat, cleanup=False, **kwargs)

        dset = orig.to_dataset()
        dset.attrs = self.obj.attrs.copy()
        for i in loop_vars[1:-1].values:
            dset[i] = self.obj[i].monet.interp_constant_lat(lat=lat, **kwargs)
        i = loop_vars.values[-1]
        dset[i] = self.obj[i].monet.interp_constant_lat(
            lat=lat, cleanup=True, **kwargs)
        return dset

    def interp_constant_lon(self, lon=None, **kwargs):
        """Short summary.

        Parameters
        ----------
        lon : type
            Description of parameter `lon`.
        **kwargs : type
            Description of parameter `**kwargs`.

        Returns
        -------
        type
            Description of returned object.

        """
        vars = pd.Series(self.obj.variables)
        skip_keys = ['latitude', 'longitude', 'time', 'TFLAG']
        loop_vars = vars.loc[~vars.isin(skip_keys)]
        kwargs = self._check_kwargs_and_set_defaults(**kwargs)
        kwargs['reuse_weights'] = True
        orig = self.obj[loop_vars[0]].monet.interp_constant_lon(
            lon=lon, **kwargs)
        dset = orig.to_dataset()
        dset.attrs = self.obj.attrs.copy()
        for i in loop_vars[1:-1].values:
            dset[i] = self.obj[i].monet.interp_constant_lon(lon=lon, **kwargs)
        i = loop_vars.values[-1]
        dset[i] = self.obj[i].monet.interp_constant_lon(
            lon=lon, cleanup=True, **kwargs)
        return dset

    def stratify(self, levels, vertical, axis=1):
        """Short summary.

        Parameters
        ----------
        levels : type
            Description of parameter `levels`.
        vertical : type
            Description of parameter `vertical`.
        axis : type
            Description of parameter `axis`.

        Returns
        -------
        type
            Description of returned object.

        """
        loop_vars = [i for i in self.obj.variables if 'z' in self.obj[i].dims]
        orig = self.obj[loop_vars[0]].stratify(levels, vertical, axis=axis)
        dset = orig.to_dataset()
        dset.attrs = self.obj.attrs.copy()
        for i in loop_vars[1:]:
            dset[i] = self.obj[i].stratify(levels, vertical, axis=axis)
        return dset

    def window(self, lat_min, lon_min, lat_max, lon_max):
        obj2 = self.obj.longitude.copy()
        obj2.coords['x'] = obj2.x.to_index()
        obj2.coords['y'] = obj2.y.to_index()
        con = (obj2.longitude >= lon_min) & (obj2.longitude <= lon_max) & (
            obj2.latitude <= lat_max) & (obj2.latitude >= lat_min)
        index = obj2.where(con, drop=True)
        x, y = index.coords['x'], index.coords['y']
        return self.obj.sel(x=x, y=y)

    def combine_point(self, df, mapping_table=None, **kwargs):
        """Short summary.

        Parameters
        ----------
        df : type
            Description of parameter `df`.
        mapping_table : type
            Description of parameter `mapping_table`.
        radius : type
            Description of parameter `radius`.

        Returns
        -------
        type
            Description of returned object.

        """
        from .models.combinetool import combine_da_to_df_xesmf
        try:
            if ~isinstance(df, pd.DataFrame):
                raise TypeError
        except TypeError:
            print('df must be of type pd.DataFrame')
        for i in mapping_table:
            df = combine_da_to_df_xesmf(
                self.obj[mapping_table[i]], df, col=i, **kwargs)
        return df
