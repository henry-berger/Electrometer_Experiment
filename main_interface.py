import threading
import numpy as np
import pandas as pd # data structures
import matplotlib.pyplot as plt

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import instruments
import widgets
from port_popup import Port_Popup
import utils


## The widget containing everything
class Pump_Interface(QWidget): 

#####################################################################################################################################
##********************** Initialize ***********************************************************************************************##
#####################################################################################################################################

    def __init__(self, parent):        
    # basic initialize
        super(Pump_Interface, self).__init__(parent) # initialize
        self.window = parent
    # Prompt the user for the names of the ports
        self.popup = Port_Popup(self)
        self.popup.exec()   
    # create the electrometer and translation stage objects
        self.e = instruments.Electrometer(self.electrometer_port)
        self.t = instruments.Translation_Stage(self.stage_port, parent=self)
    # full initialize
        self.init_vars()
        self.init_general_UI()
        
    def init_vars(self):
    # data
        self.data = pd.DataFrame({'t': [], 'V' : [], 'z' : [],'run' : []})
        self.saved = True
    # first time for things
        self.first_collection = True # whether a t0 has already been established
        self.first_graphing = True # if the graph has to be initialized
        self.last_event = 0 # essentially forever ago
        self.run_number = 1
    # running parameters
        self.scan_distance = 10
        self.wait_time = 1.5
        self.measure_time = 3
        self.ssd = 0.5
    # running parameter defaults
        self.scan_distance_DEFAULT = self.scan_distance
        self.wait_time_DEFAULT = self.wait_time
        self.measure_time_DEFAULT = self.measure_time
        self.ssd_DEFAULT = self.ssd
    
    # initialize the UI
    def init_general_UI(self): 
    # general layout
        self.layout = QGridLayout(self)
        self.layout.setRowStretch(1,3)
    # input layout (params and control)
        self.input_layout = QGridLayout(self)
        self.layout.addLayout(self.input_layout,0,0)      
    # parameter layout
        self.pw = widgets.Parameter_Widget(self)
        self.input_layout.addWidget(self.pw.param_widget,0,1) 
    # separator
        Separator = QFrame()
        Separator.setFrameShape(QFrame.VLine)
        Separator.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
        Separator.setLineWidth(1)
#         Separator.setFixedWidth(2)
        self.input_layout.addWidget(Separator,0,2)
    # buffers on the sides
        blank1 = QLabel("")
        blank1.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        blank2 = QLabel("")
        blank2.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.input_layout.addWidget(blank1,0,0)       
        self.input_layout.addWidget(blank2,0,4)       

        
    # control layout
        self.cw = widgets.Control_Widget(self)
        self.input_layout.addWidget(self.cw.control_widget,0,3)       
        
    # output layout
        self.ow = widgets.Output_Widget(self)
        self.layout.addWidget(self.ow.output_widget,1,0)
        

        


#************************** Setter functions for the popup ****************************************#
        
    # Functions that the popup window uses to change the stage and electrometer port names
    def set_stage_port(self, port):
        self.stage_port = port
        
    def set_electrometer_port(self, port):
        self.electrometer_port = port
        
    def set_save_file_name(self, name):
        self.save_file_name = name


#####################################################################################################################################
##********************** Run/Abort ************************************************************************************************##
#####################################################################################################################################

    def run(self):
        self.display_command("Run started")
        self.ow.progress.setValue(0)
        self.cw.run_btn.setText("Running...")
        self.cw.run_btn.setEnabled(False)
        self.cw.collect_btn.setEnabled(False)
        if len(self.data['run']>0):
            self.run_number = int(max(self.data['run']))+1
        else:
            self.run_number = 1
        # start the data collection loop
        self.run_loop = threading.Thread(target=self.run_looper)
        self.abort_now = False
        self.run_loop.start()
          
    def abort(self):
        self.cw.run_btn.setText("Run")
        self.cw.run_btn.setEnabled(True)
        self.cw.collect_btn.setEnabled(True)
        self.ow.progress.setValue(0)
        self.display_command("Run aborted")

        self.abort_now = True
        try:
            self.run_loop.join() 
        except:
            pass

    def run_looper(self):
        self.t.zero()
        self.ow.stage_pos_display.setText(str(self.t.get_position())+self.t.STEP_UNITS)
        self.collect(on=True)
        self.collect(on=False)

        self.last_event = 0
        target_position = self.ssd
        while self.t.get_position() < self.scan_distance + self.ssd*0.25 and not self.abort_now:
            while utils.gt()-self.last_event < self.wait_time:
                self.ow.time_display.setText(utils.timeFormat(utils.gt()-self.e.t0))
                if self.abort_now:
                    break
            self.last_event = utils.gt()
#             self.collect_btn.setChecked(True)
            self.collect(on=True)
            while utils.gt()-self.last_event < self.measure_time:
                if self.abort_now:
                    break
#             self.collect_btn.setChecked(False)
            self.collect(on=False)
            self.ow.progress.setValue(int(100*target_position/self.scan_distance))
            if (target_position < self.scan_distance + self.ssd*0.25):
                self.t.go_to(target_position)
                target_position += self.ssd
            else:
                self.abort_now = True
            self.last_event = utils.gt()
        self.cw.run_btn.setText("Run")
        self.cw.run_btn.setEnabled(True)
        self.cw.collect_btn.setEnabled(True)
        self.reset()
#         self.progress.setValue(0)

#####################################################################################################################################
##********************** Data Collection ******************************************************************************************##
#####################################################################################################################################

    def collect_data(self):
        self.tval,self.zval = self.e.time(), self.t.get_position() # get data
        self.yval = self.e.getval() # this has to be last because it takes a while, and otherwise the delay would mess up the z reading
        self.data = self.data.append([{'t':self.tval,'V':self.yval, 'z':self.zval, 'run':self.run_number}], ignore_index = True) # append data    
    
    def collect_button_signal(self):
        if self.cw.collect_btn.isChecked():
            self.collect(on=True)
        else:
            self.collect(on=False)
    # running this function starts or ends a data collection loop
    def collect(self,on=False):
        if on:
            self.display_command("Data collection turned on")

            self.cw.collect_btn.setText("Data Collection On")
#             self.window.setWindowTitle("Pump GUI (unsaved)") # for some reason, this causes the program to crash
            self.saved = False
            
            if self.first_collection: # if it's the first time collection has been on, set t0
                self.first_collection = False
                self.e.t0 = utils.gt()
                
            # start the data collection loop
            try:
                self.data_loop = threading.Thread(target=self.data_update)
                self.data_end_now = False
                self.data_loop.start()
            except:
                pass
            
        else: # i.e., if data collection has been turned off
            try:
                self.cw.collect_btn.setText("Data Collection Off")
                self.display_command("Data collection turned off")
            except:
                pass
            self.data_end_now = True
            try:
                self.data_loop.join() 
            except:
                pass
    # the data collection loop
#     def data_update(self):
#         last_update = utils.gt()-self.data_period # the -period is so that it starts immediately
#         while not self.data_end_now:
#             if utils.gt()-last_update > self.data_period:
#                 last_update = utils.gt()
#                 self.e.collect()
#                 self.saved = False
#                 # display the time and stuff
#                 self.pos_display.setText(str(sigfigs1(self.e.y,3))+" V")
#                 self.time_display.setText(utils.timeFormat(self.e.t))

    def data_update(self):
        last_update = utils.gt()-self.data_period # the -period is so that it starts immediately
        while not self.data_end_now:
            if utils.gt()-last_update > self.data_period:
                last_update = utils.gt()
                self.collect_data()
                if self.saved:
                    self.saved = False
#                     self.window.setWindowTitle("Pump GUI*")  # because there are unsaved data 
                # display the time and stuff
                self.ow.eread_display.setText(str(utils.sigfigs1(self.yval,3))+" V")
                self.ow.time_display.setText(utils.timeFormat(self.tval))

#####################################################################################################################################
##********************** Graphing *************************************************************************************************##
#####################################################################################################################################
                
    # running this function starts or ends a graphing loop 
    def graph(self):
        self.graph_period = self.measure_time+self.wait_time
        if self.cw.graph_btn.isChecked():
            self.cw.graph_btn.setText("Graphing On")
            self.display_command("Graphing turned on")

            if self.first_graphing:
                # initalize the graph
                self.first_graphing = False
                self.graph_widget = widgets.Image_Widget(self)
                self.ow.output_layout.addWidget(self.graph_widget,self.ow.row,0,4,0)
#                 self.graph_widget.setScaledContents(True)
                plt.ioff()
#                 plt.figure(figsize=(10,10))
#                 try:
#                     self.ow.output_layout.removeWidget(self.ow.blank)
#                     self.ow.blank.deleteLater()
#                     self.ow.blank = None
#                 except:
#                     pass


            self.graph_loop = threading.Thread(target=self.graph_update) # A loop for data collection
            self.graph_end_now = False
            self.graph_loop.start()
        else: 
            self.cw.graph_btn.setText("Graphing Off")
            self.display_command("Graphing turned off")

#             self.label.setText(str(round(-1*getval(),3)))
            self.graph_end_now = True
            self.graph_loop.join() 

    def graph_update(self):
        last_update = 0
        while not self.graph_end_now:
            if self.last_event-last_update > self.measure_time:
                last_update = utils.gt()
                print("Graphed")
# #                 plt.ioff() # in interactive mode, the graph doesn't display until you x out
                plt.clf() # clear previous graphs
                self.plot_graph()
        #                 # is there a more elegant way of doing this?
                plt.savefig('saved_figure.png')
                self.pixmap = QPixmap('saved_figure.png')
                self.graph_widget.setMyPixmap(self.pixmap)
                self.graph_widget.myresize()
#                 print("Graphed")
                
    # draws and formats the graph
    def plot_graph(self):
        for i in range(int(min(self.data['run'])),int(max(self.data['run']))+1):
            single_run = self.data.loc[self.data['run'] == i ]
            plt.plot(single_run['z'],single_run['V'],".",label="Run "+str(i))
        plt.xlabel("z (mm)")
        plt.ylabel("Y Value")
        plt.title("Y vs. z")
        plt.legend()

#     def paintEvent(self, e):
#         if not first_graphing:
#             w = self.graph_widget.width()
#             self.graph_widget.resize(w, int(1.5*w * (self.pixmap.height() / self.pixmap.width())))   

#####################################################################################################################################
##********************** Saving ***************************************************************************************************##
#####################################################################################################################################

    def save(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Excel files (*.xlsx)")
#         filenames = QStringList()
        
        if dlg.exec():
            filename = dlg.selectedFiles()[0] # the filename the user selects
            self.save_file_name = utils.excelFormat(filename)
#             print(filename)
#             self.data.to_excel(self.save_file_name) # adds .xlsx if necessary
            self.compile_and_save()
            print("Saved as", self.save_file_name)
            # make a note that it's been saved
#             self.window.setWindowTitle("Pump GUI")
            self.saved = True
            self.display_command("Saved as "+str(self.save_file_name))

#******************* Auto-saving ********************#
            
    # running this function starts or ends a graphing loop 
    def auto_save(self):
        if self.cw.auto_save_btn.isChecked():
            self.cw.save_btn.setEnabled(False)
            self.auto_save_loop = threading.Thread(target=self.auto_saver) # A loop for data collection
            self.auto_save_on = True
            self.auto_save_loop.start()
        else: 
            self.cw.save_btn.setEnabled(True)
#             self.label.setText(str(round(-1*getval(),3)))
            self.auto_save_on = False
            self.auto_save_loop.join() 

    def auto_saver(self):
        last_update = 0
        while self.auto_save_on:
            if self.last_event-last_update > self.measure_time and not self.saved:
                last_update = utils.gt()
#                 self
#                 self.data.to_excel(self.save_file_name) # adds .xlsx if necessary
                self.compile_and_save()
                self.display_command("Saved as "+str(self.save_file_name))
#                 self.window.setWindowTitle("Pump GUI")
                self.saved = True
    
    def compile_and_save(self):
        self.sum_data = self.summarize_data()
        Excelwriter = pd.ExcelWriter(self.save_file_name,engine="xlsxwriter")
        self.sum_data.to_excel(Excelwriter, sheet_name="Summary Data",index=False)
        self.data.to_excel(Excelwriter, sheet_name="All Data",index=False)
        Excelwriter.save()
        
    
    def summarize_data(self):
        # make a copy where the z-values are rounded, so there aren't two copies at 3.00037 and 3.00038
        data = self.data.copy()
        for z in data['z'].unique():
            data.loc[data['z']==z,'z']=np.round(z,3)
            
        sum_data = pd.DataFrame({'z' : data['z'].unique()})
        for run in data['run'].unique():
            for z in data['z'].unique():
                if len(data.loc[(data['z']==z) & (data['run']==run)]['V'])>0:
                    val = np.average(data.loc[(data['z']==z) & (data['run']==run)]['V'])
                else: val = np.nan
                sum_data.loc[sum_data['z']==z,'run '+str(int(run))]=val
        return sum_data
    
        
#####################################################################################################################################
##********************** Exiting **************************************************************************************************##
#####################################################################################################################################
        
    # triggered when the exit button is pressed
    def exit(self):
        if not self.saved:
            # ask the user if they want to save
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("You have unsaved data. Are you sure you would like to exit?")
            msg.setInformativeText("If you do, your data will be lost.")
            msg.setWindowTitle("Unsaved Data")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Save | QMessageBox.Cancel)
#             msg.buttonClicked.connect(self.msgbtn)

            ret = msg.exec()
#             print(ret)
            if ret == 1024: # Ok
                self.myclose()
            elif ret == 2048: # Save
                self.save()
            elif ret == 4194304: # Cancel
                pass
        else:
            self.myclose() # close everything
            
    # actually close
    def myclose(self):
        # end any loops that might be running
        try:
            self.data_end_now = True
            self.data_loop.join() 
        except: pass
        try:
            self.graph_end_now = True
            self.graph_loop.join() 
        except: pass
        try:
            self.auto_save_on = False
            self.auto_save_loop.join() 
        except: pass
        try:
            self.motor_stop_now = True
            self.move_loop.join() 
        except:
            pass
        try:
            self.abort_now = True
            self.run_loop.join() 
        except:
            pass
        try: 
            self.popup.rm.close()
        except:
            pass
        print(self.data)
        self.window.myclose()
        
        
#####################################################################################################################################
##********************** Miscellaneous ********************************************************************************************##
#####################################################################################################################################

    def move_stage_dist(self):
        self.t.move(dist=utils.to_num(self.cw.move_dist_input.text()))
        self.cw.move_dist_input.setText("")
        
    def move_stage_loc(self):
        self.t.go_to(position=utils.to_num(self.cw.move_loc_input.text()))
        self.cw.move_loc_input.setText("")
            
    def display_command(self, text, success=True):
        try:
            self.ow.most_recent_command.setText(text)
            self.ow.recent_command_time.setText("executed at " + utils.current_time())
        except:
            pass
#         if success:
#             self.most_recent_command.setText(text + " (success)")
#         else:
#             self.most_recent_command.setText(text + " (failure)")

    def reset(self):
        try:
            self.abort_now = True
            self.run_loop.join() 
        except:
            pass
        try:
            self.run_number = int(max(self.data['run']))+1
        except:
            self.run_number = 1
        print("Run number = ",self.run_number)
        self.ow.progress.setValue(0)
        self.t.zero()
        
    def set_current_to_0(self):
        self.t.tare()