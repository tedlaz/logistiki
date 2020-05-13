from dataclasses import dataclass
from collections import namedtuple


# Par = namedtuple('Par', 'meres adeia_meres nyxta_ores argia_ores argia_meres')
# Apod = namedtuple('Apod', '')


@dataclass
class Parousies:
    meres: int = 0
    adeia_meres: int = 0
    nyxta_ores: float = 0
    argia_ores: float = 0
    argia_meres: int = 0

    @property
    def total_meres(self):
        return self.meres + self.adeia_meres


@dataclass
class Astheneia:
    apo: str = ''
    eos: str = ''
    meres_eos3: int = 0
    meres_more3: int = 0

    @property
    def total_meres(self):
        return self.meres_eos3 + self.meres_more3


@dataclass
class Kratisi:
    name: str
    ergazomenos: float
    ergodotis: float

    @property
    def total(self):
        return round(self.ergazomenos + self.ergodotis)

    def __add__(self, other):
        return Kratisi(
            f'{self.name}+{other.name}',
            self.ergazomenos + other.ergazomenos,
            self.ergodotis + other.ergodotis
        )

    def __str__(self):
        return f'Kratisi(name={self.name!r}, ergazomenos={self.ergazomenos}, ergodotis={self.ergodotis}, total={self.total})'


class CalcKratisi:
    def __init__(self, name):
        self.name = name

    def calculate(self, value):
        raise NotImplementedError

    def __repr__(self):
        return f'CalcKratisi(name={self.name!r})'


class CalcKratisiPososto(CalcKratisi):
    def __init__(self, name, pergazomenos, ptotal):
        super().__init__(name)
        self.pergazomenos = pergazomenos
        self.ptotal = ptotal

    @property
    def pergodotis(self):
        return self.ptotal - self.pergazomenos

    def calculate(self, poso):
        ergazomenos = round(self.pergazomenos * poso / 100, 2)
        total = round(self.ptotal * poso / 100, 2)
        ergodotis = round(total - ergazomenos, 2)
        return Kratisi(self.name, ergazomenos, ergodotis)


class Mis:
    __slots__ = ['meres', 'adeia_meres',
                 'nyxta_ores', 'argia_ores', 'argia_meres']
    pnyxta = .20
    pargia = .75

    def __init__(self, parousies: Parousies, kratiseis):
        self.par = parousies
        self.kratiseis = kratiseis
        self.calculate()

    def __repr__(self):
        return f'Mis({self.__dict__})'

    def calc_apodoxes_normal(self):
        raise NotImplementedError

    def calc_imeromisthio_oromisthio(self):
        raise NotImplementedError

    def calc_apodoxes_periodoy(self):
        self.calc_imeromisthio_oromisthio()
        self.calc_apodoxes_normal()
        self.ap_nyxta = self.par.nyxta_ores * self.oromisthio * self.pnyxta
        self.ap_argia_ores = self.par.argia_ores * self.oromisthio * self.pargia
        self.ap_argia_meres = self.par.argia_meres * self.imeromisthio * self.pargia
        self.ap_argia = self.ap_argia_meres + self.ap_argia_ores
        self.ap_total = self.ap_meres + self.ap_nyxta + self.ap_argia

    def calc_kratiseis(self):
        self.kratiseis_list = []
        for kratisi in self.kratiseis:
            self.kratiseis_list.append(kratisi.calculate(self.ap_total))

    def calculate(self):
        self.calc_apodoxes_periodoy()
        self.calc_kratiseis()


class MisMisthotos(Mis):
    def __init__(self, misthos, parousies, kratiseis):
        self.misthos = misthos
        super().__init__(parousies, kratiseis)

    def calc_imeromisthio_oromisthio(self):
        self.imeromisthio = self.misthos / 25
        self.oromisthio = self.imeromisthio * 6 / 40

    def calc_apodoxes_normal(self):
        self.ap_meres = self.par.total_meres * self.misthos / 25


class MisImeromisthios(Mis):
    def __init__(self, imeromisthio, parousies, kratiseis):
        self.imeromisthio = imeromisthio
        super().__init__(parousies, kratiseis)

    def calc_imeromisthio_oromisthio(self):
        self.oromisthio = self.imeromisthio * 6 / 40

    def calc_apodoxes_normal(self):
        self.ap_meres = self.par.total_meres * self.imeromisthio


def calc_misthos(meres, misthos):
    return meres * misthos / 25


def calc_imeromisthio(meres, imeromisthio):
    return meres * imeromisthio


def calc_oromisthio(ores, oromisthio):
    return ores * oromisthio


def calc_nyxterini_prosafksisi(ores, oromisthio, pososto):
    return ores * pososto / 100


def calc_argia_meres(meres, imeromisthio, pososto):
    return meres * imeromisthio * pososto / 100


def calculate(data):
    results = []
    for erg in data:
        results.append(erg.calculate())
