import os
import pyfits
from astropy.io import fits
import numpy as np
import pickle
import shutil
from PIL import Image


def test_image(file_name, threshold=5000):
    # check size of image and return False if size is below threshold 
    statinfo = os.stat(file_name)
    if statinfo.st_size < threshold:
        return False
    return True

def load_data(file_name):
    '''
    load the various file_name format
    '''
    data_type = get_data_type(file_name)
    if data_type == '.fits':
        hdulist = fits.open(file_name, ignore_missing_end=True)
        hdu = hdulist[0]
        _image = np.asarray(hdu.data)
        hdulist.close()
        return _image
    elif (data_type == '.tiff') or (data_type == '.tif'):
        _image = Image.open(file_name)
        return np.array(_image)
    else:
        return []
    
def get_data_type(file_name):
    '''
    using the file name extension, will return the type of the data
    
    Arguments:
        full file name
        
    Returns:
        file extension    ex:.tif, .fits
    '''
    filename, file_extension = os.path.splitext(file_name)
    return file_extension.strip()

def save_file(folder='', base_file_name='', suffix='', dictionary={}):
    if folder == '':
        return
    
    output_file = folder + base_file_name + '_time_dictionary.dat'
    pickle.dump(dictionary, open(output_file, "wb"))
    
    return output_file

def get_file_duration(file_name):
    hdu_list = pyfits.open(file_name)
    hdu_0 = hdu_list[0]
    return hdu_0.header['EXPOSURE']

def read_single_fits(file):
    hdu_list = pyfits.open(file)  # fits
    hdu = hdu_list[0]
    _image = hdu.data
    _image = np.asarray(_image)
    hdu_list.close()
    return _image
    
def read_fits(list_files):
    '''takes a list of files, load them using pyfits and return a list of 
    arrays of data
    '''
    data = []
    for _file in list_files:

        hdu_list = fits.open(_file, ignore_missing_end=True)
        hdu = hdu_list[0]
        _image = hdu.data
        _image = np.asarray(_image)
        data.append(_image)
        hdu_list.close()
    return data    

def make_fits(data=[], filename=''):
    hdu = pyfits.PrimaryHDU(data)
    hdulist = pyfits.HDUList([hdu])
    hdulist.writeto(filename)
    hdulist.close()
    
def make_tiff(data=[], filename=''):
    new_image = Image.fromarray(data)
    new_image.save(filename)

def export_file(data=[], output_folder='', base_file_name=''):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    _full_output_file_name = os.path.join(output_folder, base_file_name)
    if os.path.exists(_full_output_file_name):
        return
    
    hdu = pyfits.PrimaryHDU(data)
    hdulist = pyfits.HDUList([hdu])
    hdulist.writeto(_full_output_file_name)
    hdulist.close()
    
def make_or_reset_folder(folder_name):
    if os.path.exists(folder_name):
         shutil.rmtree(folder_name)
    os.makedirs(folder_name)         
    
def remove_SummedImg_from_list(list_files):
    base_name_and_extension = os.path.basename(list_files[0])
    dir_name = os.path.dirname(list_files[0])
    [base_name, _] = os.path.splitext(base_name_and_extension)
    base_base_name_array = base_name.split('_')
    name = '_'.join(base_base_name_array[0:-1])
    index = base_base_name_array[-1]
    file_to_remove = os.path.join(dir_name, name + '_SummedImg.fits')
    list_files_cleaned = []
    for _file in list_files:
        if _file == file_to_remove:
            continue
        list_files_cleaned.append(_file)
    return list_files_cleaned
    
def make_ascii_file(metadata=[], data=[], output_file_name='', dim='2d'):
    f = open(output_file_name, 'w')
    for _meta in metadata:
        _line = _meta + "\n"
        f.write(_line)
        
    for _data in data:
        if dim == '2d':
            _str_data = [str(_value) for _value in _data]
            _line = ",".join(_str_data) + "\n"
        else:
            _line = _data + '\n'
        f.write(_line)
       
    f.close()
    
def make_ascii_file_3d_array(metadata=[], first_column=[], data=[], output_file_name=''):
           
    f = open(output_file_name, 'w')
    for _meta in metadata:
        _line = _meta + "\n"
        f.write(_line)
        
    for _index, _data in enumerate(data):
        _str_data = [str(_value) for _value in _data]
        _line = "{}".format(str(first_column[_index]) + "," + ",".join(_str_data) + "\n")
        f.write(_line)
       
    f.close()
   