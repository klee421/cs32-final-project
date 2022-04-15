# cs32-final-project
## Revenue Tracker Program for B2B SaaS Startups
### Overview
This program is intended to strealine the revenuement management process for B2B SaaS startups that have a subcription-based business model, thereby saving such companies' operations person a lot of time. 

### Motivation
The project is intended to address a pain point that I currently have at work. I am currently the Chief of Staff at a B2B SaaS startup called [MarqVision](https://marqvision.com) and part of my job involves keeping track of the revenues we are generating from each client that we collect as monthly subscription fees. But the way I am currently doing this work is quite inefficient. Whenever we sign with a new client, I open the signed contract and then manually input the subscription fees month by month in a spreadsheet by looking at the subscription fee and duration information on the contract. And whenever an existing client upgrades or downgrades its subscription plan, I open the sigend order form and then manually edit the subscription fees for the months to which the plan change applies. In order to save myself some time, I decided to build a program that can do this work for me. 

### Description of the Project with a Specific Example
Basically, I want my program to output a CSV file that looks something like Table 1 below after being inputted with sales contracts and order forms in PDF files. For example, the program would output precisely the table below in CSV file if inputted with the following pdf files:

1. A sales contract signed by Client A saying that it will be subscribed to Product X for 1 year starting January 2022, paying a monthly subscription fee of $2000
2. An order form signed by Client A saying that it wants to get a plan upgrade for an additional $1000 starting February 2022
3. A sales contract signed by Client B saying that it will be subscribed to Product Y for 1 year starting February 2022, paying a monthly subscription fee of $5000
4. An order from signed by Client B saying that it wants to get a plan downgrade and reduce its subscription fee by $1000 starting April 2022
5. A sales contract signed by Client C saying that it will be subscribed to Product X for 6 months starting March 2022, paying a monthly subscription fee of $6000

#### Table 1. 

| Client | Product | Jan 22 | Feb 22 | Mar 22 | Apr 22 | May 22 | Jun 22 | Jul 22 | Aug 22 | Sep 22 | Oct 22 | Nov 22 | Dec 22 | Jan 23 |
|--------|---------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| A      | X       | 2000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | N/A    | 
| B      | Y       | N/A    | 5000   | 5000   | 4000   | 4000   | 4000   | 4000   | 4000   | 4000   | 4000   | 4000   | 4000   | 4000   | 
| C      | X       | N/A    | N/A    | 6000   | 6000   | 6000   | 6000   | 6000   | 6000   | N/A    | N/A    | N/A    | N/A    | N/A    | 

### Problem Decomposition


#### Convert contracts (in pdf) into a client-by-client monthly subscription fee table (in csv)
    # 1. extract from contract pdfs the data required to build the table
        # 1-1. convert contract pdfs into strings
            # 1-1-1. convert contract pdfs to image files (this step is required because you can't directly access text from a pdf once it's signed, meaning we have to first turn the pdf into a set of image files and then run it through an OCR method in order to access thet text) 
            # 1-1-2. convert the content of the image files into strings
        # 1-2. extract the data required to build the table from these strings
            # 1-2-1. extract names
            # 1-2-2. extract monthly subscription fees
            # 1-2-3. extract the subcriptions periods
    # 2. use these data to build the table
        # 2-1. using the extracted data, build a list of dictionaries, where for each dictionary object, the first two keys are "Client" and "Product respectively, and the remaining keys are the month-year tuples that need to be present as columns of the final csv output
        # 2-2. convert this list of dictionaries into a csv file

### Required Library Installation

In order to convert pdf files into sets of image files, I will use the 'pdf2image' library
In order to do OCR on image files, I will use the "OpenCV" and the "Tesseract" libraries
In order to easily iterate through files in a folder, I will use the "Os" libary

### Word Done

As indicated above, I decomposed the problem at a high-level into two sub-problems: (1) extract from contract pdfs the data required to build the table, and (2) use these data to build the table. So far, I've written scripts that does (1). The "rev_tracker.py" is the main script and the "rev_tracker_lib.py" has the functions that the main script imports. More precisely, given the following three (fake) contracts (I maded and signed for the purposes of this project) in pdf as input,

[Harvard.pdf](https://github.com/klee421/cs32-final-project/files/8460724/Harvard.pdf)
[Yale.pdf](https://github.com/klee421/cs32-final-project/files/8460726/Yale.pdf)
[Princeton.pdf](https://github.com/klee421/cs32-final-project/files/8460728/Princeton.pdf)

the script outputs a list of dictionary that looks like: 
[
  {'name': 'HARVARD', 'fee': 3000, 'period': [(12, 2020), (1, 2022)]}, 
  {'name': 'YALE', 'fee': 4000, 'period': [(1, 2021), (6, 2021)]}, 
  {'name': 'PRINCETON', 'fee': 5000, 'period': [(2, 2021), (11, 2021)]}
]

I solved the second (and last) high-level sub-problem as well. That is, given the list of dictionaries as shown above, my script produces a list of dictionaries that looks like:

[
  {'name': 'HARVARD', 'Dec 2020': 3000, 'Jan 2021': 3000, 'Feb 2021': 3000,..., 'Dec 2021': 3000, 'Jan 2022': 3000}, 
  {'name': 'YALE', 'Dec 2020': 0, 'Jan 2021': 4000, 'Feb 2021': 4000,..., 'Jun 2021': 4000, 'Jul 2021': 0, ..., 'Dec 2021': 0, 'Jan 2022': 0}, 
  {'name': 'PRINCETON', 'Dec 2020': 0, 'Jan 2021': 0, 'Feb 2021': 5000,..., 'Nov 2021': 5000, 'Dec 2021': 5000, 'Jan 2022': 0}, 
]

and then, converts this list of dictionaries into a table that looks like:

| Name     | Dec 20 | Jan 21 | Feb 21 | Mar 21 | Apr 21 | May 21 | Jun 21 | Jul 21 | Aug 21 | Sep 21 | Oct 21 | Nov 21 | Dec 21 | Jan 22 |
|----------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| HARVARD  | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   |
| YALE     | N/A    | 4000   | 4000   | 4000   | 4000   | 4000   | 4000   | N/A    | N/A    | N/A    | N/A    | N/A    | N/A    | N/A    |
| PRINCETON| N/A    | N/A    | 5000   | 5000   | 5000   | 5000   | 5000   | 5000   | 5000   | 5000   | 5000   | 5000   | 5000   | N/A    |

and then saves an excel file that contains this table

I updated the scrip such that it can handle other kinds of contracts (eg. renewal contracts and order forms). So now, when I input the following set of contracts:

[Harvard_orderform.pdf](https://github.com/klee421/cs32-final-project/files/8494211/Harvard_orderform.pdf)
[Harvard_renewal.pdf](https://github.com/klee421/cs32-final-project/files/8494212/Harvard_renewal.pdf)
[Harvard.pdf](https://github.com/klee421/cs32-final-project/files/8494213/Harvard.pdf)
[Princeton_orderform.pdf](https://github.com/klee421/cs32-final-project/files/8494216/Princeton_orderform.pdf)
[Princeton.pdf](https://github.com/klee421/cs32-final-project/files/8494217/Princeton.pdf)
[Yale_renewal.pdf](https://github.com/klee421/cs32-final-project/files/8494218/Yale_renewal.pdf)
[Yale.pdf](https://github.com/klee421/cs32-final-project/files/8494219/Yale.pdf)

my script outputs this spreadsheet:
[output.xlsx](https://github.com/klee421/cs32-final-project/files/8494224/output.xlsx)


### Work To Be Done

FIXME:
1. extracting client name from order forms is kind of weird

#### Next Step
1. edit the scrip so that it can handle sales contracts for other product lines 


#### Next Next Step
0. allow the user to input an existing excel spreadsheet and contracts so that the user doesn't have to update all previous contracts everytime she wants to use the program; data should be extrated from the contracts and the spreadsheet should be updated accordingly
1. allow user to input lots of contract pdfs easily by accepting a zip file of contracts or asking the program to parse through an entire folder of contract pdfs (as of now, the user has to type in the name of every contract she wants to process in the command line)
2. instead of creating a new excel file, import the table into a tab of an existing excel file so that I can automatically run the analytics on the excel spreadsheet (without having to copy the data to the hard-coded cells of the existing spreadsheet)

### Limitations
I've completed the part where I extract data from contracts in pdf. But my script would work only for contracts that have a particular format. It's not generalizable to to all kinds of sales contracts that other companies could use. Not sure how I can overcome this limitation without natural language processing. 
