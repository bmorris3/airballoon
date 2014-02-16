airballoon
==========

Calculate astronomical airmass for sub-orbital observatories

Airballoon is a small Python tool for calculating astronomical airmass for 
sub-orbital observatories up to 100km above sea level. 

### Installation
To install, [download](https://github.com/bmorris3/airballoon/archive/master.zip)
the package, unzip the archive, change directories into it, and type

`python setup.py install`

and you're ready to go. 

### Examples
Calculate the airmass for a target 10 degrees above the horizon for an 
observatory 10km above sea level:
```python
import airballoon
print airballoon.airmass(10,10000)
>>> 1.52079630009
```

Calculate the airmass for a target at the zenith for an observatory 
at various elevations (must be between 0-100km):
```python
import airballoon
elevations = [0, 20000, 40000, 60000, 80000, 99000] # in meters
airmasses = [airballoon.airmass(90,elevation) for elevation in elevations]
print airmasses
>>> [1.0, 0.066238788963745, 0.0034865871171798524, 0.0002466814138637848, 1.1276295753616965e-05, 6.892154501781153e-08]
```

Test limiting cases: 
```python
import airballoon
print airballoon.airmass(90.0,0.0) # Zenith
>>> 1.0
print airballoon.airmass(0.0,0.0) # Horizon
>>> 35.90116951092913


```

### How it works
To see a nice TeX-ed up explanation of how airballoon calculates airmass, 
check out the documentation in the `docs/` folder.

The primary function of the airballoon module is the 
```python
airballoon.airmass(altitude,elevation)
``` 
function. It returns the column density of the atmosphere along a line of sight,
defined by the `altitude` in degrees above the horizon, at a some `elevation` 
above sea level, normalized by the column density of the atmosphere for an 
observer at sea level looking in the direction of the zenith.

Airballoon estimates the density of the atmosphere as a function of elevation 
according to the
[CIRA-2012](http://spaceweather.usu.edu/files/uploads/PDF/COSPAR_INTERNATIONAL_REFERENCE_ATMOSPHERE-CHAPTER-1_3(rev-01-11-08-2012).pdf)
semi-empirical model. 

*Note*: The words elevation and altitude are often used interchangeably, and I
use them with distinct meanings in airballoon. When airballoon uses the word 
"elevation" it is referring to height of an observatory above sea level in 
meters. When it says "altitude" it is referring to the direction of the 
target of your observations, measured in degrees above the horizon.

### Contact
Developed by [Brett M. Morris](http://staff.washington.edu/bmmorris) 
(University of Washington).
