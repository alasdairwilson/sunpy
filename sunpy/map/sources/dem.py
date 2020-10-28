"""DEM Map subclass definitions"""


import astropy.units as u
from astropy.coordinates import CartesianRepresentation, HeliocentricMeanEcliptic
from astropy.visualization import AsinhStretch
from astropy.visualization.mpl_normalize import ImageNormalize

from sunpy.map import GenericMap
from sunpy.map.sources.source_type import source_stretch

__all__ = ['DEMMap']


class DEMMap(GenericMap):
    """DEM Image Map.git 

    DEMs are recovered from multiwavelength solar instrumental data which, in combination with these
    instruments temperature responses. The following reads in DEM maps consisting of pixel specific temperature
    information generally averaged over some t range. These are are currently produced by demregpy.


    Notes
    -----
    Observer location: The standard AIA FITS header provides the spacecraft location in multiple
    coordinate systems, including Heliocentric Aries Ecliptic (HAE) and Heliographic Stonyhurst
    (HGS).  SunPy uses the provided HAE coordinates due to accuracy concerns with the provided
    HGS coordinates, but other software packages may make different choices.
    """

    def __init__(self, data, header, **kwargs):
        super().__init__(data, header, **kwargs)

        # Fill in some missing info
        self.meta['detector'] = self.meta.get('detector', "DEM")
        self._nickname = self.detector
        self.plot_settings['cmap'] = 'inferno' # self._get_cmap_name()
        self.plot_settings['norm'] = ImageNormalize(vmin=0,vmax=255)
    @property
    def measurement(self):
        
        return self.meta['instrume']      
    @property
    def _supported_observer_coordinates(self):
        return [(('haex_obs', 'haey_obs', 'haez_obs'), {'x': self.meta.get('haex_obs'),
                                                        'y': self.meta.get('haey_obs'),
                                                        'z': self.meta.get('haez_obs'),
                                                        'unit': u.m,
                                                        'representation_type': CartesianRepresentation,
                                                        'frame': HeliocentricMeanEcliptic})
                ] + super()._supported_observer_coordinates

    @property
    def observatory(self):
        """
        Returns the observatory.
        """
        return self.meta.get('telescop', '').split('/')[0]

    @classmethod
    def is_datasource_for(cls, data, header, **kwargs):
        """
        returns if map is consistent with a DEM
        """
        return str(header.get('detector', '')).startswith('dem')


