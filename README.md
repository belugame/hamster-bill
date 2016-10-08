# hamster-bill

A small Python 3 wrapper for creating monthly bills from your [hamster-indicator](https://apps.ubuntu.com/cat/applications/precise/hamster-indicator/) time tracking database in HTML/PDF. Allows you to define your own template and per-customer variables (like hourly rate).

Tested under Ubuntu 16.04 with WeasyPrint 0.31 and SQLAlchemy 1.1.0

## Installation: 

    git clone https://github.com/belugame/hamster-bill.git
    pip install WeasyPrint sqlalchemy
    cd hamster-bill


## Usage:

- edit config.py to adjust at least your database path, output folder and one customer definition.

- for a generating the September 2016 bill for all records tagged "CompanyA" you would call it like:

    ./bill 2016-9 CompanyA

    2016-09-05 08:00:00 - 2016-09-05 08:32:00  feature XY
    2016-09-06 08:00:00 - 2016-09-06 08:30:00  upgrade server
    2016-09-07 08:00:00 - 2016-09-07 08:30:00  email template
    Total: 1.53 hours in 9/2016
    Bill saved to: /home/foo/C201609.pdf


The sample bill template is based on and friendly provided by [HTML PDF API](https://htmlpdfapi.com/)
