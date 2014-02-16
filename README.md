airballoon
==========

Calculate astronomical airmass for sub-orbital observatories

Airballoon is a small Python tool for calculating astronomical airmass for sub-orbital observatories up to 100km above sea level. 

### Installation
To install, [download](https://github.com/bmorris3/airballoon/archive/master.zip) the package, unzip the archive, change directories into it, and type

`python setup.py install`

and you're ready to go. For example, calculate the airmass for at target 10 degrees above the horizon for an observatory 10km above sea level:

```python
import airballoon
print airballoon.airmass(10,10000)
>>> 1.52079630009
```

###### Contact
Developed by Brett M. Morris (University of Washington)