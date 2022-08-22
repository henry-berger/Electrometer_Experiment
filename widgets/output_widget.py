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
        self.output_layout = QGridLayout()

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
        self.olabel.setMaximumHeight(36)
    
    
# These labels will be changed as the variables change
    
#************************ Time **************************#
        self.row += 1
    # label
        self.time_label = QLabel("Time:")
        self.output_layout.addWidget(self.time_label,self.row,0,alignment=Qt.AlignRight)
    # reading
        self.time_display = QLabel("--")
        self.output_layout.addWidget(self.time_display,self.row,1,alignment=Qt.AlignLeft)
        self.time_display.setMaximumHeight(28)

#************** Electrometer Reading ********************#
        self.row += 1
    # label
        self.eread_label = QLabel("Current Value:")
        self.output_layout.addWidget(self.eread_label,self.row,0,alignment=Qt.AlignRight)
    # reading
        self.eread_display = QLabel("--")
        self.output_layout.addWidget(self.eread_display,self.row,1,alignment=Qt.AlignLeft)
        self.eread_display.setMaximumHeight(28)

#******************* Stage Position ********************#
        self.row += 1
    # label
        self.stage_pos_label = QLabel("Stage Position:")
        self.output_layout.addWidget(self.stage_pos_label,self.row,0,alignment=Qt.AlignRight)
    # reading
        self.stage_pos_display = QLabel("--")
        self.output_layout.addWidget(self.stage_pos_display,self.row,1,alignment=Qt.AlignLeft)
        self.stage_pos_display.setMaximumHeight(28)

#**************** Most Recent Command ******************#
        self.row += 1
        self.command_layout = QGridLayout()
    # label
        self.recent_command_label = QLabel("Most recent command:")
        self.command_layout.addWidget(self.recent_command_label,0,0,alignment=Qt.AlignRight)
    # reading
        self.most_recent_command = QLabel("--")
        self.command_layout.addWidget(self.most_recent_command,0,1,alignment=Qt.AlignLeft)
        self.most_recent_command.setMaximumHeight(28)
    # timestamp
        self.recent_command_time = QLabel("")
        self.command_layout.addWidget(self.recent_command_time,1,1,alignment=Qt.AlignLeft)
        self.recent_command_time.setMaximumHeight(28)
    # layout
        self.output_layout.addLayout(self.command_layout,self.row,0,1,0)
        self.row += 1 # for the graph
        
#**************** Status Bar ******************#
    # setup
        self.progress_layout = QHBoxLayout()
        self.output_layout.addLayout(self.progress_layout,self.row,0,1,0)
    # label 0%
        lab0 = QLabel("0%")
        self.progress_layout.addWidget(lab0)
    # slider
        self.progress = QSlider(Qt.Horizontal,parent=self)
#         self.progress = QProgressBar(parent=self)
        self.progress_layout.addWidget(self.progress)
    # setup
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setEnabled(False)
    # label 100%
        lab100 = QLabel("100%")
        self.progress_layout.addWidget(lab100)
        
        self.row += 1