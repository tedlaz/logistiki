from collections import defaultdict


class ColumnType:

    def render(self, value, size: int):
        raise NotImplementedError

    def reverse(self, textline):
        raise NotImplementedError

    def fill_front_zeros(self, txtval: str, size: int) -> str:
        len_txtval = len(txtval)
        if len_txtval > size:
            raise ValueError('Value is bigger than size')
        return '0' * (size - len_txtval) + txtval

    def fill_back_spaces(self, txtval: str, size: int) -> str:
        len_txtval = len(txtval)
        if len_txtval > size:
            raise ValueError('Value is bigger than size')
        return txtval + ' ' * (size - len_txtval)


class ColText(ColumnType):
    def render(self, value, size: int) -> str:
        return self.fill_back_spaces(value, size)

    def reverse(self, txtvalue: str):
        return txtvalue.strip()


class ColDate(ColumnType):
    def render(self, value, size: int) -> str:
        if value.strip() == '':
            return self.fill_back_spaces(value, size)
        yyyy, mm, dd = value.split('-')
        return f'{dd}{mm}{yyyy}'

    def reverse(self, txtvalue: str):
        if txtvalue.strip() == '':
            return ''
        dd = txtvalue[:2]
        mm = txtvalue[2:4]
        yyyy = txtvalue[4:8]
        return f'{yyyy}-{mm}-{dd}'


class ColPoso(ColumnType):
    def render(self, poso, size: int) -> str:
        poso = f'{poso:.2f}'.replace('.', '')
        return self.fill_front_zeros(poso, size)

    def reverse(self, txtvalue):
        return float(f'{txtvalue[:-2]}.{txtvalue[-2:]}')


class ColInt(ColumnType):
    def render(self, poso, size: int) -> str:
        poso = int(poso)
        return self.fill_front_zeros(str(poso), size)

    def reverse(self, txtvalue):
        return int(txtvalue)


class ColTextInt(ColumnType):
    def render(self, poso, size: int) -> str:
        poso = int(poso)
        return self.fill_front_zeros(str(poso), size)

    def reverse(self, txtvalue):
        return txtvalue.strip()


class Column:
    def __init__(self, name: str, typos: ColumnType, size: int) -> None:
        self.name = name
        self.column_type = typos
        self.size = size

    def render(self, value):
        return self.column_type.render(value, self.size)

    def read(self, txtvalue):
        return self.column_type.reverse(txtvalue)

    def __str__(self):
        return f'{self.name:30} {self.size:4}'


class Line:
    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix
        self.columns = []

    def __str__(self):
        st1 = f'Line {self.name!r} with total size:{self.size}\n'
        st1 += f"{'prefix':30} {self.prefix:>4}\n"
        for col in self.columns:
            st1 += f'{str(col)}\n'
        return st1

    @property
    def size(self):
        return sum(c.size for c in self.columns) + len(self.prefix)

    def add_column(self, column):
        self.columns.append(column)

    def render(self, data):
        stx = f'{self.prefix}'
        for column in self.columns:
            stx += column.render(data[column.name])
        return stx

    def read(self, textline: str):
        if not textline.startswith(self.prefix):
            raise ValueError(f'textline({textline}) is not compatible')
        if len(textline) != self.size:
            raise ValueError(
                f'textline({textline}) size ({len(textline)}) is not correct')
        arr = {}
        apo = eos = len(self.prefix)
        for column in self.columns:
            eos = column.size + apo
            arr[column.name] = column.read(textline[apo:eos])
            apo = eos
        return arr


class Document:
    def __init__(self) -> None:
        self.linetypes = {}
        self.lines = []

    def __str__(self):
        st1 = 'Document with template lines:\n'
        st1 += '\n'.join(str(ltype) for ltype in self.linetypes.values())
        return st1

    def add_linetype(self, code: str, linetype):
        if code in self.linetypes.keys():
            raise ValueError('Linetype code already exists')
        self.linetypes[code] = linetype

    def add_line(self, line):
        self.lines.append(line)

    def print_lines(self):
        for line in self.lines:
            for key, val in line.items():
                print(f'{key:<30}: {val:14}')
            print()

    def render(self):
        lst = [self.linetypes[i['line_code']].render(i) for i in self.lines]
        return '\n'.join(lst)

    def render2file(self, filename):
        with open(filename, 'w', encoding='WINDOWS-1253') as fil:
            fil.write(self.render())
        print(f'File {filename} created !!!')

    def parse(self, filename):
        with open(filename, encoding='WINDOWS-1253') as fil:
            lines = fil.read().split('\n')
        for lin in lines:
            for code, linetype in self.linetypes.items():
                if lin.startswith(code):
                    ldic = linetype.read(lin)
                    ldic['line_code'] = code
                    self.add_line(ldic)

    def get_totals(self):
        apodoxes = eisfores = meres = 0
        for line in self.lines:
            if line['line_code'] == '3':
                apodoxes += line['apodoxes']
                eisfores += line['katablitees_eisfores']
                meres += line['imeres_asfalisis']
        return apodoxes, eisfores, meres

    def correct_header(self):
        l_apodoxes, l_eisfores, l_meres = self.get_totals()
        self.lines[0]['apodoxes'] = l_apodoxes
        self.lines[0]['eisfores'] = l_eisfores
        self.lines[0]['totalmeres'] = l_meres

    def check(self):
        l_apodoxes, l_eisfores, l_meres = self.get_totals()
        assert l_apodoxes == self.lines[0]['apodoxes']
        assert l_eisfores == self.lines[0]['eisfores']
        assert l_meres == self.lines[0]['totalmeres']
        print('Everything is under control')

    def malakia(self):
        pos = []
        val = []
        for i, lin in enumerate(self.lines):
            if lin['line_code'] == '3':
                ndic = dict(lin)
                ndic['apodoxes_type'] = 18
                ndic['apoapasxolisi'] = '2020-03-15'
                ndic['eosapasxolisi'] = '2020-03-31'
                val.append(ndic)
                pos.append(i)
        pos.reverse()
        val.reverse()
        print(pos)
        for i, ps in enumerate(pos):
            self.lines.insert(ps+1, val[i])


def apd_builder():
    li1 = Line(name='Header', prefix='1')
    li1.add_column(Column('plithos', ColTextInt(), 2))
    li1.add_column(Column('aa', ColTextInt(), 2))
    li1.add_column(Column('fname', ColText(), 8))
    li1.add_column(Column('ekdosi', ColTextInt(), 2))
    li1.add_column(Column('dilosityp', ColTextInt(), 2))
    li1.add_column(Column('ypma', ColTextInt(), 3))
    li1.add_column(Column('ypname', ColText(), 50))
    li1.add_column(Column('epon', ColText(), 80))
    li1.add_column(Column('onoma', ColText(), 30))
    li1.add_column(Column('pateras', ColText(), 30))
    li1.add_column(Column('ame', ColTextInt(), 10))
    li1.add_column(Column('afm', ColTextInt(), 9))
    li1.add_column(Column('odos', ColText(), 50))
    li1.add_column(Column('arithmos', ColText(), 10))
    li1.add_column(Column('tk', ColTextInt(), 5))
    li1.add_column(Column('poli', ColText(), 30))
    li1.add_column(Column('apomina', ColTextInt(), 2))
    li1.add_column(Column('apoetos', ColTextInt(), 4))
    li1.add_column(Column('eosmina', ColTextInt(), 2))
    li1.add_column(Column('eosetos', ColTextInt(), 4))
    li1.add_column(Column('totalmeres', ColInt(), 8))
    li1.add_column(Column('apodoxes', ColPoso(), 12))
    li1.add_column(Column('eisfores', ColPoso(), 12))
    li1.add_column(Column('ypoboli', ColDate(), 8))
    li1.add_column(Column('pafsi', ColDate(), 8))
    li1.add_column(Column('filler', ColText(), 30))

    li2 = Line(name='Stoixeia Ergazomenoy', prefix='2')
    li2.add_column(Column('ama', ColTextInt(), 9))
    li2.add_column(Column('amka', ColTextInt(), 11))
    li2.add_column(Column('asf_eponymo', ColText(), 50))
    li2.add_column(Column('asf_onoma', ColText(), 30))
    li2.add_column(Column('asf_pateras', ColText(), 30))
    li2.add_column(Column('asf_mitera', ColText(), 30))
    li2.add_column(Column('asf_gennisi', ColDate(), 8))
    li2.add_column(Column('asf_afm', ColTextInt(), 9))

    li3 = Line(name='Stoixeia misthodosias', prefix='3')
    li3.add_column(Column('parartima_no', ColTextInt(), 4))
    li3.add_column(Column('kad', ColTextInt(), 4))
    li3.add_column(Column('plires_orario', ColTextInt(), 1))
    li3.add_column(Column('oles_ergasimes', ColTextInt(), 1))
    li3.add_column(Column('kyriakes', ColInt(), 1))
    li3.add_column(Column('eid', ColTextInt(), 6))
    li3.add_column(Column('eid_per_asfalisis', ColTextInt(), 2))
    li3.add_column(Column('kpk', ColTextInt(), 4))
    li3.add_column(Column('mismina', ColTextInt(), 2))
    li3.add_column(Column('misetos', ColTextInt(), 4))
    li3.add_column(Column('apoapasxolisi', ColDate(), 8))
    li3.add_column(Column('eosapasxolisi', ColDate(), 8))
    li3.add_column(Column('apodoxes_type', ColTextInt(), 2))
    li3.add_column(Column('imeres_asfalisis', ColInt(), 3))
    li3.add_column(Column('imeromisthio', ColPoso(), 10))
    li3.add_column(Column('apodoxes', ColPoso(), 10))
    li3.add_column(Column('eisf_asfalismenoy', ColPoso(), 10))
    li3.add_column(Column('eisf_ergodoti', ColPoso(), 10))
    li3.add_column(Column('eisf_total', ColPoso(), 11))
    li3.add_column(Column('epid_asfalismenoy_poso', ColPoso(), 10))
    li3.add_column(Column('epid_ergodoti_pososto', ColPoso(), 5))
    li3.add_column(Column('epid_ergodoti_poso', ColPoso(), 10))
    li3.add_column(Column('katablitees_eisfores', ColPoso(), 11))

    leof = Line(name='Terminator line', prefix='EOF')

    do1 = Document()
    do1.add_linetype('1', li1)
    do1.add_linetype('2', li2)
    do1.add_linetype('3', li3)
    do1.add_linetype('EOF', leof)
    return do1
