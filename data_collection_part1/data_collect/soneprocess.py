"""

Using edgar-online api for SEC S-1 Filings parsing

"""

import pandas
import util
from bs4 import BeautifulSoup
import sys
import traceback
from urllib.request import urlopen
import json
import company
from company import AF


#link: ikt
app_key = '22bc809f268182c5196b611916b5c525'
static_url = 'https://datafied.api.edgar-online.com/v2/corefinancials/ann?primarysymbols='
end_url = '&numperiods=100&appkey=' + app_key


all_errors = []

def parse_helper(json_item, year, ticker):
  print('Helper')
  rows = json_item['result']['rows']
  total_rows = json_item['result']['totalrows']
  last_row = json_item['result']['rows'][total_rows-1]
  last_row_num = total_rows -1
  revenue = {}
  ipo_year = int(year) - 1

  ret = {}
  done = False
  ipo_done = False
  pre_done = False
  try:
    for i in range(total_rows):
      r = json_item['result']['rows'][total_rows-i-1]
      values = r['values']
      rowvalues = {}
      is_ipo_year = False
      is_pre_year = False
      
      
      for j in range(len(values)):
        f = values[j]
        if f['field'] == 'fiscalyear':
          print(f['value'])
          #ipo year
          if f['value'] == ipo_year:
            ipo_done = True
            is_ipo_year = True
          if f['value'] == ipo_year-1:
            is_pre_year = True
            pre_done = True
        if f['field'] == 'sicdescription':
          rowvalues['sicdescription'] = f['value']
        if f['field'] == "ebit":
          rowvalues["ebit"] = f['value']
        if f['field'] == "grossprofit":
          rowvalues['grossprofit'] = f['value']
        if f['field'] == "netincome":
          rowvalues['netincome'] = f['value']
        if f['field'] == "totalrevenue":
          rowvalues['totalrevenue'] = f['value']
        if f['field'] == "costofrevenue":
          rowvalues['costofrevenue'] = f['value']
        if f['field'] == "totalassets":
          rowvalues['totalassets'] = f['value']

      if is_pre_year:
        revenue[ipo_year-1] = rowvalues['totalrevenue']
      if is_ipo_year:
        revenue[ipo_year] = rowvalues['totalrevenue']
        ret['sicdescription'] = rowvalues['sicdescription']
        ret["ebit"] =  rowvalues["ebit"]
        ret['grossprofit']=rowvalues['grossprofit']
        ret['netincome']=rowvalues['netincome']
        ret['totalrevenue']=rowvalues['totalrevenue']
        ret['costofrevenue']=rowvalues['costofrevenue']
        ret['totalassets']=rowvalues['totalassets']
        
      if ipo_done and pre_done:
        break
    if ipo_done and not pre_done:
      print('---No One Year Before--')
    revenue_growth = (revenue[ipo_year] - revenue[ipo_year-1]) / revenue[ipo_year-1]
    print(revenue_growth)
    ret['revenue_growth'] = revenue_growth
    return ret

  except Exception as e:
    print(str(e))
    ex_type, ex_value, ex_traceback = sys.exc_info()

    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)

    # Format stacktrace
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

    print("Exception type : %s " % ex_type.__name__)
    print("Exception message : %s" %ex_value)
    print("Stack trace : %s" %stack_trace)
    all_errors.append(str([ticker,ex_type.__name__ ,ex_value,stack_trace]))
    
    return None

  

      





      
          
      




  

  # 'sicdescription'
  # 'fiscalyear'
  # "ebit"
  # "grossprofit"
  # "netincome"
  # "totalrevenue"
  # "costofrevenue"
  # "totalassets"
  




def run_part3_collect(file_name):
  df = util.readFromCsv(file_name)
 

  ticker_key = df.keys()[2]
  index_key = df.keys()[0]
  companies_key = df.keys()[1]

  date_key = df.keys()[7]
  df[date_key] = pandas.to_datetime(df[date_key])


  no_rows_companies = []
  no_rows_index = []
  error_companies = []
  error_index = []
  none_companies = []
  none_index = []
  df['sicdescription'] = "None"
  df["ebit"] =  "None"
  df['grossprofit']="None"
  df['netincome']="None"
  df['totalrevenue']="None"
  df['costofrevenue']="None"
  df['totalassets']="None"
  df['revenue_growth'] = "None"

  for index, row in df.iterrows():
    year = row[date_key].year
    print(str(year))

    ticker_symbol = row[ticker_key]
    print("Ticker : " + str(ticker_symbol))
    url = static_url+ticker_symbol+end_url
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    try:
      print("Index: " + str(index))
      #print(bs.prettify())
      bs2 = json.loads(bs.prettify())
      #print(type(bs2))
      if (bs2['result']['totalrows'] == 0):
        print("----No Row ----")
        no_rows_companies.append(row[companies_key])
        no_rows_index.append(index)
      else:
        val = parse_helper(bs2, year, ticker_symbol)
        if val is None or val == None:
          print("---- None ----")

          none_companies.append(ticker_symbol)
          none_index.append(index)
          continue
        else:
          print("----Write----")
          df.loc[index,'sicdescription'] = val['sicdescription'] 
          df.loc[index,"ebit"] =   val["ebit"]
          df.loc[index,'grossprofit']=val['grossprofit']
          df.loc[index,'netincome']=val['netincome']
          df.loc[index,'totalrevenue']=val['totalrevenue']
          df.loc[index,'costofrevenue']=val['costofrevenue']
          df.loc[index,'totalassets']=val['totalassets']
          df.loc[index,'revenue_growth'] = val['revenue_growth']

          df = df.reset_index(drop=True)
          df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
          df.to_csv('part_3_data/companies_years_2009_2020_p3_v1_total.csv', sep=',', na_rep='Nane')
        
          
          
    except:
      error_index.append(index)
      error_companies.append(ticker_symbol)
      continue

  util.writeToCsv(no_rows_companies,['company_name'], 'no_rows_names_part3_v1.csv')
  util.writeToCsv(no_rows_index,['index'], 'no_rows_index_index_part3_v1.csv')
  df = df.drop(none_index)
  df = df.drop(no_rows_index)
  df = df.reset_index(drop=True)
  df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
  df.to_csv('part_3_data/companies_years_2009_2020_p3_v1_total.csv', sep=',', na_rep='None')

  util.writeToCsv(none_companies,['company_name'], 'companies_none_com_part3_v1.csv')
  util.writeToCsv(none_index,['index'], 'companies_none_index_part3_v1.csv')
  util.writeToCsv(error_companies,['company_name'], 'companies_error_names_part3_v1.csv')
  util.writeToCsv(error_index,['index'], 'companies_error_index_part3_v1.csv')


  return


if __name__ == "__main__":
  file_name = "part_2_data\companies_years_2009_2020_p2_v1_total.csv"
  run_part3_collect(file_name)
  util.writeToCsv(all_errors,['errors'], 'companies_error_index_part3_v1.csv')



  #tear down the driver
  #driver.close()



