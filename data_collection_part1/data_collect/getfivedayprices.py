


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
import util

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-ssl-errors')
# options.add_argument('--ignore-certificate-errors-spki-list')
# driver = webdriver.Chrome(options= options ,executable_path=r"C:\Users\jchen\Documents\chromedriver\chromedriver.exe")
# driver.implicitly_wait(10)
#https://sec-api.io/docs#query-financial-statementss
from selenium.webdriver.firefox.options import Options
options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r"C:\Users\jchen\Documents\firefoxdriver\geckodriver.exe", options=options)
driver.implicitly_wait(15)
error_companies = []
error_index = []
value_error_index = []
value_error_com = []
less_than_10_employees = []
less_than_10_employees_index = []

static_url = 'https://www.marketwatch.com/investing/stock/'
end_url = '/download-data?startDate='
end_date_url = '&endDate='

from urllib.request import urlopen
"""
[<td class="overflow__cell fixed--column">
<div class="cell__content fixed--cell u-secondary">04/15/2009</div>
<div class="cell__content u-secondary">04/15/2009</div>
</td>, 
<td class="overflow__cell"><div class="cell__content">$10.5000</div></td>,
 <td class="overflow__cell"><div class="cell__content">$11.6800</div></td>, 
 <td class="overflow__cell"><div class="cell__content">$9.7500</div></td>,
  <td class="overflow__cell"><div class="cell__content">$11.1000</div></td>, 
  <td class="overflow__cell"><div class="cell__content">7,324,263</div></td>]
"""

def price_parser_helper(url, start_date, end_date, index):
  try:
    
    driver.get(url)
    if index == 0 :
      try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'scrim-creative')))
        driver.implicitly_wait(5)
      except:
        pass
      try:
        ad = driver.find_element_by_xpath("//*[@id='cx-scrim-overlay']")
        driver.execute_script("arguments[0].setAttribute('visibility','hidden');", ad)
        driver.execute_script("arguments[0].setAttribute('display','none');", ad)

        ad = driver.find_element_by_class_name('mw-paywall-scrim')
        driver.execute_script("arguments[0].setAttribute('visibility','hidden');", ad)
        driver.execute_script("arguments[0].setAttribute('display','none');", ad)
      except:
        pass

      try:
        close_btn = driver.find_element_by_xpath("/html/body/footer/div[2]/div/div/div[1]/img")
        close_btn.click()
      except:
        pass



    in_s = driver.find_element_by_name('startdate')
    in_s.clear()
    in_s.send_keys(start_date)
    try:
      WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[6]/div/mw-downloaddata/form/div/div[2]/div[1]/div/div/div/footer/a[3]')))
      close_in_s = driver.find_element_by_xpath('/html/body/div[4]/div[6]/div/mw-downloaddata/form/div/div[2]/div[1]/div/div/div/footer/a[3]')
      close_in_s.click()
    except:
      pass
    
    en_s=driver.find_element_by_xpath('/html/body/div[4]/div[6]/div/mw-downloaddata/form/div/div[2]/div[2]/input')
    en_s.clear()
    en_s.send_keys(end_date)

    try:
      WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[6]/div/mw-downloaddata/form/div/div[2]/div[2]/div/div/div/footer/a[3]')))

      close_en_s = driver.find_element_by_xpath('/html/body/div[4]/div[6]/div/mw-downloaddata/form/div/div[2]/div[2]/div/div/div/footer/a[3]')
      close_en_s.click()
    except:
      pass

    update = driver.find_element_by_xpath('/html/body/div[4]/div[6]/div/mw-downloaddata/form/div/button')
    update.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[6]/div/div/mw-tabs/div[2]/div[1]/mw-downloaddata/div/div[1]/table')))
    table = driver.find_element_by_xpath('/html/body/div[4]/div[6]/div/div/mw-tabs/div[2]/div[1]/mw-downloaddata/div/div[1]/table')

    elementHTML = driver.execute_script("return arguments[0].outerHTML;", table)
    table_bs = BeautifulSoup(elementHTML, 'html.parser')
    table_body = table_bs.find('tbody')
    rows = table_body.find_all('tr')
    price_list = []
    for i in reversed(range(len(rows))):
      try:
        tds = rows[i].find_all('td')
        end_day_price = tds[4].getText().strip()
        price_list.append(end_day_price)
        print(end_day_price)
        if (len(rows)-i-1 == 5):
          return price_list
      except:
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
        return None

    return price_list
        

    # print(rows)
    # print(table_bs.prettify())



  except:
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
      return None


def run_part4_collect(file_name):
  df = util.readFromCsv(file_name)
 

  ticker_key = df.keys()[2]
  index_key = df.keys()[0]
  companies_key = df.keys()[1]

  date_key = df.keys()[7]
  df[date_key] = pandas.to_datetime(df[date_key])
  df['1'] = 0
  df["2"] = 0
  df['3'] = 0
  df['4'] = 0
  df['5'] = 0

  error_companies = []
  error_index = []


  for index, row in df.iterrows():
    print(row[date_key])
    start_date = row[date_key].strftime('%m/%d/%Y')
    print(start_date)
    end_date = row[date_key] + pandas.DateOffset(days=10)
    end_date = end_date.strftime('%m/%d/%Y')
    print(end_date)
    print(row[date_key])

    ticker_symbol = row[ticker_key]
    print("Ticker : " + str(ticker_symbol))
    url = static_url+ticker_symbol+end_url+start_date+end_date_url+end_date
    try:
      # list of tuples
      price_list = price_parser_helper(url, start_date, end_date, index)
      print(price_list)
      df.loc[index, '1'] = price_list[0]
      df.loc[index, '2'] = price_list[1]
      df.loc[index, '3'] = price_list[2]
      df.loc[index, '4'] = price_list[3]
      df.loc[index, '5'] = price_list[4]

      df = df.reset_index(drop=True)
      df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
      df.to_csv('part_4_data/companies_years_2009_2020_p4_v1_total.csv', sep=',', na_rep='Nane')
      
    
    except:
      error_companies.append(ticker_symbol)
      error_index.append(index)
      continue

  util.writeToCsv(error_companies,['company_name'], 'companies_error_names_part4_v1.csv')
  util.writeToCsv(error_index,['index'], 'companies_error_index_part4_v1.csv')




  return


if __name__ == "__main__":
  file_name = "part_3_data\companies_years_2009_2020_p3_v1_total.csv"
  run_part4_collect(file_name)