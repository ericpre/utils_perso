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
Delete all files containing a given string 'string' and a given extension 'ext'
Usefull to delete useless files after a batch convertion
"""
import os

def conditional_delete_file(files_list, path, string, ext):
    """
    function that deletes files containing the string 'string' and the extention
    'ext'
    """
    for filename in files_list:
        if string in filename:
            if '.'+ext in filename:
                filename2 = path+'/'+filename
                os.remove(filename2)
                print filename+' deleted'

def conditional_delete_file_in_directory(root_dir, string, ext,
                                         subdirectory=True):
    """
    Delete all the files contening the given string and extension in the file
    and its subdirectories if option is selected
    
    Parameters
    ----------
    root_dir : str, corresponding to the main directory
    
    string: list of str or str, all files containing this string and the
            corresponding ext parameter will be deleted
            
    ext: list of str or str, all files containing this extension and the
            corresponding string parameter will be deleted
            
    subdirectory : bool, apply to subdirectories or not    
    """
    if isinstance(string, str):
        string = [string]
    if isinstance(ext, str):
        ext = [ext]
    
    for ext in ext:
        for string2 in string:
            if subdirectory:
                for root, subFolder, files_list in os.walk(root_dir):
                    print '*******************\n'+root
                    conditional_delete_file(files_list, root, string2, ext)
            else:
                conditional_delete_file(os.listdir(root_dir), root_dir, string2, ext)

    
if __name__ == '__main__':
    string = 'Spectrum Image'
    ext=['jpg','raw', 'rpl']
    
    root_dir = os.getcwd()
    conditional_delete_file_in_directory(root_dir, string, ext, subdirectory=True)
    

    

