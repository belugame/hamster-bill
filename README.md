# hamster-bill

A small Python 3 wrapper for creating monthly PDF bills and reports from your [hamster-indicator](https://projecthamster.wordpress.com/) time tracking database. Allows you to define your own template and per-customer variables (like hourly rate). 

[See sample pdf](/sample/C201609.pdf?raw=true "Sample bill")

Sample records:

![sample records](/sample/screenshot.jpg?raw=true)

Sample generated bill:
![sample pdf](/sample/bill.jpg?raw=true)


## Features

- collects all time records for a given month with the same tag (=company name)
- calculates total hours, tax amount, grand total
- renders first page with your logo, address, customer address etc.
- auto-generates invoice number, due date
- creates bar chart with time spent per activity
- renders activity table with all log records on following pages
- formats numbers as your locale
- generate bar charts: hours worked per month/day

Tested under Ubuntu 16.04 with hamster-applet v. 2.91 / hamster-indicator v. 0.1+037dd2e-0ubuntu, WeasyPrint 0.31 and SQLAlchemy 1.1.0

## Installation:

    git clone https://github.com/belugame/hamster-bill.git
    pip install WeasyPrint sqlalchemy
    cd hamster-bill
    cp config.py.sample config.py


## Usage:

- use hamster-indicator as usual, chose a common tag for all records you want to bill together.
- edit `config.py` to adjust at least your database path, output folder and one customer definition.
- for generating the September 2016 bill for all records tagged "CompanyA" you would call it like:
```
./bill 2016-9 CompanyA

2016-09-05 08:00:00 - 2016-09-05 08:32:00  feature XY
2016-09-06 08:00:00 - 2016-09-06 08:30:00  upgrade server
2016-09-07 08:00:00 - 2016-09-07 08:30:00  email template
Total: 1.53 hours in 9/2016
Bill saved to: /home/foo/C201609.pdf

# Daily hours worked for a customer

python3 report.py 2016-11 CustomerA

Total hours in 11/2016: 64.00
###############################################################################
                                                               0.06  2016-11-01
||                                                             0.44  2016-11-02
|||||||||||||||||||||||||||||||||||                            6.25  2016-11-03
||||||||||||||||||||||||||||||||||||||||||||                   7.81  2016-11-04
|||||                                                          0.97  2016-11-06
|||||||||||||||||||||||||||||||||||||||||||||                  7.93  2016-11-07
|||||||||||||||||||||||||||||||||||||||||||||||                8.28  2016-11-08
|||||||||||||||||||||||||||||                                  5.22  2016-11-09
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  10.52  2016-11-10
|||||||||||||||||||||||||||||||||||||||                        6.93  2016-11-11
||||||||||||||||||||||||||||||||||                             6.10  2016-11-12
||||                                                           0.75  2016-11-13
|||||||||||||||                                                2.75  2016-11-14

# Monthly hours worked for a customer

python3 report.py 2016 CompanyA

Total hours in 2016: 761.06
###############################################################################
|||||||||||||||||||||||||||||||||                              59.66  January  
|||||||||||||||||||||||||||||||                                56.27  February 
||||||||||||||||||||||||||||||||                               56.50  March    
||||||||||||||||||||||||||||||||||                             61.54  April    
||||||||||||||||||||||||||                                     46.43  May      
|||||||||||||||||||||||||||||||||||||||||||||||||              86.77  June     
||||||||||||||||||||||||||||||||||||||||||||||||               84.99  July     
|||||||||||||||||||||||                                        41.96  August   
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||   105.91  September
||||||||||||||||||||||||||||||||||||||||||||||||||||||         97.05  October  
||||||||||||||||||||||||||||||||||||                           64.00  November

```

The original sample bill template was friendly provided by the [HTML PDF API](https://htmlpdfapi.com/)
