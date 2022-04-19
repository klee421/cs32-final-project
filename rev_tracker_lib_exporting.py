''' rev_tracker_lib_exporting contains a routine
that allows us to export the polished data into a spreadsheet'''

import pandas as pd
import xlwings as xw

def export(list_polished):
    """
    Exports into an existing Excel workbook the polished list of dictionaries 
    carrying monthly subscription fees information for each client-product pair. 
    The Excel workbook is pre-coded such that when data gets exported to a certain 
    sheet of the workbook, analytics are automatically executed on other sheets of the
    same workbook. 
    """

    # convert the polished data to a pandas dataframe
    df = pd.DataFrame(list_polished)
    print("Based on these extracted contract data, the final revenue table in excel should look like: " + "\n", df)

    # load workbook to which the dataframe needs to be exported 
    app = xw.App(visible=False)
    wb = xw.Book('Revenue Analytics.xlsx')  
    ws = wb.sheets['Revenue by Client']

    # update the workbook with the dataframe
    ws.range('A1').options(index=False).value = df

    #close workbook
    wb.save()
    wb.close()
    app.quit()

