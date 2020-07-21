import feather
import pandas as pd
import scipy
import pickle


# Create load and save function for: pickels, csv, feather, npz

def load_csv():
  pass

def save_csv():
  pass

def load_feather(filename, path):
  """ load data from a local feather file

  Parameters
  ----------
  filename : str
    name of the feather file
  path : str
    path to the file
  """
  return pd.read_feather('../working/' + path + '/' + filename + '.feather')

def save_feather(df,filename,path="./"):
  """ save data to a local feather file

  Parameters
  ----------
  df : Pandas DataFrame
    data that stored in the file
  filename : str
    name of the feather file
  path : str
    path to the file
  """
  feather.write_dataframe(df,'../working/' + path + '/' + filename + '.feather')

def load_npz(filename, path):
  """ load data from a local npz file

  Parameters
  ----------
  filename : str
    name of the npz file
  path : str
    path to the file
  """
  return scipy.sparse.load_npz('../working/' + path + '/' + filename + '.npz')

def save_npz(data,filename, path):
  """ save data to a local npz file

    Parameters
    ----------
    data : ??
      data that stored in the file
    filename : str
      name of the npz file
    path : str
      path to the file
    """
  scipy.sparse.save_npz('../working/' + path + '/' + filename + '.npz', data)

def load_pickel(filename,path):
  """ load data from a local pickel file

  Parameters
  ----------
  filename : str
    name of the pickel file
  path : str
    path to the file
  """
  return  pickle.load(open('../working/' + path + '/' + filename + '.p', 'rb'))

def save_pickel(data,filename,path):
  """ save data to a local pickel file

    Parameters
    ----------
    data : ??
      data that stored in the file
    filename : str
      name of the feather file
    path : str
      path to the file
    """
  pickle.dump(data, open('../working/' + path + '/' + filename + '.p', 'wb'))

