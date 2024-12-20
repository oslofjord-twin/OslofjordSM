import numpy as np
from datetime import datetime, timedelta 

class VirtualLander():
    '''
    Variables:
    - Time
    - Location
    - Change 
    - Salinity
    - Temperature
    '''
    maxlat, minlat, maxlon, minlon, center_lat, center_lon, particle_center_lat, particle_center_lon = 0, 0, 0, 0, 0, 0, 0 ,0
    
    
    df_salinity = None
    df_temperature = None
    df_turbidity = None

    arr_salinity = []
    arr_temperature = []
    arr_turbidity = []


    arr_datetime = []
    arr_change = []

    change = False
    starttime = None
    id= 0
    seed_length = 0

    def __init__(self, id):
        self.id = id
       


    def create_lander(self, min_lat, max_lat, min_lon, max_lon, starttime, seed_length):
        '''
        Method to create a single lander
        Required variables:
            min_lat
            max_lat
            min_lon
            max_lon
            starttime
            seed_length
        '''

        self.starttime = starttime
        self.seed_length = seed_length

        self.maxlat = max_lat
        self.minlat = min_lat
        self.maxlon = max_lon
        self.minlon = min_lon

        self.calculate_center(max_lat, min_lat, max_lon, min_lon)

        self.arr_salinity = np.full(seed_length, self.df_salinity, dtype=np.float32)
        self.arr_temperature = np.full(seed_length, self.df_temperature, dtype=np.float32)
        self.arr_turbidity = np.full(seed_length, self.df_turbidity, dtype=np.float32)

        self.arr_change = np.full(seed_length, False)
        self.arr_datetime = np.full(seed_length, (starttime))

        for i in range(seed_length):
            self.arr_datetime[i] =  (starttime) + timedelta(hours=i)

        #print(f"Lander {self.id} is created")

    def update_lander(self, sim_salinity, sim_temperature, sim_turbidity, sim_time):
        '''
        Method to update the lander salinity, temperature and turbidity
        Required variables:
            salinity
            temperature
            turbidity
            current run time
        
        '''
        
        time_difference = (sim_time - self.starttime)
        
        duration = int(time_difference.total_seconds() / 3600)

        self.change = True
        
        if self.arr_change[duration] == False:
            self.arr_salinity[duration] = sim_salinity
            self.arr_temperature[duration] = sim_temperature
            self.arr_turbidity[duration] = sim_turbidity
            self.arr_change[duration] = True
            #print(f"Lander {self.id} values updated.")

        else:
            curr__salinity = self.arr_salinity[duration]
            new_salinity = np.float32((curr__salinity + sim_salinity)/2)
            self.arr_salinity[duration] = new_salinity

            curr__temperature = self.arr_temperature[duration]
            new_temperature = np.float32((curr__temperature + sim_temperature)/2)
            self.arr_temperature[duration] = new_temperature

            curr__turbidity = self.arr_turbidity[duration]
            new_turbidity = np.float32((curr__turbidity + sim_turbidity)/2)
            self.arr_turbidity[duration] = new_turbidity
            #print(f"Lander {self.id} values updated.")

    ## Lag metode for å kunne finne midtpunktet for alle partiklene som er innom griden til gitt tid
    def calculate_particle_center_point(self, lat, lon):
        '''
        Method to find center point for the particles entering the lander area
        Required variables:
            lat
            lon
        '''
        if self.particle_center_lat == 0 and self.particle_center_lon == 0:
            self.particle_center_lat = lat
            self.particle_center_lon = lon
        
        else:
            self.particle_center_lat = np.float32((self.particle_center_lat + lat) / 2)
            self.particle_center_lat = np.float32((self.particle_center_lon + lon) / 2)

    def contains(self, lat, lon):
        '''
        Method to check if current particle is in the lander area
        Required variables:
            lat
            lon
        '''
        if not (self.minlat <= lat <= self.maxlat and self.minlon <= lon <= self.maxlon):
            return False
        else:
            return True
    
        
    def smoother(self):
        '''
        Smoothing method for the lander values.
        The Change-value will not be changed, but rather fill in the default values with smoothe values.       
        '''
        for i in range(self.seed_length):
            if self.arr_change[i] == True: #må endre or self.arr_change[i-1] == False
                continue
                #skip
            
            # Check if current value is unchanged AND if the previous value is changed, OR if the previous values have been smoothen
            elif self.arr_change[i] == False  and (self.arr_change[i-1] == True):
                    next_changed_index = i+1

                    # Check if there are any changed values after the current unchanged default values. 
                    # If it finds any changed values, the current value will be set as the average of the previous + the next changed value
                    while next_changed_index < self.seed_length:
                        if self.arr_change[next_changed_index] == True:
                            self.arr_salinity[i] = np.float32((self.arr_salinity[i-1] + self.arr_salinity[next_changed_index])/2)
                            self.arr_temperature[i] = np.float32((self.arr_temperature[i-1] + self.arr_temperature[next_changed_index])/2)
                            self.arr_turbidity[i] = np.float32((self.arr_turbidity[i-1] + self.arr_turbidity[next_changed_index])/2)
                            self.arr_change[i] = True
                            break
                        
                        next_changed_index= next_changed_index+1

                    # If the current value is stil set as default, current value will be set as previous value
                    #if self.arr_salinity[i] == self.df_salinity and self.arr_temperature[i] == self.df_temperature and self.arr_turbidity[i] == self.df_turbidity:
                    if self.arr_change[i] == False:    
                        self.arr_salinity[i] = np.float32(self.arr_salinity[i-1])
                        self.arr_temperature[i] = np.float32(self.arr_temperature[i-1])
                        self.arr_turbidity[i] = np.float32(self.arr_turbidity[i-1])
                        self.arr_change[i] = True

            # If there arent any previous values set the current value
            elif self.arr_change[i] == False:
                next_changed_index = i+1
                while next_changed_index < self.seed_length:
                        if self.arr_change[next_changed_index] == True:
                            self.arr_salinity[i] = np.float32(self.arr_salinity[next_changed_index])
                            self.arr_temperature[i] = np.float32(self.arr_temperature[next_changed_index])
                            self.arr_turbidity[i] = np.float32(self.arr_turbidity[next_changed_index])
                            break

                        next_changed_index= next_changed_index+1



    def calculate_center(self, max_lat, min_lat, max_lon, min_lon):
        '''
        Method to find centroid of grid
        Required variables:
            max_lat
            min_lat
            max_lon
            min_lon
        '''
        self.center_lat = (max_lat + min_lat) / 2
        self.center_lon = (max_lon + min_lon) / 2
        
        
    def print_lander(self):      
        print(f"Lander {self.id} has location {self.center_lat} {self.center_lon}")
        print(f"Datetime: {self.arr_datetime}")
        print(f"Salinity: {self.arr_salinity}")
        print(f"Temperature: {self.arr_temperature} ")
        print(f"Turbidity: {self.arr_turbidity}")
        print(f"Status of update {self.arr_change} ")
        print(f"Grid size lat: {self.maxlat} {self.minlat}, lon: {self.maxlon} {self.minlon}")
        print("--------------------------------")
        
