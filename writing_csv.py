import csv
with open ('emp.csv', mode = 'w') as file:

    emp_write= csv.writer(file , delimiter=',')

    emp_write.writerow(['me','you','they'])
    emp_write.writerow(['me','you','they'])