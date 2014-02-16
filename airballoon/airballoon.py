import numpy as np
from scipy import integrate, interpolate

R_e = 6371000.0 # Radius of the Earth in meters

# Interpolation data: 
# Use the CIRA-2012 model atmosphere to find the density of the
# at elevations from 0 (sea level) to 100km. 
#     Source: http://spaceweather.usu.edu/files/uploads/PDF/
#             COSPAR_INTERNATIONAL_REFERENCE_ATMOSPHERE-CHAPTER-1_3
#             (rev-01-11-08-2012).pdf
cira_elevations = np.array([0, 20, 40, 60, 80, 100])*1000.0 # meters
cira_densities = np.array([1.16e0, 9.37e-2, 4.02e-3, 3.26e-4, 1.83e-5, \
                           5.73e-7]) # kg m^-3
f_logrho = interpolate.interp1d(cira_elevations, np.log(cira_densities), \
                             kind='linear')

def rho(elevation):
    '''
    Interpolate for the density of the atmosphere as a function of elevation
    above sea level `x` in meters.
    
    Parameters
    ----------
    elevation : float
        The height of the observer above sea-level in meters    
    
    Returns
    -------
    rho : float
        The density of the atmosphere :math:`\\rho` at height `elevation`    
        in kg m^-3
        
    Notes
    -----
    Uses the CIRA-2012 atmosphere model. In order to preserve
    a roughly exponential decline in the density with elevation, the 
    interpolation function will interpolate linearly from the log of the 
    denities, which should be roughly linear with elevation, and then return 
    the exponential of the result.
    '''
    return np.exp(f_logrho(elevation))

def columndensity_integrand(y, z, y_obs):
    '''
    The column density :math:`\\sigma` is defined as 
    :math:`\\sigma(s) = \\int \\rho(s) ds` along a path :math:`s` through the
    atmosphere. After change of variables from :math:`s \\rightarrow y`, 
    
    .. math::
    
        \\sigma(y_{obs}, z) = \\int^{y_{atm}}_{y_{obs}}  \\frac{\\rho(y)~\\left(R_e + y\\right)~dy}{\\sqrt{ (R_e + y_{obs})^2 \\cos^2 z - y_{obs}^2 + y^2 - 2R_e(y_{obs} - y) }}    
    
    where :math:`y_{obs}` is the elevation of the observer above sea level in 
    meters,  :math:`y_{atm}` is the upper edge of the atmosphere (Karman Line),  
    `y` is some height on :math:`y_{obs} \le y \le y_{atm}`, 
    `z` is the zenith angle of the target,  and :math:`R_e` is the radius of the
    Earth.
    
    This function returns the integrand in the above equation.
    
    Parameters
    ----------
    y : float
        The height above sea level in meters  
    z : float
        The zenith angle of the target (after refraction correction) in degrees
    y_obs : float
        Elevation of the observer above sea level in meters
        
    Returns
    -------
    integrand : float
        The integrand of the equation for the column density as a function of
        observer elevation and zenith angle.

    Notes
    -----
    Variable density atmosphere: 
    http://en.wikipedia.org/wiki/Air_mass_%28astronomy%29#Variable-density_atmosphere
    '''

    return rho(y)*(R_e + y)/np.sqrt((R_e+y_obs)**2 * np.cos(z*np.pi/180.0)**2 - 2.0*R_e*(y_obs - y) + y**2 - y_obs**2) ## NOT assuming sea-level observer

def airmass(altitude, elevation):
    '''    
    Here we define airmass `X` for an observer at elevation `elevation` 
    (in meters), observing a target `altitude` degrees above the horizon,  

    .. math::
        
        X = \\frac{\\sigma(y_{obs}=elevation, ~~z=90-altitude)}{\\sigma(y_{obs}=0, z=0)}
    
    Parameters
    ----------
    altitude : float
        The altitude :math:`\\alpha` (in degrees) of a target above the horizon. 
        :math:`0 \le \\alpha \le 90` Will convert into zenith angle 
        :math:`z = 90.0 - \\alpha`.
    elevation : float    
        Height of the observer above sea level in meters
        
    Returns
    -------
    relative_airmass : float
        The relative airmass is the column density to the
        target at zenith angle :math:`z = 90 - \\alpha` from elevation `elevation`
        normalized by the column density to the zenith at :math:`z = 0` 
        from :math:`elevation=0` (sea level). Results should be accurate to 
        roughly 0.1%.
    '''
    
    # Check for good input arguments
    if type(altitude) is list:
        raise TypeError('Altitude and elevation must be floats or integers.')      
    elif altitude < 0.0 or elevation < 0.0:
        raise ValueError('Altitude and elevation must be greater than or '+\
                         'equal to zero.')
    elif elevation >= 100000.0:
        raise ValueError('Elevation must be less than 100km.')
    
    z = 90.0 - altitude # zenith angle
    y_atm = 100000.0     # Upper limit on atmosphere
    absolute_airmass = integrate.quad(columndensity_integrand, elevation, y_atm, \
                                      args=(z, elevation), epsabs=0, epsrel=1e-3)[0]
    # Airmass at the zenith from zero elevation 
    airmass_zenith =  integrate.quad(columndensity_integrand, 0.0, y_atm, \
                                     args=(0.0, 0.0), epsabs=0, epsrel=1e-3)[0]

    relative_airmass = absolute_airmass/airmass_zenith
    return relative_airmass