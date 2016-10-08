# hamster-bill

A small Python 3 wrapper for creating monthly bills from your [hamster-indicator](https://apps.ubuntu.com/cat/applications/precise/hamster-indicator/) time tracking database in HTML/PDF. Allows you to define your own template and per-customer variables (like hourly rate). 

## Features

- collects all time records for a given month with the same tag (=company name)
- calculates total hours, tax amount, grand total
- renders first page with your logo, address, customer address etc.
- auto-generates invoice number, due date 
- renders activity table with all log records on following pages
- formats numbers as your locale

Tested under Ubuntu 16.04 with hamster-applet v. 2.91 / hamster-indicator v. 0.1+037dd2e-0ubuntu, WeasyPrint 0.31 and SQLAlchemy 1.1.0

## Installation: 

    git clone https://github.com/belugame/hamster-bill.git
    pip install WeasyPrint sqlalchemy
    cd hamster-bill


## Usage:

- edit `config.py` to adjust at least your database path, output folder and one customer definition.

- for generating the September 2016 bill for all records tagged "CompanyA" you would call it like:
```
./bill 2016-9 CompanyA

2016-09-05 08:00:00 - 2016-09-05 08:32:00  feature XY
2016-09-06 08:00:00 - 2016-09-06 08:30:00  upgrade server
2016-09-07 08:00:00 - 2016-09-07 08:30:00  email template
Total: 1.53 hours in 9/2016
Bill saved to: /home/foo/C201609.pdf
```

The original sample bill template was friendly provided by the [HTML PDF API](https://htmlpdfapi.com/)
