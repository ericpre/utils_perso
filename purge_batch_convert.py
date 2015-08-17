# -*- coding: utf-8 -*-
# Copyright 2015 Eric Prestat
#
#
# This is a free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# <http://www.gnu.org/licenses/>.-
"""
Find and delete all files containing a given string and having one the given extension
Usefull to delete useless files after a batch convertion.
"""
import os
from PyQt4 import QtGui

class PurgeBatchConvertedFiles(QtGui.QWidget):

    def __init__(self, subdirectory=True):
        super(PurgeBatchConvertedFiles, self).__init__()
        self._initUI()

        self.dname = os.getcwd()
        self.subdirectory = subdirectory

    def _initUI(self):
        # window
        self.setGeometry(300, 300, 800, 1000)        
        self.setWindowTitle('Purge batch converted files')   

        self.label1 = QtGui.QLabel('Find Files containing one of the following strings:', self)
        self.label2 = QtGui.QLabel('and having one of the following extensions:', self)
        self.SelectFolderButton = QtGui.QPushButton('Select folder', self)
        self.stringLineEdit = QtGui.QLineEdit(self)
        self.extentionLineEdit = QtGui.QLineEdit(self)
        self.convertedextentionLineEdit = QtGui.QLineEdit(self)
        self.DeleteButton = QtGui.QPushButton('Delete', self)
        self.CheckConvertedFileCheckBox = QtGui.QCheckBox('Check if files have been converted to', self)
        self.SubdirectoryCheckBox = QtGui.QCheckBox('Subdirectory', self)

        self.SubdirectoryCheckBox.setChecked(True)

        self._connect_gui()
        self._setup_table()

        # layout
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.stringLineEdit)
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.label2)
        hbox2.addWidget(self.extentionLineEdit)
        hbox3 = QtGui.QHBoxLayout()
        hbox3.addWidget(self.CheckConvertedFileCheckBox)
        hbox3.addWidget(self.convertedextentionLineEdit)
        hbox4 = QtGui.QHBoxLayout()
        hbox4.addWidget(self.SelectFolderButton)
        hbox4.addWidget(self.SubdirectoryCheckBox)
        hbox4.addWidget(self.DeleteButton)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        vbox.addWidget(self.table)
        self.setLayout(vbox)

        self.show()

    def _connect_gui(self):
        self.SelectFolderButton.clicked.connect(self._open_directory_dialog)
        self.CheckConvertedFileCheckBox.clicked.connect(self._get_files_list)
        self.SubdirectoryCheckBox.clicked.connect(self._get_files_list)        
        self.DeleteButton.clicked.connect(self._delete_files)
        self.stringLineEdit.textChanged.connect(self._get_files_list)
        self.extentionLineEdit.textChanged.connect(self._get_files_list)
        self.convertedextentionLineEdit.textChanged.connect(self._get_files_list)

    def _setup_table(self):
        self.table = QtGui.QTableWidget()
        self.table.setColumnCount(3)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setHorizontalHeaderLabels(['Path', 'Directory', 'File'])

    def _fill_table(self):
        self.table.setRowCount(len(self.to_delete_files_list))
        for i, fullfilename in enumerate(self.to_delete_files_list):
            fulldirname, filename = os.path.split(fullfilename)
            path, dirname = os.path.split(fulldirname)
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(path))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(dirname))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(filename))

    def _open_directory_dialog(self):
        self.dname = str(QtGui.QFileDialog.getExistingDirectory(self, directory=self.dname))
        if self.dname is '':
            self.dname = os.getcwd()
        self._get_files_list()

    def _get_files_list(self):
        self._read_parameter()
        self.to_delete_files_list = []
        self.not_to_delete_files_list = []
        self.subdirectory = self.SubdirectoryCheckBox.isChecked()
        # Get the list of files to delete
        self.get_conditional_files_list_to_delete_in_directory()        
        self._fill_table()

        print 'File not to delete because the converted files can\'t be found'
        print self.not_to_delete_files_list

    def _delete_files(self):
        for fullfilename in self.to_delete_files_list:
            os.remove(fullfilename)
        print 'Files deleted:'
        print self.to_delete_files_list
        self._get_files_list()

    def get_conditional_file_to_delete_list(self, files_list, path, string, ext,
                                            check_already_converted=True):
        """
        Get the list of files containing the string 'string' and the extention
        'ext'
        """
        for filename in files_list:
            if string in filename:
                if '.'+ext in filename:
                    filename2 = path+'/'+filename
                    if check_already_converted:
                        if self.check_already_converted(filename, files_list):
                            self.to_delete_files_list.append(filename2)
                        else:
                            self.not_to_delete_files_list.append(filename2)
                    else:
                        self.to_delete_files_list.append(filename2)

    def get_conditional_files_list_to_delete_in_directory(self):
        root_dir = self.dname
        string = self.string_list
        ext = self.extension_list
        subdirectory = self.subdirectory
        check_already_converted = self.CheckConvertedFileCheckBox.isChecked()

        if isinstance(string, str):
            string = [string]
        if isinstance(ext, str):
            ext = [ext]
        
        for ext in ext:
            for string2 in string:
                if subdirectory:
                    for root, subFolder, files_list in os.walk(root_dir):
                        self.get_conditional_file_to_delete_list(files_list,
                                                                 root, string2,
                                                                 ext,
                                                                 check_already_converted)
                else:
                    self.get_conditional_file_to_delete_list(os.listdir(root_dir),
                                                             root_dir, string2,
                                                             ext,
                                                             check_already_converted)

    def check_already_converted(self, filename, files_list):
        extension_list = self.convertedextentionLineEdit.text().split(', ')
        filename, ext = os.path.splitext(filename)
        for extension in extension_list:
            if filename+'.'+extension in files_list:
                return True
        return False

    def set_parameter(self, string_list=None, extension_list=None,
                      converted_file_extension=None):
        if string_list is not None:
            self.stringLineEdit.setText(', '.join(string_list))
        if extension_list is not None:
            self.extentionLineEdit.setText(', '.join(extension_list))
        if converted_file_extension is not None:
            self.convertedextentionLineEdit.setText(', '.join(converted_file_extension))

    def _read_parameter(self):
        self.string_list = self.stringLineEdit.text().split(', ')
        self.extension_list = self.extentionLineEdit.text().split(', ')
  
if __name__ == '__main__':
    # default parameter
    string_list = ['Spectrum Image', 'Thumbs']
    extension_list = ['jpg','raw', 'rpl', 'db']
    converted_file_extension = ['dm3', 'dm4']
    
#    string_list = 'mapping'
#    extension_list=['png']
    
    import sys
    app = QtGui.QApplication(sys.argv)
    purge_batch_converted_files_widget = PurgeBatchConvertedFiles()
    purge_batch_converted_files_widget.set_parameter(string_list,
                                                     extension_list,
                                                     converted_file_extension)
    
    
    

    

    

