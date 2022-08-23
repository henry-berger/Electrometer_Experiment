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
        
        
        
        self.param_widget = QWidget()
        self.param_layout = QGridLayout(self.param_widget)  
        
#         self.param_layout.setSpacing(0)
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
#         self.move_step_input.returnPressed.connect(self.move_step_changed)
        self.move_step_input.returnPressed.connect(lambda: self.changed(0))
        self.move_step_input.textChanged.connect(lambda: self.changed_unsaved(0))
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
        self.scan_input.textChanged.connect(lambda: self.changed_unsaved(1))
        self.scan_input.returnPressed.connect(lambda: self.changed(1))
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
        self.wait_input.returnPressed.connect(lambda: self.changed(2))
        self.wait_input.textChanged.connect(lambda: self.changed_unsaved(2))
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
        self.measure_input.returnPressed.connect(lambda: self.changed(3))
        self.measure_input.textChanged.connect(lambda: self.changed_unsaved(3))
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
        
        row += 1
        blank = QLabel("")
        self.param_layout.addWidget(blank,row,0)
        blank.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        
        print(self.param_widget.height())
        print(self.param_widget.width())
        self.param_widget.setMaximumHeight(480)
        self.param_widget.setMaximumWidth(640)
#         self.param_widget.setMaximumHeight(self.param_widget.height())
#         self.param_widget.setMaximumWidth(self.param_widget.width())

    
############################################################################################################################################
######################## MOTOR FUNCTIONS ###################################################################################################
############################################################################################################################################
                                     
       
    def changed_unsaved(self, i):
        labels = [self.step_label,self.scan_label,
                  self.wait_label,self.measure_label]
        label_texts = ["Scanning step distance:*", "Scan distance:*",
                       "Wait time:*","Measure time:*"]
        labels[i].setText(label_texts[i])      
        
        
    def changed(self, i):
    #setup
        labels = [self.step_label,self.scan_label,
                  self.wait_label,self.measure_label]
        label_texts = ["Scanning step distance", "Scan distance",
                       "Wait time","Measure time"]
        inputs = [self.move_step_input,self.scan_input,
                 self.wait_input,self.measure_input]
        defaults = [self.p.ssd_DEFAULT, self.p.scan_distance_DEFAULT,
               self.p.wait_time_DEFAULT, self.p.measure_time_DEFAULT]
        vals = [self.p.ssd, self.p.scan_distance,
               self.p.wait_time, self.p.measure_time]
        units = [" mm", " mm", " s", " s"]
        
        vals[i]=utils.to_num(inputs[i].text())
        if np.isnan(vals[i]) or vals[i] < 0:
            self.invalid_alert(vals[i],label_texts[i],defaults[i],units[i])
            vals[i]=defaults[i]
        inputs[i].setText(str(vals[i]))
        labels[i].setText(label_texts[i]+": ")
        self.p.display_command(label_texts[i] + " set to " + str(vals[i])+units[i])
        [self.p.ssd, self.p.scan_distance,
        self.p.wait_time, self.p.measure_time] = vals

        print([self.p.ssd, self.p.scan_distance,
        self.p.wait_time, self.p.measure_time])
        

    def zero(self):
        self.height_dial.setValue(0)
#         print(self.height_dial.value())

    def invalid_alert(self, var,label,default,units):
        alert = QMessageBox()
        if np.isnan(var):
            alert.setText("Error: "+label+" must be a number.\n"+label+" set to default ("+str(default)+").")
        elif var < 0:
            alert.setText("Error: "+label+" cannot be negative.\n"+label+" set to default ("+str(default)+units+").")
        alert.setWindowTitle("Invalid input")
        alert.exec()
        
    def data_rate_changed(self):
        self.p.data_period = self.possible_data_periods[self.data_rate_input.currentIndex()]
        self.p.display_command("Data collection rate set to " + self.data_rate_input.currentText()+ ".")