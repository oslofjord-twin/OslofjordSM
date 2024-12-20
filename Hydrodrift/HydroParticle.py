from opendrift.models.oceandrift import OceanDrift
from opendrift.elements import LagrangianArray
from datetime import datetime, timedelta
import numpy as np

class HydroParticle(LagrangianArray):
    '''
    Class defining Hydroparticles
    '''

    # Create custom variables for the current particle
    variables = LagrangianArray.add_variables([

        ('current_drift_factor', {'dtype': np.float32,
                                  'units': '',
                                  'default': 1.0}),## 100% effekt av strøm = 1.0

        ('wind_drift_factor', {'dtype': np.float32,      
                               'units': '',
                               'default': 0.02}),# 2% effekt av vind

        ('terminal_velocity', {'dtype': np.float32, 
                               'units': 'm/s',
                               'default': 0.0}), # Deafult = 0 vil si at partikelen ikke synker og heller ikke går opp
    ]) 
    


