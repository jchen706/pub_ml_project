"""
Selenium Driver with BeautifulSoup

"""


import os 
import selenium 
from selenium import webdriver
import sys
import traceback
from bs4 import BeautifulSoup
import company
from company import Company
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import pandas
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

def int_month_coversion(month):
  if int(month) < 10:
    return '0'+str(month)
  else:
    return str(month)


def update(month):
  if month == '01':
    return '02'
  if month == '02':
    return '03'
  if month == '03':
    return '04'
  if month == '04':
    return '05'
  if month == '05':
    return '06'
  if month == '06':
    return '07'
  if month == '07':
    return '08'
  if month == '08':
    return '09'
  if month == '09':
    return '10'
  if month == '10':
    return '11'
  if month == '11':
    return '12'
  if month == '12':
    return '01'

def codemonth(month):
  if month == '01':
    return 'JAN'
  if month == '02':
    return 'FEB'
  if month == '03':
    return 'MAR'
  if month == '04':
    return 'APR'
  if month == '05':
    return 'MAY'
  if month == '06':
    return 'JUN'
  if month == '07':
    return 'JUL'
  if month == '08':
    return 'AUG'
  if month == '09':
    return 'SEP'
  if month == '10':
    return 'OCT'
  if month == '11':
    return 'NOV'
  if month == '12':
    return 'DEV'

def clear_entire_text(element):
    element.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)
  

def input_date(driver, start_month, year):
  date_w =  driver.find_element_by_xpath("//div[@class='date-picker date-picker--month-only']")

  date_widget =  date_w.find_element_by_xpath("//button[@class='date-picker__toggle']")
  date_widget.click()
  driver.implicitly_wait(20) 

  date_picker =  driver.find_element_by_xpath("//div[@class='date-picker__widget']")


  data_input = date_picker.find_element_by_xpath("//input[@class='date-picker__input']")
  d = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'date-picker__input')))
  data_input.click()
  print("Element is visible? " + str(data_input.is_displayed()))
  

  # MM/YYYY
  data_input.clear()
  data_input.send_keys(start_month+str(year))

  data_apply = date_picker.find_element_by_xpath("//button[@class='date-picker__apply']")

  data_apply.click()


def getCompanyPage(company_temp):
    href = company_temp.href

    driver.get(href)

    company_table = driver.find_element_by_xpath("//table")

    tableHTML = company_table.get_attribute('outerHTML')
    com_page = BeautifulSoup(tableHTML, 'html.parser')

    # print("--")
    # print(com_page.prettify())
    # print("--")
    table_body_com = com_page.find('tbody')
    rows_com = table_body_com.find_all('tr')
    tds = table_body_com.find_all('td')

    employees =  tds[4].getText().strip().split(" ")[0].replace(',','')
    if int(employees) < 10:
        driver.implicitly_wait(20) 
        #driver.execute_script("window.history.go(-1)")
        driver.refresh()
        #driver.back()
        driver.implicitly_wait(20)
        return None
    print(employees)
    print('----')
    shared_outstanding = tds[17].getText().strip()
    print(shared_outstanding)
    print('----')
    stock_valuation = int(shared_outstanding.replace(',','')) * float(share_price)
    print(stock_valuation)

    driver.implicitly_wait(20) 
    #driver.execute_script("window.history.go(-1)")
    driver.refresh()
    #driver.back()
    driver.implicitly_wait(20) 

    return employees, shared_outstanding, stock_valuation


def writeToCsvPartOne(data, column_names):
  #cities = pd.DataFrame([['Sacramento', 'California'], ['Miami', 'Florida']], columns=['City', 'State'])
  #cities.to_csv('cities.csv')
  l = []
 
  for each_company in data:
    l.append(each_company.toListPartOne())
    
  com = pandas.DataFrame(l, columns = column_names)
  com.to_csv('companies_2010_2020_p1_v2_error_redo_v14.csv', sep=',', na_rep='None')
  
def writeToCsvErrorYears(data, column_names):
  l = []
 
  for each_tup in data:
    l.append([each_tup[0], each_tup[1]])
  com = pandas.DataFrame(l, columns = column_names)
  com.to_csv('error_years_2010_2020_p1_v2_redo_v14.csv', sep=',', na_rep='None')

"""

  returns a panda dataframe type
"""
def readFromCsvErrorYears(file_name):
  data = pandas.read_csv(file_name)
  print(data)
  print(type(data))
  return data


def getCompanyPageBs():
  return 
  

def runErrorYears():

  #read from csv
  dates = readFromCsvErrorYears('error_years_2010_2020_p1_v2_redo_v13.csv')
 
    



  options = webdriver.ChromeOptions()
  options.add_argument('--ignore-ssl-errors')
  options.add_argument('--ignore-certificate-errors-spki-list')


  driver = webdriver.Chrome(options= options ,executable_path=r"C:\Users\jchen\Documents\chromedriver\chromedriver.exe")
  driver.implicitly_wait(30)
  nasdaq_url = 'https://www.nasdaq.com'
  driver.get('https://www.nasdaq.com/market-activity/ipos')
  driver.implicitly_wait(20)


  data = []


  start_month = '01'
  start_year = 2020

  #(month, year)
  error_years = []


  # step from 2010 to 2021
  for index, row in dates.iterrows():
      month = int_month_coversion(str(row['month']))
      year = str(row['year'])

      print(str(row['month']) + " " + str(row['year']))
      # nested try except to get all the data
      #step for each month 12 months
      try:
        #date picker widget
        
        driver.implicitly_wait(30) 


        # d = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//div[@class='time-belt']/div[@class='time-belt__list']/button[@class='time-belt__item time-belt__item--active' and text()="+month_str+" "+ str(year)+"]")))
        # print("Element is visible? " + str(d.is_displayed()))


        # driver.explicitly_wait(1000) 


        #wait for 2019 to appear
        input_date(driver, month, year)


        section_of_tables = driver.find_element_by_xpath("//div[@class='market-calendar-table market-calendar-table--with-title']/h3[text()='Priced']/..")
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        _element = WebDriverWait(driver, 20,ignored_exceptions=ignored_exceptions)\
                          .until(EC.presence_of_element_located((By.XPATH, "//div[@class='market-calendar-table market-calendar-table--with-title']/h3[text()='Priced']/..")))

        element1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'market-calendar-table__cell-content')))

        #for each in section_of_tables:
        try:
            #WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='market-calendar-table market-calendar-table--with-title/h3[text()='Priced']/../table']")))

            elementHTML = section_of_tables.get_attribute('outerHTML')
            page = BeautifulSoup(elementHTML, 'html.parser')

            # print("--")
            # print(page.prettify())
            # print("--")

            table_body = page.find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
              try:
                tds = row.find_all('td')
                #print('--------')
                #print(tds[6].getText().strip())
                if tds[6].getText().strip() == 'Priced':
                  th = row.find('th')
                  ticker = th.getText().strip()
                  href = th.find('a').get('href')
                  print(href)
                  company_name = tds[0].getText().strip()
                

                  print('--')
                  print(ticker)
                  print(company_name)
                  print("--")
                
                  exchange = tds[1].getText().strip()
                  #print(exchange)
                  share_price = tds[2].getText().strip()
                  #print(share_price)
                  #print("-------------")
                  shares_offered = tds[3].getText().strip()
                  #print(shares_offered)
                  #print("-------------")
                  date_of_priced = tds[4].getText().strip()
                  #print(date_of_priced)"
                  #print("-------------")
                  dollar_value_of_shares = tds[5].getText().strip()
                  #print(shares_offered)
                  #print("-------------")

                  #add pops up

                  #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                  #driver.switch_to.alert.dismiss()

                  #element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.LINK_TEXT, ticker)))

                  #link_to_page = driver.find_element_by_link_text(ticker)
                  #href = link_to_page.get_attribute('href')


                  #goes to the companies page 
                  



                  #driver.execute_script("arguments[0].click();", link_to_page)
                  
                  #javascript to execute click on the company ticker
                  
                  # element=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.LINK_TEXT ,ticker)))
                  # element.click()

                  
                  com = Company(company_name,ticker,exchange,share_price,shares_offered,dollar_value_of_shares,date_of_priced, href)
                  data.append(com)
                  print("---Finish---")
                  
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
                    error_years.append((month, year))

                    continue   
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
            error_years.append((month, year))

            continue   
        


        print("Number of Companies: " + str(len(data)))
        # # class name = market-calendar-table market-calendar-table--with-title
        

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
        error_years.append((month, year))

      
  
    








  driver.implicitly_wait(5)
  driver.close()

  #com = Company(company_name,ticker,exchange,share_price,shares_offered,dollar_value_of_shares,date_of_priced, href)

  column_names = ['company_name', 'ticker', 'exchange','share_price', 'shares_offered', 'dollar_value_of_shares', 'date_of_priced', 'href']
  writeToCsvPartOne(data, column_names)
  print(error_years)
  print(len(error_years))
  writeToCsvErrorYears(error_years, ["month", "year"])










#edgar-online processing
#link: https://datafied.api.edgar-online.com/v2/corefinancials/ann?primarysymbols=ikt&appkey=22bc809f268182c5196b611916b5c525


def merge_all_csv_panda():
  import glob
  import os
  import pandas as pd   
  df = pd.concat(map(pd.read_csv, glob.glob(os.path.join('', "data_files/companies*.csv"))), ignore_index=True)
  key = df.keys()[7]
  print(key)
  df[key] = pd.to_datetime(df[key])
  df = df.sort_values(by=key)
  df = df.drop_duplicates(subset=[df.keys()[2]])
   #drop the comp and karo from 4/2021
  df = df.reset_index(drop=True)
  df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
  df.to_csv('part_1_data/companies_years_2009_2020_p1_v1_total.csv', sep=',', na_rep='None')
  df = pandas.read_csv('part_1_data/companies_years_2009_2020_p1_v1_total.csv')

  df = df.drop([1558,1559,1560])
  df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

  df.to_csv('part_1_data/companies_years_2009_2020_p1_v1_total.csv',sep=',', na_rep='None')


  

if __name__ == "__main__":
  #runErrorYears()
  merge_all_csv_panda()