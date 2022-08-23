from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# the widget with all the buttons:
"""
      R  U  N
 COLLECT   ABORT
  RESET    GRAPH
Auto-SAVE  EXIT
"""
class Control_Widget(QWidget):
    def __init__(self,parent):
        super(Control_Widget, self).__init__(parent)
#         print("Made")
        self.p = parent # the pump interface, with all the functions
        self.BUTTON_WIDTH = 180
        self.init_UI()
        
    def init_UI(self):
        
        self.control_widget = QWidget()
        self.control_layout = QGridLayout(self.control_widget)
        
       
        row = 0 # the row
    
#         Separator = QFrame()
#         Separator.setFrameShape(QFrame.HLine)
#         Separator.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
#         Separator.setLineWidth(1)
#         Separator.setFixedHeight(2)
#         self.control_layout.addWidget(Separator,row,0,1,0)
        
#         row += 1
        
        self.elabel = QLabel("Control")
        self.control_layout.addWidget(self.elabel,row,0,1,0,alignment=Qt.AlignHCenter)
        self.elabel.setFont(QFont('Arial', 10))
        self.elabel.setMaximumHeight(36)
        
        row += 1

        # Run button
        self.run_btn = QPushButton("Run")
        self.control_layout.addWidget(self.run_btn,row,0,alignment=Qt.AlignRight)
        self.run_btn.setCheckable(False) # button can stay down
        self.run_btn.clicked.connect(self.p.run)
        self.run_btn.setStyleSheet("background-color: magenta;")
        self.run_btn.setFixedWidth(int(self.BUTTON_WIDTH))
        
        # Graph button
        self.abort_btn = QPushButton("Abort Run")
        self.control_layout.addWidget(self.abort_btn,row,1,alignment=Qt.AlignLeft)
        self.abort_btn.setCheckable(False) # button can stay down
        self.abort_btn.clicked.connect(self.p.abort)
        self.abort_btn.setStyleSheet("background-color: red;")
        self.abort_btn.setFixedWidth(self.BUTTON_WIDTH)
    
        row += 1
            
        # Run button
        self.collect_btn = QPushButton("Data Collection")
        self.control_layout.addWidget(self.collect_btn,row,0,alignment=Qt.AlignRight)
        self.collect_btn.setCheckable(True) # button can stay down
        self.collect_btn.clicked.connect(self.p.collect_button_signal)
        self.collect_btn.setStyleSheet("background-color: lightgreen;")
        self.collect_btn.setFixedWidth(self.BUTTON_WIDTH)


        # Graph button
        self.graph_btn = QPushButton("Graph")
        self.control_layout.addWidget(self.graph_btn,row,1,alignment=Qt.AlignLeft)
        self.graph_btn.setCheckable(True) # button can stay down
        self.graph_btn.clicked.connect(self.p.graph)
        self.graph_btn.setStyleSheet("background-color: lightblue;")
        self.graph_btn.setFixedWidth(self.BUTTON_WIDTH)
        
        row += 1
        
        # Run button
        self.reset_btn = QPushButton("Prep for New Run")
        self.control_layout.addWidget(self.reset_btn,row,0,alignment=Qt.AlignRight)
        self.reset_btn.setCheckable(False) # button can stay down
        self.reset_btn.clicked.connect(self.p.reset)
        self.reset_btn.setStyleSheet("background-color: white;")
        self.reset_btn.setFixedWidth(self.BUTTON_WIDTH)
        
        # Zero button
        self.zero_btn = QPushButton("Current Pos = 0")
        self.control_layout.addWidget(self.zero_btn,row,1,alignment=Qt.AlignLeft)
        self.zero_btn.setCheckable(False) # button can stay down
        self.zero_btn.clicked.connect(self.p.set_current_to_0)
        self.zero_btn.setStyleSheet("background-color: white;")
        self.zero_btn.setFixedWidth(self.BUTTON_WIDTH)

        row += 1

        # Exit button
        self.exit_btn = QPushButton("Exit")
        self.control_layout.addWidget(self.exit_btn,row,1,alignment=Qt.AlignLeft)
        self.exit_btn.setCheckable(False)  # button can't stay down
        self.exit_btn.clicked.connect(self.p.exit)     
        self.exit_btn.setStyleSheet("background-color: red;")
        self.exit_btn.setFixedWidth(self.BUTTON_WIDTH)
        
#************************ Save Buttons **************************#
        
        # Save buttons
        self.save_layout = QHBoxLayout()
        # Auto-save Checkbox
        self.auto_save_btn = QPushButton("Auto \u2014")
        self.auto_save_btn.setFixedWidth(int(self.BUTTON_WIDTH/2))  
        self.auto_save_btn.setCheckable(True)   # button can't stay down
        self.auto_save_btn.clicked.connect(self.p.auto_save)
        self.auto_save_btn.setStyleSheet("background-color: lightgray;")
#         self.auto_save_btn.setLayoutDirection(Qt.RightToLeft)
        self.save_layout.addWidget(self.auto_save_btn)
        
        # save button
        self.save_btn = QPushButton("Save")
        self.save_layout.addWidget(self.save_btn)
        self.save_btn.setCheckable(False)   # button can't stay down
        self.save_btn.clicked.connect(self.p.save)
        self.save_btn.setStyleSheet("background-color: lightgray;")
        self.save_btn.setFixedWidth(int(self.BUTTON_WIDTH/2))    
        
        self.save_layout.setSpacing(0)
        self.control_layout.addLayout(self.save_layout,row,0,alignment=Qt.AlignRight)
        
#####################################################################################################################################
##********************** Manual Motor Control *************************************************************************************##
#####################################################################################################################################
        
        row += 1
        
    # Separator
        Separator2 = QFrame()
        Separator2.setFrameShape(QFrame.HLine)
        Separator2.setLineWidth(1)
        Separator2.setFixedHeight(2)
        Separator2.setFixedWidth(int(self.BUTTON_WIDTH*2.1))
        self.control_layout.addWidget(Separator2,row,0,1,0,alignment=Qt.AlignHCenter)
        
        row += 1
        
        self.mlabel = QLabel("Manual Motor Control")
        self.control_layout.addWidget(self.mlabel,row,0,1,0,alignment=Qt.AlignHCenter)
#         self.mlabel.setFont(QFont('Arial', 10))
#         self.mlabel.setMaximumHeight(36)
            
        row += 1
        
        self.motor_control_layout = QGridLayout()
        self.control_layout.addLayout(self.motor_control_layout,row,0,1,0,alignment=Qt.AlignHCenter)
        self.motor_control_layout.setSpacing(0)

            
        #******************* Move By Distance ********************#

# Label
        self.move_dist_label = QLabel("Move by distance: ")# input
        self.motor_control_layout.addWidget(self.move_dist_label,row,0,alignment=Qt.AlignRight)
# Input
        self.move_dist_input = QLineEdit()
#         self.move_dist_input.setText(str(self.p.ssd))
# Connections
        self.move_dist_input.returnPressed.connect(self.p.move_stage_dist)
#         self.move_step_input.textChanged.connect(self.move_step_changed_unsaved)
# Layout        
        self.motor_control_layout.addWidget(self.move_dist_input,row,1,alignment=Qt.AlignHCenter)
        self.move_dist_input.setFixedWidth(100)
# Units
        self.move_dist_units_label = QLabel(" mm")
        self.motor_control_layout.addWidget(self.move_dist_units_label,row,2,alignment=Qt.AlignLeft)
        
        row += 1
        
        #******************* Move to Location ********************#

# Label
        self.move_loc_label = QLabel("Move to location: ")# input
        self.motor_control_layout.addWidget(self.move_loc_label,row,0,alignment=Qt.AlignRight)
# Input
        self.move_loc_input = QLineEdit()
#         self.move_loc_input.setText(str(self.p.ssd))
# Connections
        self.move_loc_input.returnPressed.connect(self.p.move_stage_loc)
#         self.move_step_input.textChanged.connect(self.move_step_changed_unsaved)
# Layout        
        self.motor_control_layout.addWidget(self.move_loc_input,row,1,alignment=Qt.AlignHCenter)
        self.move_loc_input.setFixedWidth(100)
# Units
        self.move_loc_units_label = QLabel(" mm")
        self.motor_control_layout.addWidget(self.move_loc_units_label,row,2,alignment=Qt.AlignLeft)
        
        self.control_widget.setMaximumHeight(640)
        self.control_widget.setMaximumWidth(480)
        
#         self.control_widget.setMaximumHeight(self.control_widget.height())
#         self.control_widget.setMaximumWidth(self.control_widget.width())