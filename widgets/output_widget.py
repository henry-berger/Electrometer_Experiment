from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Output_Widget(QWidget):
    def __init__(self,parent):
        super(Output_Widget, self).__init__(parent)
#         print("Done")
        self.p = parent # the pump interface, with all the functions
        self.init_output_UI()
        
    def init_output_UI(self):
        self.output_widget = QWidget()
        self.output_layout = QGridLayout(self.output_widget)
        self.output_layout.setRowStretch(2,0)

        self.TEXT_HEIGHT = 28
        self.row = 0
        
        Separador = QFrame()
        Separador.setFrameShape(QFrame.HLine)
        Separador.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
        Separador.setLineWidth(1)
        Separador.setFixedHeight(2)
        self.output_layout.addWidget(Separador,self.row,0,1,0)
        
        self.row += 1
        
        self.olabel = QLabel("Output")
        self.output_layout.addWidget(self.olabel,self.row,0,1,0,alignment=Qt.AlignHCenter)
        self.olabel.setFont(QFont('Arial', 10))
        self.olabel.setFixedHeight(32)
    
    
# These labels will be changed as the variables change
        self.readings_layout = QGridLayout()
    
#************************ Time **************************#
        self.row += 1
    # label
        self.time_label = QLabel("Time:")
        self.readings_layout.addWidget(self.time_label,self.row,0,alignment=Qt.AlignRight)
    # reading
        self.time_display = QLabel("--")
        self.readings_layout.addWidget(self.time_display,self.row,1,alignment=Qt.AlignLeft)
        self.time_display.setFixedHeight(self.TEXT_HEIGHT)

#************** Electrometer Reading ********************#
        self.row += 1
    # label
        self.eread_label = QLabel("Current Value:")
        self.readings_layout.addWidget(self.eread_label,self.row,0,alignment=Qt.AlignRight)
    # reading
        self.eread_display = QLabel("--")
        self.readings_layout.addWidget(self.eread_display,self.row,1,alignment=Qt.AlignLeft)
        self.eread_display.setFixedHeight(self.TEXT_HEIGHT)

#******************* Stage Position ********************#
        self.row += 1
    # label
        self.stage_pos_label = QLabel("Stage Position:")
        self.readings_layout.addWidget(self.stage_pos_label,self.row,0,alignment=Qt.AlignRight)
    # reading
        self.stage_pos_display = QLabel("--")
        self.readings_layout.addWidget(self.stage_pos_display,self.row,1,alignment=Qt.AlignLeft)
        self.stage_pos_display.setFixedHeight(self.TEXT_HEIGHT)
        
        self.output_layout.addLayout(self.readings_layout,self.row,0,1,0)
        

#**************** Most Recent Command ******************#
        self.row += 1
        self.command_layout = QGridLayout()
    # label
        self.recent_command_label = QLabel("Most recent command:")
        self.command_layout.addWidget(self.recent_command_label,0,0,alignment=Qt.AlignRight)
    # reading
        self.most_recent_command = QLabel("--")
        self.command_layout.addWidget(self.most_recent_command,0,1,alignment=Qt.AlignLeft)
        self.most_recent_command.setFixedHeight(self.TEXT_HEIGHT)
    # timestamp
        self.recent_command_time = QLabel("")
        self.command_layout.addWidget(self.recent_command_time,1,1,alignment=Qt.AlignLeft)
        self.recent_command_time.setFixedHeight(self.TEXT_HEIGHT)
    # layout
        self.output_layout.addLayout(self.command_layout,self.row,0,1,0)
        self.row += 1 # for the graph
        
#**************** Status Bar ******************#
    # setup
        self.progress_widget = QWidget()
        self.progress_layout = QHBoxLayout(self.progress_widget)
        self.output_layout.addWidget(self.progress_widget,self.row,0,1,0)
    # label 0%
        lab0 = QLabel("0%")
        self.progress_layout.addWidget(lab0,alignment=Qt.AlignRight)
    # slider
        self.progress = QSlider(Qt.Horizontal,parent=self)
#         self.progress = QProgressBar(parent=self)
        self.progress_layout.addWidget(self.progress)
    # setup
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setEnabled(False)
        self.progress.setFixedHeight(30)
        self.progress.setMaximumWidth(640)
    # label 100%
        lab100 = QLabel("100%")
        self.progress_layout.addWidget(lab100,alignment=Qt.AlignLeft)
        self.progress_widget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)

        self.row += 1

#         self.blank = QLabel("")
#         self.blank.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
#         self.output_layout.addWidget(self.blank,self.row,0)       
        
#         self.row += 1