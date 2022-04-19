from rev_tracker_lib_extracting import pdf_to_text, extract_name, extract_product, extract_fee, extract_start, extract_duration, extract_period, extract_individual, extract
from rev_tracker_lib_polishing import get_integerized_date, get_date_range, build_keys, polish
from rev_tracker_lib_exporting import export


def main():
    # extract relevant data from contracts
    list_unpolished = extract()

    # polish the data so that it can be easily exported into a spreadsheet
    list_polished = polish(list_unpolished)
    
    # export the polished data into an excel workbook pre-coded to automatically run analytics on the revenue data being exported
    export(list_polished)

if __name__ == '__main__':
    main()

