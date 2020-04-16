from logistiki.utils import dec
from logistiki.logger import logger
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
f2_template = os.path.join(dir_path, 'f2.html')

F2CODES = [
    'apo', 'eos', 'epon', 'onom', 'patr', 'afm',
    'i301', 'i302', 'i303', 'i304', 'i305', 'i306', 'i307',
    'i331', 'i332', 'i333', 'i334', 'i335', 'i336', 'i337',
    'i361', 'i362', 'i363', 'i364', 'i365', 'i366', 'i367',
    'i381', 'i382', 'i383', 'i384', 'i385', 'i386', 'i387',
    'i342', 'i345', 'i348', 'i349', 'i310', 'i311', 'i312',
    'i400', 'i402', 'i407', 'i410', 'i411', 'i422', 'i423', 'i428', 'i430',
    'i470', 'i401', 'i403', 'i404', 'i502', 'i503',
    'i480', 'i483', 'i505', 'i511', 'i523'
]


def sumd(dic, sumkeys):
    """
    Sums values from a dictionary according to sumkeys parameter
    dic: {key1: val1, key2:val2, ...}
    sumkeys: [key1, key3, ...]
    """
    val = dec(0)
    for key in sumkeys:
        val += dic.get(key, dec(0))
    return val


def dec2str(val):
    '''
    Returns string with Greek Formatted decimal (12345.67 becomes 12.345,67)
    '''
    if val == 0:
        return ''
    return f'{val:,.2f}'.replace('.', '|').replace(',', '.').replace('|', ',')


def calculate_f2(dat):
    """
    Calculate values
    """
    adi = {}
    # Εκροές με ΦΠΑ
    for elm in range(301, 307):
        adi[elm] = dat.get(elm, dec(0))
    adi[307] = sumd(adi, range(301, 307))
    adi[331] = dec(adi[301] * dec(.13))
    adi[332] = dec(adi[302] * dec(.06))
    adi[333] = dec(adi[303] * dec(.24))
    adi[334] = dec(adi[304] * dec(.09))
    adi[335] = dec(adi[305] * dec(.04))
    adi[336] = dec(adi[306] * dec(.17))
    adi[337] = sumd(adi, range(331, 337))
    # Λοιπές εκροές
    adi[342] = dat.get(342, dec(0))
    adi[345] = dat.get(345, dec(0))
    adi[348] = dat.get(348, dec(0))
    adi[349] = dat.get(349, dec(0))
    adi[310] = dat.get(310, dec(0))
    adi[311] = sumd(adi, [307, 342, 345, 348, 349, 310])
    adi[312] = adi[311] - dat.get(364, dec(0)) - dat.get(365, dec(0))
    # Εισροές με ΦΠΑ
    for elm in range(361, 367):
        adi[elm] = dat.get(elm, dec(0))
    adi[367] = sumd(adi, range(361, 367))
    for elm in range(381, 387):
        adi[elm] = dat.get(elm, dec(0))
    adi[387] = sumd(adi, range(381, 387))
    # Ο λογαριασμός ελέγχου του φπα περιόδου
    fpa_apo_logistiki = dat.get(5400, dec(0))
    delta_fpa = adi[337] - adi[387] + fpa_apo_logistiki
    if delta_fpa > 0:
        dat[402] = delta_fpa
    elif delta_fpa < 0:
        dat[422] = -delta_fpa
    # Προστιθέμενα ποσά
    for elm in [400, 402, 407]:
        adi[elm] = dat.get(elm, dec(0))
    adi[410] = sumd(adi, [400, 402, 407])
    # Αφαιρούμενα ποσά
    for elm in [411, 422, 423]:
        adi[elm] = dat.get(elm, dec(0))
    adi[428] = sumd(adi, [411, 422, 423])
    adi[430] = adi[387] + adi[410] - adi[428]
    # Πίνακας Εκκαθάρισης Φόρου
    adi[401] = dat.get(401, dec(0))
    adi[483] = dat.get(483, dec(0))
    adi[403] = dat.get(403, dec(0))
    adi[505] = dat.get(505, dec(0))
    if adi[430] < adi[337]:
        adi[470] = dec(0)
        adi[480] = adi[337] - adi[430]
    else:
        adi[470] = adi[430] - adi[337]
        adi[480] = dec(0)
    if (adi[480] + adi[483]) > (adi[470] + adi[401]):
        adi[511] = (adi[480] + adi[483]) - (adi[470] + adi[401])
    else:
        adi[502] = (adi[470] + adi[401]) - (adi[480] + adi[483])
    return adi


def pre_render(header, data):
    """
    Prepare data
    """
    adic = {'i%s' % key: dec2str(data[key]) for key in data}
    adic['apo'] = header.get('apo', '')
    adic['eos'] = header.get('eos', '')
    adic['epon'] = header.get('name', '')
    adic['onom'] = header.get('onom', '')
    adic['patr'] = header.get('patr', '')
    adic['afm'] = header.get('afm', '')
    return adic


def f2_render(head, data, html_file=None, template=f2_template):
    """
    Render data to html
    """
    f2data = pre_render(head, calculate_f2(data))
    with open(template) as fil:
        html_template = fil.read()
    # Create and fill all form fields with ''
    html_data = {i: '' for i in F2CODES}
    # Fill fields from f2data
    for key, val in f2data.items():
        if key in html_data.keys():
            html_data[key] = val
    # Finally save the form
    if html_file:
        with open(html_file, 'w') as fout:
            fout.write(html_template.format(**html_data))
        logger.info(f'fpa report saved to file: {html_file}')
    else:
        print(html_data)


if __name__ == '__main__':
    # print(render_f2({'epon': 'ΛΑΖΑΡΟΣ'}, 'skata.html'))
    HEAD = {
        'epon': 'ΔΟΚΙΜΗ ΕΠΕ', 'afm': '123123123',
        'apo': '1/2019', 'eos': '3/2019'
    }
    # data = {301: 100, 303: 1500, 361: 1500, 381: 360, 401: 100, 364: 100, }
    DATA = {361: dec(95156.97), 303: dec(101119.21),
            306: dec(28529.25), 364: dec(1825.68), 349: dec(39527.90)}
    f2_render(HEAD, DATA)
