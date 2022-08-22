import time
import pyvisa
import sys

sys.path.append('../')
import utils

# class for communicating with the electrometer
class Electrometer():
#************************ Setup **************************#
    def __init__(self, port_name="None"):
        print(port_name)
        self.connect_to_electrometer(port_name)
        self.t0 = time.time() # just in case, but this should be reset when the data collection actually starts
        
    def connect_to_electrometer(self, port_name="None"):
        # if there's no electrometer, just track mouse position
        if port_name == "None":
            self.use_mouse_position = True
            
        # otherwise, connect to the electrometer
        else:
            rm = pyvisa.ResourceManager()
            self.inst = rm.open_resource(port_name)
            self.use_mouse_position = False

#********************** Reading **************************#        
    def time(self):
        return time.time()-self.t0
    
    def getval(self):
        if self.use_mouse_position:
            # if there's no electrometer, just track mouse position
            x,y = utils.queryMousePosition()
            return 1-y/912  #+ random.random()*0.1-0.05
        else:
            message = self.inst.query("*IDN?")
            # the first four characters aren't part of the actual number
            return float(message[4:])
    

# Old things:
"""
    # Since I'm also tracking the stage position, now self.time() and self.getval() are called directly from the Pump_Interface
    def collect(self):
        self.t,self.y = self.time(), self.getval() # get data
        self.data = self.data.append([{'t':self.t,'V':self.y}], ignore_index = True) # append data
        
    # these were in __init__ back when 
        self.data = pd.DataFrame({'t': [], 'V' : []})
        self.graph_rate = 1
        self.data_rate = 1
        self.end_next = False
        self.graphing = False
"""