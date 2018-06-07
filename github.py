import os
import time
 
os.chdir('/home/odoo/Downloads/NitroShare/coomon_reports_yasir/')
os.system('git init')
os.system('git remote add origin https://github.com/khyasir/Reports.git')
os.system('git add *')
os.system('git status')
os.system('git commit -m "Odoo 10 SQL report"')
os.system('git push origin master')