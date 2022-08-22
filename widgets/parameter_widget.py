import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

sys.path.append('../')
import utils

class Parameter_Widget(QWidget):
    def __init__(self,parent):
        super(Parameter_Widget, self).__init__(parent)
#         print("Done")
        self.p = parent # the pump interface, with all the functions
        self.init_param_UI()


#         self.param_layout.setMaximumHeight(190)
        
    def init_param_UI(self):
        
        self.param_layout = QGridLayout()
        
        self.param_layout.setSpacing(0)
#         self.param_layout.addStretch(1)
        
        row = 0
        
        self.plabel = QLabel("Parameters")
        self.param_layout.addWidget(self.plabel,0,0,2,0,alignment=Qt.AlignHCenter)
        self.plabel.setFont(QFont('Arial', 10))
        self.plabel.setFixedHeight(40)
        
        row += 2
        
        
    

#******************* Step Distance ********************#

# Label
        self.step_label = QLabel("Scanning step distance: ")# input
        self.param_layout.addWidget(self.step_label,row,0,alignment=Qt.AlignRight)
# Input
        self.move_step_input = QLineEdit()
        self.move_step_input.setText(str(self.p.ssd))
# Connections
        self.move_step_input.returnPressed.connect(self.move_step_changed)
        self.move_step_input.textChanged.connect(self.move_step_changed_unsaved)
# Layout        
        self.param_layout.addWidget(self.move_step_input,row,1,alignment=Qt.AlignHCenter)
        self.move_step_input.setFixedWidth(100)
# Units
        self.move_step_units_label = QLabel(" mm")
        self.param_layout.addWidget(self.move_step_units_label,row,2,alignment=Qt.AlignLeft)
        
#******************* Scan Distance ********************#

        row += 1
        
# Label
        self.scan_label = QLabel("Scan distance: ")
        self.param_layout.addWidget(self.scan_label,row,0,alignment=Qt.AlignRight)
# Input
        self.scan_input = QLineEdit()
        self.scan_input.setText(str(self.p.scan_distance))
# Connections
        self.scan_input.textChanged.connect(self.scan_changed_unsaved)
        self.scan_input.returnPressed.connect(self.scan_changed)
# Layout
        self.scan_input.setFixedWidth(100)
        self.param_layout.addWidget(self.scan_input,row,1,alignment=Qt.AlignHCenter)
# Units
        self.scan_units_label = QLabel(" mm")
        self.param_layout.addWidget(self.scan_units_label,row,2,alignment=Qt.AlignLeft)
        
#******************* Wait Time ********************#
        row += 1
    
# label
        self.wait_label = QLabel("Wait time: ")
        self.param_layout.addWidget(self.wait_label,row,0, alignment=Qt.AlignRight)
# input
        self.wait_input = QLineEdit()
        self.wait_input.setText(str(self.p.wait_time))
# Connections
        self.wait_input.returnPressed.connect(self.wait_changed)
        self.wait_input.textChanged.connect(self.wait_changed_unsaved)
# Layout
        self.wait_input.setFixedWidth(100)
        self.param_layout.addWidget(self.wait_input,row,1)
# Units
        self.wait_units_label = QLabel(" s")
        self.param_layout.addWidget(self.wait_units_label,row,2,alignment=Qt.AlignLeft)
        
#******************* Measure Time ********************#
        row += 1
    
# label
        self.measure_label = QLabel("Measure time: ")
        self.param_layout.addWidget(self.measure_label,row,0, alignment=Qt.AlignRight)
# input
        self.measure_input = QLineEdit()
        self.measure_input.setText(str(self.p.measure_time))
# Connections
        self.measure_input.returnPressed.connect(self.measure_changed)
        self.measure_input.textChanged.connect(self.measure_changed_unsaved)
# Layout
        self.measure_input.setFixedWidth(100)
        self.param_layout.addWidget(self.measure_input,row,1)
# Units
        self.measure_units_label = QLabel(" s")
        self.param_layout.addWidget(self.measure_units_label,row,2,alignment=Qt.AlignLeft)
        
#******************* Data Collection Rate ********************#
        row += 1
    
        self.data_rate_label = QLabel("Data collection rate: ")
        self.param_layout.addWidget(self.data_rate_label,row,0,alignment=Qt.AlignRight)

        # dropdown menu
        self.data_rate_input = QComboBox()
        self.data_rate_input.addItems(["0.5 Hz", "1 Hz", "2 Hz","3 Hz", "Max"])
        self.possible_data_periods = [2,1,0.5,1/3,0]
        self.param_layout.addWidget(self.data_rate_input,row,1,alignment=Qt.AlignLeft)
        self.data_rate_input.currentIndexChanged.connect(self.data_rate_changed)
        self.data_rate_input.setCurrentIndex(4) # default to max
    
############################################################################################################################################
######################## MOTOR FUNCTIONS ###################################################################################################
############################################################################################################################################
                                     
    def move_step_changed(self):
        self.p.ssd = utils.to_num(self.move_step_input.text()) # scan step distance
        # make sure input is valid
        if np.isnan(self.p.ssd) or self.p.ssd<0:
            self.invalid_alert(self.p.ssd, "Scanning step distance",self.p.ssd_DEFAULT)
            self.p.ssd = self.p.ssd_DEFAULT
        # regardless, set the new volume (0 if an error occurred)
        self.move_step_input.setText(str(self.p.ssd))
        self.step_label.setText("Scanning step distance: ")
        self.p.display_command("Scanning step distance set to " + str(self.p.ssd) + " mm")
        
    def scan_changed(self):
        self.p.scan_distance = utils.to_num(self.scan_input.text()) # scan step distance
        # make sure input is valid
        if np.isnan(self.p.scan_distance) or self.p.scan_distance<0:
            self.invalid_alert(self.p.scan_distance, "Scan distance",self.p.scan_distance_DEFAULT)
            self.p.scan_distance = self.p.scan_distance_DEFAULT
        # regardless, set the new volume (0 if an error occurred)
        self.scan_input.setText(str(self.p.scan_distance))
        self.scan_label.setText("Scan distance: ")
        self.p.display_command("Scan distance set to " + str(self.p.scan_distance) + " mm")
        
    def wait_changed(self):
        self.p.wait_time = utils.to_num(self.wait_input.text()) # scan step distance
        # make sure input is valid
        if np.isnan(self.p.wait_time) or self.p.wait_time<0:
            self.invalid_alert(self.p.wait_time, "Wait time",self.p.wait_time_DEFAULT)
            self.p.wait_time = self.p.wait_time_DEFAULT
        # regardless, set the new volume (0 if an error occurred)
        self.wait_input.setText(str(self.p.wait_time))
        self.wait_label.setText("Wait time: ")
        self.p.display_command("Wait time set to " + str(self.p.wait_time) + " s")
        
    def measure_changed(self):
        self.p.measure_time = utils.to_num(self.measure_input.text()) # scan step distance
        # make sure input is valid
        if np.isnan(self.p.measure_time) or self.p.measure_time<0:
            self.invalid_alert(self.p.measure_time, "Measure time",self.p.measure_time_DEFAULT)
            self.p.measure_time = self.p.measure_time_DEFAULT
        # regardless, set the new volume (0 if an error occurred)
        self.measure_input.setText(str(self.p.measure_time))
        self.measure_label.setText("Meaure time: ")
        self.p.display_command("Measure time set to " + str(self.p.measure_time) + " s")
        
    def move_step_changed_unsaved(self):
        self.step_label.setText("Scanning step distance:*")
        
    def scan_changed_unsaved(self):
        self.scan_label.setText("Scan distance:*")
        
    def wait_changed_unsaved(self):
        self.wait_label.setText("Wait time:*")
        
    def measure_changed_unsaved(self):
        self.measure_label.setText("Measure time:*")

    def zero(self):
        self.height_dial.setValue(0)
#         print(self.height_dial.value())

    def invalid_alert(self, var,label,default):
        alert = QMessageBox()
        if np.isnan(var):
            alert.setText("Error: "+label+" must be a number.\n"+label+" set to default ("+str(default)+").")
        elif var < 0:
            alert.setText("Error: "+label+" cannot be negative.\n"+label+" set to default ("+str(default)+").")
        alert.setWindowTitle("Invalid input")
        alert.exec()
        
    def data_rate_changed(self):
        self.p.data_period = self.possible_data_periods[self.data_rate_input.currentIndex()]
        self.p.display_command("Data collection rate set to " + self.data_rate_input.currentText()+ ".")

        