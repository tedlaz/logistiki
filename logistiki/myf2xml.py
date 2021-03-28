txml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n<packages>\n  '
    '<package actor_afm="{afm}" month="{month}" year="{year}"'
    ' branch="{branch}">\n{data}  </package>\n'
    '</packages>'
)
tcash = (
    '    <groupedCashRegisters action="{xtype}">\n{data}'
    '    </groupedCashRegisters>\n'
)
trevs = '    <groupedRevenues action="{xtype}">\n{data}    </groupedRevenues>\n'
texps = '    <groupedExpenses action="{xtype}">\n{data}    </groupedExpenses>\n'
tothe = (
    '    <otherExpenses>\n      <amount>{amount}</amount> <tax>{tax}</tax> '
    '<date>{date}</date>\n    </otherExpenses>\n'
)
tgcash = (
    '      <cashregister>\n        <cashreg_id>{tamNo}</cashreg_id>'
    ' <amount>{amount}</amount> <tax>{tax}</tax> <date>{date}</date>\n'
    '      </cashregister>\n'
)
greven = (
    '      <revenue> <afm>{afm}</afm> <amount>{amount}</amount> <tax>{tax}</tax>'
    ' <invoices>{invoices}</invoices> <note>{note}</note> <date>{date}</date>'
    ' </revenue>\n'
)
xlexpe = (
    '      <expense> <afm>{afm}</afm> <amount>{amount}</amount> <tax>{tax}</tax>'
    ' <invoices>{invoices}</invoices> <note>{note}</note>'
    ' <nonObl>{nonObl}</nonObl> <date>{date}</date> </expense>\n'
)


def create_xml(data):
    """
    Δημιουργία αρχείου xml για  ΜΥΦ
    Χρειαζόμαστε 4 πράγματα:
    0. ΑΦΜ εταρείας , year, month="12", branch="" action="replace"
    1. groupedRevenues
    2. groupedCashRegisters
    3. groupedExpenses
    4. otherExpenses
    Για τη λεπτομερή δομή του data δες τεστ : test_myf2xml.py
    """
    # Initialize all to ''
    revenues = expenses = other_expenses = gcash_registers = ''
    afms = []
    if data['grevenues']:
        revenues = trevs.format(
            xtype=data['action'],
            data=''.join(greven.format(**i) for i in data['grevenues'])
        )
        afms += [i['afm'] for i in data['grevenues'] if i['afm'].strip() != '']

    if data['gexpenses']:
        expenses = texps.format(
            xtype=data['action'],
            data=''.join(xlexpe.format(**i) for i in data['gexpenses'])
        )
        afms += [i['afm'] for i in data['gexpenses'] if i['afm'].strip() != '']

    if data['oexpenses']:
        other_expenses = tothe.format(**data['oexpenses'])

    if data['gcash']:
        gcash_registers = tcash.format(
            xtype=data['action'],
            data=''.join(tgcash.format(**i) for i in data['gcash'])
        )

    # finally add all to final rendering
    data['co']['data'] = revenues + gcash_registers + expenses + other_expenses
    xml_data = txml.format(**data['co'])
    afms = list(set(afms))  # Για να έχω μοναδικά ΑΦΜ
    afms.sort()
    return xml_data, afms
