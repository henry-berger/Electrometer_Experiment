import pyvisa
import numpy as np
import sys

sys.path.append('../')
import utils

# class for communicating with the translation stage
class Translation_Stage():
#************************ Setup **************************#
    def __init__(self, port_name="None", motor_number=1, parent=None):
        self.p = parent
        self.position = 0 
            # the initial position should be zero,
            # because the stage should be adjusted manually beforehand
        
        # Constants:
        self.STEPS_PER_REV = 400
        self.DIST_PER_REV = 0.635
        self.STEP_DIST = self.DIST_PER_REV / self.STEPS_PER_REV
        self.STEP_UNITS = " mm"
        
        # connect
        self.connect_to_motor(port_name)
        self.mn = str(motor_number)
        
    # connect to the motor, if it exists
    def connect_to_motor(self, port_name):
        if port_name == "None":
            self.real_stage = False
        else:
            rm = pyvisa.ResourceManager()
            self.inst = rm.open_resource(port_name)
            self.real_stage = True
        
#************************ Moving **************************#

    # Input: a list of commands
    # output: a single string with those commands, separated by commas
    def message(self, *commands):
        m = ""
        for command in commands:
            m = m + str(command) + ","
        return m[:-1] # the -1 to get rid of the the last comma
        
    def move(self, speed=1, revs=np.nan, dist = np.nan, steps=np.nan):
        if not np.isnan(dist):
            steps = int(np.round(dist / self.STEP_DIST,0))
                # it needs to be an int, but int() doesn't round properly, hence the np.round
        elif not np.isnan(revs):
            steps = int(np.round(revs * 400))
                # it needs to be an int, but int() doesn't round properly, hence the np.round
        elif np.isnan(steps):
            steps = 0
            
        self.position += self.STEP_DIST * steps 
        message = self.message("F", # VXM On-Line WITH Echo OFF 
                               "PM-0", # Change To AND Clear Program 0
                               "S"+self.mn+"M"+ # set speed to ...
                               str(int(speed*1000)),
                               "I"+self.mn+"M"+ # set go a distance to ...
                               str(steps),
                               "R" # Run
                              )
        if self.real_stage:
            self.inst.write(message) # send the command
        text = "Moved {s:n} steps to position {p:.04f} mm."
        report = (text.format(s=steps,p=self.get_position()))
        print(report)
        try:
            self.p.ow.stage_pos_display.setText(str(self.get_position())+self.STEP_UNITS)
            self.p.display_command(report)
            # this is only in a try/except so that when I create a test instance,
            # it doesn't throw an error because there's no parent
        except: pass
        return(message)
    
    # go to a certain position (IN MM)
    def go_to(self, position,speed=1):
        self.move(dist=position-self.position,speed=speed)


#************************ Other **************************#
    
    def zero(self):
        # move the motor to 0
        if self.get_position() != 0:
            self.go_to(-1)
            utils.mysleep(2) # give the motor time to move
            self.go_to(0)
        else:
            self.p.display_command("Already at 0.")
    
    def get_position(self):
# A guess at how to query the position:
#         if self.real_stage:
#             pos = self.inst.query("X")
#             print(pos)
#             return float(pos)
        return round(self.position,5) # Make an interpolation:
        
    
    def tare(self):
        # make 0 the current position
        self.position = 0
        try:
            self.p.ow.stage_pos_display.setText(str(self.get_position())+self.STEP_UNITS)
            self.p.display_command("Current position set to 0.")
        except:
            pass
        
