''' rev_tracker_lib_extracting contains routines 
that allow us to extract relevant data from contract pdfs'''


import cv2
import pytesseract
from pdf2image import convert_from_path
import os


def pdf_to_text(pdf):
    """
    Returns a list where each element corresponds to a line of text from a pdf file. 
    This method achieves this goal by first converting the pdf file into a set of image files, 
    and then passing this set through an OCR model to extract the text in those images into a string. 
    The reason behind having this middle step of converting a pdf into a set of images is that 
    we are working with signed pdfs, and computers can't directly access the text in a pdf once it's signed. 
    """
    
    # convert a pdf file into a set of image files and save them
    images = convert_from_path(pdf)
    for i in range(len(images)):
        images[i].save(str(i) + pdf[:len(pdf)-4], 'JPEG')
    
    # extract text from this set of images into a string 
    text = ''
    for imagefile in os.listdir():
        if imagefile.endswith(pdf[:len(pdf)-4]):
            img = cv2.imread(imagefile)
            partial = pytesseract.image_to_string(img)
            text += f"{partial} \n\n"
    
    # convert the string into a list of lines of string so that we can later analyze the text in the contract line-by-line
    linelist = text.splitlines()
    
    # return that list of text lines
    return linelist

def extract_name(linelist):
    """
    Returns a string containing the name of the client with whom the contract was signed. 
    This method is not a very general one; that is, there is no guarantee that
    it will work on contracts used by other companies that may be written in a differnt format.
    This method is tailored to my company's sales contracts, wherein our company's name appears
    in all capitalized letters only once in the contract and the remaining string in the line
    denotes the name of the client with whom the contract was signed.
    """

    # find the name of the client with whom the contract was signed
    # by first looking for the line where 'MARQ VISION INC.' appears
    # and then capturing the remaining string in that line
    for line in linelist:
        if line.find('MARQ VISION INC.') != -1:
            name = line[17:]
            break

    # return that string
    return name

def extract_product(linelist):
    """
    Returns a string containing the name of the product/service to which the client is agreeing to subscribe.
    This method is not a very general one; that is, there is no guarantee that
    it will work on contracts used by other companies that may be written in a differnt format.
    This method is tailored to the sales contracts of my company (which currently has two products), 
    wherein if the name of a product appears in the contract at all, it necessarily follows that
    the contract is for the product picked out by that name.     
    """
    
    # find the name of the relevant product/service by looking for a string that matches the product/service name
    for line in linelist:
        if line.find('MARQ CONTENTS') != -1:
            product = 'MARQ CONTENTS'
            break
        elif line.find('MARQ COMMERCE') != -1:
            product = 'MARQ COMMERCE'
            break
    
    # return that string
    return product

def extract_fee(linelist):
    """
    Returns an integer representing the monthly subscription fee the client is agreeing to pay. 
    This method is not a very general one; that is, there is no guarantee that
    it will work on contracts used by other companies that may be written in a differnt format.
    This method is tailored to my company's sales contracts, wherein the string 'USD' appears 
    only once in the entire contract, and the string of numbers that appears in the line in which
    'USD' appears denotes the monthly subscription fees.     
    """

    # find the line in which 'USD' appears
    for line in linelist:
        if line.find('USD') != -1:
            fee_line = line
            break

    # extract the string of numbers in that line
    fee_str = ''
    for character in fee_line:
        if character.isdigit() == True:
            fee_str += character

    # convert that string into an integer
    fee = int(fee_str)

    # return that integer
    return fee

def extract_start(linelist):
    """
    Returns a tuple of two strings, where each denotes the month and year in which the 
    client is agreeing to start its subscription, respectively. 
    This method is not a very general one; that is, there is no guarantee that
    it will work on contracts used by other companies that may be written in a differnt format.
    This method is tailored to my company's sales contracts, wherein the subscription starts
    when the client signs the contract, the dates on which the parties signed the contract
    appear in the same line, and the client writes the signed date in the format exemplified by
    the following: "January 14, 2022".   
    """

    # find the line that contains the string "Start Date:"
    for line in linelist:
        if line.find('Signed Date:') != -1:
            startdate_line = line
            break

    # find the index location of the second occurrence of that string in the line 
    # and cut the string at that index so we are left with only the string conveying the date info
    first = startdate_line.find('Signed Date:')
    second = startdate_line.find('Signed Date:', first+len('Signed Date:'))
    startdate_str = startdate_line[second+len('Signed Date:'):].strip(' ')

    # obtain a string of numbers representing the month in which the client is starting its subscription
    months = {'January':'01' , 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}
    for key in months:
        if startdate_str.find(key) != -1:
            start_month = months[key]
            break

    # obtain a string of numbers representing the year in which the client is starting its subscription,
    # with the assumpiton that no client is starting subscription in 2019 or ealier
    n = 2020
    while True:
        if  startdate_str.find(str(n)) != -1:
            index = startdate_str.find(str(n))
            start_year = startdate_str[index:index+len(str(n))]
            break
        else:
            n += 1

    # put those two strings into a tuple
    start = (start_month, start_year)

    # return that tuple
    return start

def extract_duration(linelist):
    """
    Returns an integer reprsenting the temporal length/duration of the contract. 
    This method is not a very general one; that is, there is no guarantee that
    it will work on contracts used by other companies that may be written in a differnt format.
    This method is tailored to my company's sales contracts, wherein the duration of the contract
    appears immediately before the string 'months from the Effective Date', in the same line.
    """
    
    # find the line in which the string "months from the Effective Date" appears
    # and cut the line at the indext where the string starts
    # so that we are left with a string indicating the duration of the contract
    for line in linelist:
        index = line.find('months from the Effective Date')
        if index != -1:
            duration_line = line[:index]
            break

    # extract from that string a substring of numbers representing the duration of the contract,
    # which is necessary because the string also contains a substring written in English
    # that represents the duration of the contract
    duration_str = ''
    for character in duration_line:
        if character.isdigit() == True:
            duration_str += character

    # convert that substring into an integer
    duration = int(duration_str)
    return duration

def extract_period(linelist):
    """
    Returns a list of two tuples that represent month-and-year of 
    the start of the subscription and the end of the subscription, respetively. 
    Each tuple consists of two strings that represent the month and the year, respectively. 
    This routine achieves its purpose by calling the extract_duration and extrat_start routines defined above. 
    Essentially, it adds the duration (in months) to the start month-year to find the end month-year.
    """

    # extract the duration of the contract
    duration = extract_duration(linelist)

    # extract the start month and start year of the contract
    start = extract_start(linelist)
    start_month, start_year = start 

    # use the duration, start month, and start year to get end month and end year
    if int(start_month) + duration - 1 < 13:
        end_month = str(int(start_month) + duration - 1)
        end_year = start_year
    else: 
        end_month = str(int(start_month) + duration - 1 - (12 * ((int(start_month) + duration) // 12)))
        end_year = str(int(start_year) + ((int(start_month) + duration) // 12))

    if len(end_month) < 2:
        end_month = '0' + end_month
    end = (end_month, end_year)
    
    # return list of start month-year tuple and end month-year tuple
    period = [start,end]
    return period

    
def extract_individual(pdf):
    """
    Returns a dictionary containing the relevant data extracted from a single contract pdf 
    (ie. client name, product/service name, subscription fee, and subscription period). 
    This routine achieves its purpose by calling the pdf_to_text, extract_name, extract_product, 
    extract_fee, and extract_period routines defined above. 
    """
    # extract text from contract pdf
    linelist = pdf_to_text(pdf)

    # extract client name 
    name = extract_name(linelist)

    # extract product/service name 
    product = extract_product(linelist)

    # extract subscription fee 
    fee = extract_fee(linelist)

    # extract the period during which the contract is effective
    period = extract_period(linelist)

    # put these data into a dictionary
    data_unpolished = {'name':name, 'product':product, 'fee':fee, 'period':period}
    
    # return that dictionary
    return data_unpolished

def extract():
    """
    Returns a list of dictionaries containing the relevant data extracted from every contract pdf.
    This routine runes the extract_individual routine defined above on all contracts and puts
    the resulting dictionaries into a list. 
    """

    # extract relevant data (into a dictionary) from all contract pdfs and
    # put those dictionaries into a list
    list_unpolished = []
    for contractfile in os.listdir():
        if contractfile.endswith(".pdf"):
            data_unpolished = extract_individual(contractfile)  
            list_unpolished.append(data_unpolished)
            print("Data extracted from one of " + data_unpolished['name'] + "\'s contracts for " + data_unpolished['product'])
            print(data_unpolished, "\n")

    # return that list
    return list_unpolished








