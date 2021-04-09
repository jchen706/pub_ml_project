import pandas

def readFromCsv(file_name):
  data = pandas.read_csv(file_name)
  print(data)
  print(type(data))
  return data

def writeToCsv(data, column_names, file_name):
  com = pandas.DataFrame(data, columns = column_names)
  com.to_csv(file_name, sep=',', na_rep='None')