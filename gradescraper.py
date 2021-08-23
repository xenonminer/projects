from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

driver.get("https://mystudent.fjuhsd.org/Parent/LoginParent.aspx")

email = driver.find_element_by_id('portalAccountUsername')
password = driver.find_element_by_id('portalAccountPassword')

email.send_keys("email") #your email here

next_button = driver.find_element_by_id('next')
next_button.click()

password.send_keys('password') #your password here

signin_button = driver.find_element_by_id('LoginButton')
signin_button.click()

driver.get("https://mystudent.fjuhsd.org/Parent/GradebookSummary.aspx")

soup = BeautifulSoup(driver.page_source, 'html.parser')

strings = soup.find_all(class_="Data al")
numbers = soup.find_all(class_="Data ac")

class_names = []
teachers = []
letter_grade = []
number_grades = []
for string in strings:
    string = string.get_text().strip() #get the raw text from each element in strings
    if string != "": #for strings with text
        if(len(string) < 3 and string[0].isupper()): #if the string is less than 3 chars and the first letter is uppercase
            letter_grade.append(string) # it's a letter grade
        elif(string.istitle() and '-' not in string): #if the string is a title (all words only have the first letter capitalized) and there are no hyphens)
            teachers.append(string) # it's a teacher
        elif(len(string) > 5): # if it's not the other two and the length of the string is greater than 5
            class_names.append(string) # it's a class

for num in numbers:
    if('span' in str(num)): #if there's span in the element (only number grades have span in them)
        num = num.span # num is equal to the span tag
    if(num.get('style') != "display:none;"): # if the style attribute of the span tag isn't "display:none;"
        num = num.get_text().strip() # get the innerHTML of the span
        if num != "" and len(num) > 2: # if the text is greater than 2 and isn't nothing
            if(num[:2].isnumeric()): # if the first two characters of the grade are numbers
                number_grades.append(num) # it's a number grade

assert len(class_names) == len(teachers) == len(letter_grade) == len(number_grades)

# iterate through all the lists at the same time and print the elements as it goes
for name, teacher, letter, number in zip(class_names, teachers, letter_grade, number_grades):
    if(letter == "A+" or number == '100.00'):
        code = '\u001b[32;1m'
    elif('A' in letter):
        code = '\u001b[32m'
    elif('B' in letter):
        code = '\u001b[34;1m'
    elif('C' in letter):
        code = '\u001b[33;1m'
    elif('D' in letter):
        code = '\u001b[31;1m'
    elif('F' in letter):
        code = '\u001b[31m'
    else:
        code = '\u001b[0m'
    print(f"\u001b[0m{name} ({teacher}) - {code}{number} \u001b[0m({code}{letter}\u001b[0m)")
