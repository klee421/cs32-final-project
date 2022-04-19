''' rev_tracker_lib_polishing contains routines 
that allow us to polish the extracted data so that
they can be easily exported into a spreadsheet'''

def get_integerized_date(t):
    """
    Returns an integer denoting month-and-year. For example, the tuple
    ("06","2021") is passed through this routine, what comes out is
    the integer 202106. The purpose of this routine is to make it 
    easier to numerically compare two dates and figure our which is earlier.
    """
    return int(t[1] + t[0])

def get_date_range (list_unpolished):
    """
    Returns a tuple of strings where the first string represents the very first month-year
    in which subscription revenues started to be generated, and the second string represents
    the very last month-year for which there is any subscrition revenues, based on all signed contracts.
    Essentially, the purpose of this routine is to identify the range of month-year's that we need
    as the columns of the spreadsheet we want to produce.
    """
    # build a list of month-year's denoting the start of contracts and 
    # a list of month-year's denoting the end of contracts
    startdate_list = []
    enddate_list = []
    for client in list_unpolished:
        startdate = client['period'][0]
        enddate = client['period'][1]
        startdate_list.append(startdate)
        enddate_list.append(enddate)  

    # sort each list in chronological order   
    startdate_list_sorted = sorted(startdate_list, key=get_integerized_date)
    enddate_list_sorted = sorted(enddate_list, key=get_integerized_date)
    
    # identify earliest start month-year and the latest end month-year and put them into a tuple
    start_of_range = startdate_list_sorted[0]
    end_of_range = enddate_list_sorted[-1]  
    date_range = (start_of_range,end_of_range)
    
    # return that tuple
    return date_range

def build_keys(list_unpolished):
    """
    Returns a list of strings that will serve as the keys to the polished dictionary we will build 
    for every client. In other words, items in this list will eventually be the columns of 
    the spreadsheet we want to produce. This routine achieves its purpose by calling the
    get_date_range routine defined above.
    """

    # identify the range of month-year's that need to be present as a column head the final spreadsheet, 
    # or equivalently, as a key to the polished dictionary we need to build in order to produce the final spreadsheet
    date_range = get_date_range(list_unpolished)
    
    # build a list that starts with the strings "Client Name" and "Product Line", followed by
    # strings representing all month-year's within the identifed dated range
    keys = ['Client Name', 'Product Line', date_range[0][0] + '/' + date_range[0][1]]
    current_month = date_range[0][0]
    current_year = date_range[0][1]
    while True:
        if int(current_month) == int(date_range[1][0]) and int(current_year) == int(date_range[1][1]):
            break
        else:
            if int(current_month) < 12:
                new_month = int(current_month) + 1
                current_month = str(new_month)
            else:
                new_month = int(current_month) - 11
                current_month = str(new_month)
                new_year = int(current_year) + 1
                current_year = str(new_year)
            if len(current_month) == 1:
                current_month = '0' + current_month
            keys.append(current_month + '/' + current_year)
    
    # return that list
    return keys

def polish(list_unpolished):
    """
    Returns a chronologically sorted list of dicionaries that is polished in a way that renders it easy to be 
    converted into a dataframe that can be easily exported into a excel workbook on which some pre-coded analytics 
    will automatically run. Each dictionary in this list represents the total subscription fees paid by 
    a client for a specific product/service. In other words, for each client-product pair, the information found in
    the initial sales contract, in any order form particular to that client-product pair, 
    and in any renewal contracts particular to that client-product pair are "merged" to produce
    one dictionary. By calling the build_keys routine defined above, this routine builds a list of dictionaries, 
    where each dictionary looks like the following: {
    "Client Name" : string representing name of client, 
    "Product Line": string representing name of product/service, 
    string reprenting the first month-year of subscription: subscription fee for that month,
    string reprenting the second month-year of subscription: subscription fee for that month, 
    .
    .
    .
    string reprenting the last month-year of subscription: subscription fee for that month
    }
    """

    # create the keys for the dictionaries we want to create
    keys = build_keys(list_unpolished)

    # initiate the list of dictionaries we are going to build 
    list_polished_unsorted = []

    # build a dictionary for each client-product pair and put those dictionaries into the list initiated above
    for data_unpolished in list_unpolished:
        already_exists = False
        for data_polished in list_polished_unsorted:
            if data_polished['Client Name'] == data_unpolished['name'] and data_polished['Product Line'] == data_unpolished['product']:
                already_exists = True
                dict_to_be_updated = data_polished
                break
        if already_exists == True:
            for date in keys[2:]:
                if int(date[3:]+date[:2]) >= int(data_unpolished['period'][0][1] + data_unpolished['period'][0][0]):
                    if int(date[3:]+date[:2]) <= int(data_unpolished['period'][1][1] + data_unpolished['period'][1][0]):
                        dict_to_be_updated[date] += data_unpolished['fee']
        else:      
            data_polished = dict.fromkeys(keys, 0)
            data_polished['Client Name'] = data_unpolished['name']
            data_polished['Product Line'] = data_unpolished['product']
            for date in keys[2:]:
                if int(date[3:]+date[:2]) >= int(data_unpolished['period'][0][1] + data_unpolished['period'][0][0]):
                    if int(date[3:]+date[:2]) <= int(data_unpolished['period'][1][1] + data_unpolished['period'][1][0]):
                        data_polished[date] = data_unpolished['fee']
            list_polished_unsorted.append(data_polished)

    # sort this list of dictionaries in chronological order
    list_polished = []
    for date in keys[2:]:
        for data_polished in list_polished_unsorted:
            if data_polished[date] != 0:
                list_polished.append(data_polished)
                list_polished_unsorted.remove(data_polished)

    # replace the integer 0 with an empty string during the months before the start of the intitial subscription;
    # that is, if a client subscribes to a particular product/service starting in Jan 2021 but our date_range 
    # starts in Jun 2020, then for each key from "06/2020" to "12/2020", the corresponding value becomes an
    # empty string, instead of a zero; which is an important setup for the revenue analytics that will be run
    # on the excel workbook to which this data will eventually be exported
    for data_polished in list_polished:
        for date in keys[2:]:
            if data_polished[date] == 0:
                data_polished[date] = ''
            else:
                break

    # return that list
    return list_polished
