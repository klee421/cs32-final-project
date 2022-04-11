# convert contracts in pdf format into a client-by-client monthly subscription fee table
    # extract from contract pdfs the data required to build the table
        # convert contract pdfs into strings
            # convert contract pdfs to image files
            # convert the content of the image files into strings
        # extract from strings the data required to build the table
            # extract client names
            # extract monthly subscription fees
            # extract the month and year of the start of the subscription
            # extract the montha and year of the end of the subscription

    # use these data to build the table
        # build a list of dictionaries, where keys are the months and values are the subscription fees
        # convert this list of dictionaries into a csv file


import sys
from rev_tracker_lib import pdf_to_text, extract_name, extract_fee, extract_start, extract_duration, extract_period, extract_data


def main():
    if len(sys.argv) <= 1:
        sys.exit("need to input at least one contract in pdf")

    list_unpolished = []
    
    for contract in sys.argv[1:]:
        data_unpolished = extract_data(contract)  
        list_unpolished.append(data_unpolished)

    print(list_unpolished)

if __name__ == '__main__':
    main()

