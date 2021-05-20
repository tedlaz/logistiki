from qlogistiki import misthodosia as mst
from qlogistiki.misthodosia import Parousies


def test_misthodosia_001():
    p1 = mst.CalcKratisiPososto("efka-101", 15, 32)
    p2 = mst.CalcKratisiPososto("epik2", 4, 4)
    ergs = []
    ergs.append(
        mst.MisMisthotos(misthos=810, parousies=Parousies(25), kratiseis=[p1, p2])
    )
    ergs.append(
        mst.MisImeromisthios(
            imeromisthio=50, parousies=Parousies(adeia_meres=10), kratiseis=[p1]
        )
    )
    # for erg in ergs:
    #     print(erg)

    # k1 = mst.Kratisi(10, 20)
    # k2 = mst.Kratisi(100, 200)
    # print(k1 + k2)

    p1 = mst.CalcKratisiPososto("efka-101", 15, 32)
    p2 = mst.CalcKratisiPososto("epik2", 4, 4)
    a11 = p1.calculate(200)
    a12 = p2.calculate(200)
    # print(a11 + a12)
