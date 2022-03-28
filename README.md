# cs32-final-project
## Revenue Tracker Program for B2B SaaS Startups
### Overview
This program is intended to strealine the revenuement management process for B2B SaaS startups that have a subcription-based business model, thereby saving such companies' operations person a lot of time. 

### Motivation
The project is intended to address a pain point that I currently have at work. I am currently the Chief of Staff at a B2B SaaS startup called [MarqVision](https://marqvision.com) and part of my job involves keeping track of the revenues we are generating from each client that we collect as monthly subscription fees. But the way I am currently doing this work is quite inefficient. Whenever we sign with a new client, I open the signed contract and then manually input the subscription fees month by month in a spreadsheet by looking at the subscription fee and duration information on the contract. And whenever an existing client upgrades or downgrades its subscription plan, I open the sigend order form and then manually edit the subscription fees for the months to which the plan change applies. In order to save myself some time, I decided to build a program that can do this work for me. 

### Details
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

