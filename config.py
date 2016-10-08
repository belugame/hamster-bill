import textwrap

HAMSTER_DB = "sqlite:////home/foo/.local/share/hamster-applet/hamster.db"
BILL_TEMPLATE = "./template/index.html"
TIMEDELTA_DUE_DATE = 14  # amount of days from today until bill due
LOCALE = ""  # e.g. de_DE.utf8 or leave empty for system default
ACTIVITY_ROW_TEMPLATE = "<tr><td>$start</td><td>$end</td><td>$duration</td><td>$description</td></tr>"

CUSTOMER = {
    "__common__": {  # common attributes for all customer
        "hourly_rate": 10,
        "tax_rate": 19,
        "notice": textwrap.dedent("""Bank information:</br>
                                  John Doe</br>
                                  IBAN: DE203045766403457896633</br>
                                  BIC/SwiftCode: DGTADEFD431</br>
                                  Foo Bank</br>
                                  """),
    },

    "CompanyA": {  # customer specific details
        "name": "Company A Corp",
        "hourly_rate": 5,
        "output_folder": "/home/foo/bills/CompanyA/",
        "address_line1": "1337 Foo St",
        "address_line2": "Bar 344",
        "address_line3": "PDR of Baz",
        "description_short": "Development",
        "description_long": "Python backend coding + HTML templating",
    }

}
