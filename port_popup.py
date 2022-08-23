import pyvisa
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# the popup to choose the ports for the instruments
class Port_Popup(QDialog):

    def __init__(self, parent):        
        super(Port_Popup, self).__init__(parent)
        self.p = parent # the overall window
        self.do_close = False # default: don't close unless "Confirm" is pressed
        self.setWindowTitle("Port Selection")
        # find which ports exist
        self.rm = pyvisa.ResourceManager()
        self.port_list = self.rm.list_resources()
        
        self.init_UI()
        
    def init_UI(self):
        self.layout = QGridLayout(self)

# The dropdowns aren't connected to any functions, 
# because they will be read when the popup is closed.  
        
#************************ Stage Port **************************#
    # label
        self.stage_port_label = QLabel("Stage Port Name:")
        self.layout.addWidget(self.stage_port_label,0,0,alignment=Qt.AlignRight)
    # dropdown
        self.stage_port_dropdown = QComboBox()
        self.stage_port_dropdown.addItems(["None"])
        self.stage_port_dropdown.addItems(self.port_list)
    # layout
        self.layout.addWidget(self.stage_port_dropdown,0,1)
        self.stage_port_dropdown.setMaximumWidth(200)

#************************ Electrometer Port **************************#
    # label
        self.electrometer_port_label = QLabel("Electrometer Port Name:")
        self.layout.addWidget(self.electrometer_port_label,1,0,alignment=Qt.AlignRight)
    # dropdown
        self.electrometer_port_dropdown = QComboBox()
        self.electrometer_port_dropdown.addItems(["None"])
        self.electrometer_port_dropdown.addItems(self.port_list)
    # layout
        self.layout.addWidget(self.electrometer_port_dropdown,1,1)
        self.electrometer_port_dropdown.setMaximumWidth(200)

#************************ Autosave  **************************#

    # label
        self.auto_save_label = QLabel("Auto-save as: ")   
        self.layout.addWidget(self.auto_save_label,2,0, alignment = Qt.AlignRight)
        self.auto_save_label.setMaximumHeight(20)
    # Current file label
        self.file_name_label = QLabel(os.getcwd()+"\Most_Recent_Data.xlsx")
        self.layout.addWidget(self.file_name_label,2,1,alignment = Qt.AlignRight)
            # self.p.set_save_file_name("D:\Sync\Other\Python\Chem Lab\GUI\Most_Recent_Data.xlsx")
                # Shouldn't be necessary because it is read at the end
    # set button
        self.set_auto_save = QPushButton("Set")
        self.set_auto_save.clicked.connect(self.choose_save_file)
        self.set_auto_save.setCheckable(False)   # button can't stay down
    # layout
        self.set_auto_save.setFixedWidth(50)
        self.layout.addWidget(self.set_auto_save,3,1,alignment = Qt.AlignRight)
        
#************************ Ok Button  **************************#
        
        self.ok_btn = QPushButton("Confirm")
        self.layout.addWidget(self.ok_btn,4,1)
        self.ok_btn.clicked.connect(self.myclose) # the function that actually closes the window
        self.ok_btn.setFixedWidth(120)

    # the function to actually close
    def myclose(self):
        self.do_close = True
    # pass the ports and file name to the main window
        self.p.set_stage_port(self.stage_port_dropdown.currentText())
        self.p.set_electrometer_port(self.electrometer_port_dropdown.currentText())
        self.p.set_save_file_name(self.file_name_label.text())
    
        self.close()

        
    def closeEvent(self, event):
        if self.do_close: # i.e., if myclose has been called
            event.accept()
        else: # i.e., if the x button has been pressed
            # (don't exit)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Please click the Confirm button instead")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
            event.ignore()
            
    def choose_save_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("Excel files (*.xlsx)")
        if dlg.exec():
            filename = dlg.selectedFiles()[0] # the filename the user selects
            self.save_file_name = utils.excelFormat(filename)
            self.file_name_label.setText(self.save_file_name)
#             self.p.set_save_file_name(self.save_file_name)
                # Shouldn't be necessary because it is read at the end