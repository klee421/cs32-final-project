<h3 align="center">Revenue Tracker Program for B2B SaaS Startups </h3>

  <p align="center">
    This program is intended to strealine the revenuement management process for B2B SaaS startups that have a subcription-based business model, thereby saving such companies' operations person a lot of time. 

</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#how-to-use">How to Use</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

### The Why
The project is intended to address a pain point that I currently have at work. I am currently the Chief of Staff at a B2B SaaS startup called [MarqVision](https://marqvision.com) and part of my job involves keeping track of the revenues we are generating from each client that we collect as monthly subscription fees. But the way I am currently doing this work is quite inefficient. Whenever we sign with a new client, I open the signed contract and then manually input the subscription fees month by month in a spreadsheet by looking at the subscription fee and duration information on the contract. And whenever an existing client upgrades its subscription plan, I open the sigend order form and then manually edit the subscription fees for the months to which the plan change applies. In order to save myself some time, I decided to build a program that can do this work for me, automatically. 

### The What

For example, I want my program to export into an existing excel spreadsheet a table that looks something like Table 1 below, if inputted with sales contracts and order forms in PDF files as indicated below. The excel workbook of which this spreadsheet is a part is pre-coded such that when data gets exported to the spreadsheet, certain revenue analytics are automatically executed on other sheets of the workbook. This is why I am exporting the table into an existing spreadsheet, as opposed to creating a new one. 

1. A sales contract signed by Client A saying that it will be subscribed to Product X for 1 year starting January 2022, paying a monthly subscription fee of $2000
2. An order form signed by Client A saying that it wants to get a plan upgrade for Product X for an additional $1000 starting February 2022
3. A sales contract signed by Client B saying that it will be subscribed to Product Y for 1 year starting February 2022, paying a monthly subscription fee of $5000
4. An order from signed by Client B saying that it wants to get a plan upgrade for Product Y for an additional $5000 starting April 2022
5. A sales contract signed by Client A saying that it will be subscribed to Product Y for 6 months starting March 2022, paying a monthly subscription fee of $6000
6. A sales contract signed by Client A saying that it will be subscribed to Product Y for 5 months starting September 2022, paying a monthly subscription fee of $4000

#### Table 1. 

| Client | Product | Jan 22 | Feb 22 | Mar 22 | Apr 22 | May 22 | Jun 22 | Jul 22 | Aug 22 | Sep 22 | Oct 22 | Nov 22 | Dec 22 | Jan 23 |
|--------|---------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| A      | X       | 2000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 3000   | 0      | 
| B      | Y       |        | 5000   | 5000   | 5500   | 5500   | 5500   | 5500   | 5500   | 5500   | 5500   | 5500   | 5500   | 5500   | 
| A      | Y       |        |        | 6000   | 6000   | 6000   | 6000   | 6000   | 6000   | 4000   | 4000   | 4000   | 4000   | 4000   | 


### The How

The problem can be decomposed at a high-level as follows:

1. extract from contract pdfs the data required to build the table
2. polish the data so that it can be easily exported into a spreadsheet
3. export the polished data into a sheet of an existing excel workbook

Since the first sub-problem is the most difficult to tackle, provided below is how this sub-problem can be further decomposed:

1. convert contract pdfs to image files 
2. convert the content of the image files into strings
3. extract the data required to build the table from these strings

You may be wondering why I have the extra step of converting pdfs into sets of image files before extracting the text of the contracts into strings. This extra step is required because you can't directly access text from a pdf once it's signed. Therefore, we need to turn those pdfs into sets of image files and then pass those images through an OCR model to extract the text we need.


<!-- GETTING STARTED -->
## Getting Started


The following packages are required to run this program:

1. pdf2image
2. cv2
3. pytesseract
5. os
6. sys
7. pandas
8. xlwings


<!-- HOW TO USE -->
## How to Use

Provided below are the steps you need to take to properly use the program:

1. Install any package among those listed above that you don't already have. 
2. Download all of the files in the main branch to a new folder in your local machine. Make sure to keep all the files in the same folder. Besides the python scripts, there should be 18 pdf files and 1 excel file in this folder. These 18 pdf files are the some fake contracts I signed to use as sample inputs to this program. The excel file is the pre-coded workbook to which our data needs to be exported. 
3. Open this folder in Visual Studio Code
4. Execute the script "rev_tracker.py" in the terminal

The program should export the following table into the sheet "Revenue by Client" in the workbook "Revenue Analytics"

<img width="1250" alt="image" src="https://user-images.githubusercontent.com/102482222/164077175-fd39e04f-2b00-41a4-ba7a-2fbffa2aef59.png">



<!-- CONTACT -->
## Contact

Ki Kyung (Kik) Lee - klee@jd22.law.harvard.edu, kik.lee@marqvision.com

Project Link: [https://github.com/klee421/cs32-final-project.git](https://github.com/klee421/cs32-final-project.git)






