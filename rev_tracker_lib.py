import cv2
import pytesseract
from pdf2image import convert_from_path
import os

def pdf_to_text(pdf):
    images = convert_from_path(pdf)
    for i in range(len(images)):
        images[i].save(str(i) + pdf[:len(pdf)-4], 'JPEG')
    text = ''
    for imagefile in os.listdir(): #in the parenthesis, put the name of the folder within the FP folder where the images are located
        if imagefile.endswith(pdf[:len(pdf)-4]):
            img = cv2.imread(imagefile)
            partial = pytesseract.image_to_string(img)
            text += f"{partial} \n\n"
    return text

def extract_name(linelist):
    for line in linelist:
        if line.find('MARQ VISION INC.') != -1:
            name = line[17:]
            break
    return name

def extract_fee(linelist):
    for line in linelist:
        if line.find('USD') != -1:
            fee_line = line
            break

    fee_str = ''
    for character in fee_line:
        if character.isdigit() == True:
            fee_str += character

    fee = int(fee_str)
    return fee

def extract_start(linelist):
    # find the line that contains "Start Date:"
    for line in linelist:
        if line.find('Signed Date:') != -1:
            startdate_line = line
            break

    # find the index location of the second occurrence of that substring and cut the string at that index so we are left with only string conveying date info
    first = startdate_line.find('Signed Date:')
    second = startdate_line.find('Signed Date:', first+len('Signed Date:'))
    startdate_str = startdate_line[second+len('Signed Date:'):].strip(' ')

    # convert the date string into a tuple (start_month, start_year)
    # get the month
    months = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    for key in months:
        if startdate_str.find(key) != -1:
            start_month = months[key]
            break

    # get the year
    n = 2020
    while True:
        if  startdate_str.find(str(n)) != -1:
            index = startdate_str.find(str(n))
            start_year = int(startdate_str[index:index+len(str(n))])
            break
        else:
            n += 1

    start = (start_month, start_year)
    return start

def extract_duration(linelist):
    for line in linelist:
        index = line.find('months from the Effective Date')
        if index != -1:
            duration_line = line[:index]
            break

    duration_str = ''
    for character in duration_line:
        if character.isdigit() == True:
            duration_str += character

    duration = int(duration_str)
    return duration

def extract_period(linelist):
    duration = extract_duration(linelist)
    start = extract_start(linelist)
    start_month, start_year = start 
    if start_month + duration < 13:
        end_month = start_month + duration - 1
        end_year = start_year
    else: 
        end_month = start_month + duration - 1 - (12 * ((start_month + duration) // 12))
        end_year = start_year + ((start_month + duration) // 12) 

    end = (end_month, end_year)
    period = [start,end]
    return period

    
def extract_data(pdf):
    text = pdf_to_text(pdf)
    linelist = text.splitlines()
    name = extract_name(linelist)
    fee = extract_fee(linelist)
    period = extract_period(linelist)
    data = {'name':name, 'fee':fee, 'period':period}
    return data















# print(wordlist)

# for word in wordlist:
#     # if word == '(\“Marq\', \'Vision\”),':
#     if word == 'SERVICES':
#         print (word)



    # img = cv2.imread(images[i])
    # partial = pytesseract.image_to_string(img)
    # text += f"{partial} \n\n\n\n\n"
# img = cv2.imread('contract.pdf')
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# text = pytesseract.image_to_string(img)
# print(text)

