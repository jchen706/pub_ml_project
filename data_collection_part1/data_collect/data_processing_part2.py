
from bs4 import BeautifulSoup
import requests
import pandas
import sys
from selenium import webdriver
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import re

static_url = 'https://www.nasdaq.com'
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-ssl-errors')
# options.add_argument('--ignore-certificate-errors-spki-list')
# driver = webdriver.Chrome(options= options ,executable_path=r"C:\Users\jchen\Documents\chromedriver\chromedriver.exe")
# driver.implicitly_wait(10)
#https://sec-api.io/docs#query-financial-statementss
from selenium.webdriver.firefox.options import Options
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r"C:\Users\jchen\Documents\firefoxdriver\geckodriver.exe", firefox_options=options)
driver.implicitly_wait(10)
error_companies = []
error_index = []
value_error_index = []
value_error_com = []
less_than_10_employees = []
less_than_10_employees_index = []

def getCompanyPage(href, company_name, index, share_price):
      # headers={}
      # headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
      # print('request')
      # r = requests.get(static_url+href, headers=headers)

      # print(static_url+href)

      # #page = urlopen(static_url+href)
      # m_page = BeautifulSoup(r, 'html.parser')
      # print(m_page.prettify())
      # sys.exit(1)
    print('----')
    print("Index: " + str(index))
    print('----')
  
    try:


    
      driver.get(static_url+href)
      page_source = driver.page_source


      soup = BeautifulSoup(page_source, 'lxml')

      #print(soup.prettify())


    


      
      #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='content-container']/div[@class='content overview active']/table/tr")))

      #company_table = driver.find_element_by_xpath("//div[@class='content-container']/div[@class='content overview active']/table")


      #tableHTML = company_table.get_attribute('outerHTML')
      #com_page = BeautifulSoup(tableHTML, 'html.parser')

      # print("--")
      # print(com_page.prettify())
      # print("--")
      table = soup.find('table')
      # print(table)


      table_body_com = table.find('tbody')
      rows_com = table_body_com.find_all('tr')
      tds = table_body_com.find_all('td')

      employees =  tds[4].getText().strip().split(" ")[0].replace(',','')
      if int(employees) < 10:
          print('-- Less than 10 --')
          less_than_10_employees.append(company_name)
          less_than_10_employees.append(index)
          return None
      print(employees)
      print('----')
      shared_outstanding = tds[17].getText().strip()
      print(shared_outstanding)
      print('----')
      print(shared_outstanding)
      temp = float(re.sub('\D', '', shared_outstanding))
      print(temp)
      print(type(temp))
      print(type(share_price))
      print(share_price)
      stock_valuation = temp * float(share_price)
      print(stock_valuation)
      print('----')
      company_address = tds[9].getText().strip()
      print(company_address)
      print('----')
      phone = tds[10].getText().strip()
      print(phone)
      print('----')


      return employees, shared_outstanding, stock_valuation, company_address, phone
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
      
      if (ex_type.__name__ == 'ValueError'):
          value_error_com.append(company_name)
        

          value_error_index.append(index)

      else:
        error_companies.append(company_name)
        

        error_index.append(index)
        return None
      return None




"""

  returns a panda dataframe type
"""
def readFromCsv(file_name):
  data = pandas.read_csv(file_name)
  print(data)
  print(type(data))
  return data

def writeToCsv(data, column_names, file_name):
  com = pandas.DataFrame(data, columns = column_names)
  com.to_csv(file_name, sep=',', na_rep='None')

def run_company_pages(file_name):
  df = readFromCsv(file_name)
  href_key = df.keys()[8]
  drop_list = []
  drop_index = []
  print('here')
  df['employees'] = 0
  df['shares_outstanding'] = 0
  df['stock_valuation']=0
  df['company_address']="None"
  df['phone']="0"
  share_key = df.keys()[4]
  company_name_key = df.keys()[1]
  index_key = df.keys()[0]


  print('here1')
  count = 0

  for index, row in df.iterrows():
    try:
      share_price = row[share_key]
      company_name = row[company_name_key]
      index = row[index_key]

      print(row[df.keys()[1]])
      print(row[href_key])
      print(share_price)
      val = getCompanyPage(row[href_key], company_name, index,share_price)
      if val == None or val is None:
        #row 1 is company name
        drop_list.append(row[1])
        drop_index.append(row[0])
        continue
      else:
        employees, shared_outstanding, stock_valuation, company_address, phone = val
        df.loc[index,'employees'] = employees
        df.loc[index,'shares_outstanding'] = shared_outstanding
        df.loc[index,'stock_valuation']= stock_valuation
        df.loc[index,'company_address']= company_address
        df.loc[index, 'phone'] = phone
        df = df.reset_index(drop=True)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.to_csv('part_2_data/companies_years_2009_2020_p2_v1_total.csv', sep=',', na_rep='None')

      # count+=1
      # if (count == 20):
      #   break
    
    except KeyboardInterrupt:
      df = df.drop(drop_index)
      writeToCsv(drop_list,['company_name'], 'companies_drop_spacs_part2_v1.csv')
      writeToCsv(error_companies,['company_name'], 'companies_error_names_part2_v1.csv')
      writeToCsv(error_index,['index'], 'companies_error_index_part2_v1.csv')
      writeToCsv(value_error_com,['company_name'], 'companies_value_error_names_part2_v1.csv')
      writeToCsv(value_error_index,['index'], 'companies_value_error_index_part2_v1.csv')
      writeToCsv(less_than_10_employees,['company_name'], 'companies_less_employees_names_part2_v1.csv')
      writeToCsv(less_than_10_employees_index,['index'], 'companies_less_employees_index_part2_v1.csv')

      

      df = df.reset_index(drop=True)
      df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

      df.to_csv('part_2_data/companies_years_2009_2020_p2_v1_total.csv', sep=',', na_rep='None')
      print("Current Index: " + str(index))

  df = df.drop(drop_index)
  writeToCsv(drop_list,['company_name'], 'companies_drop_spacs_part2_v1.csv')
  writeToCsv(error_companies,['company_name'], 'companies_error_names_part2_v1.csv')
  writeToCsv(error_index,['index'], 'companies_error_index_part2_v1.csv')
  writeToCsv(value_error_com,['company_name'], 'companies_value_error_names_part2_v1.csv')
  writeToCsv(value_error_index,['index'], 'companies_value_error_index_part2_v1.csv')
  writeToCsv(less_than_10_employees,['company_name'], 'companies_less_employees_names_part2_v1.csv')
  writeToCsv(less_than_10_employees_index,['index'], 'companies_less_employees_index_part2_v1.csv')

    

  df = df.reset_index(drop=True)
  df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

  df.to_csv('part_2_data/companies_years_2009_2020_p2_v1_total.csv', sep=',', na_rep='None')









  





if __name__ == "__main__":
  file_name = 'part_1_data/companies_years_2009_2020_p1_v1_total.csv'
  run_company_pages(file_name)
 
  
  driver.close()
  