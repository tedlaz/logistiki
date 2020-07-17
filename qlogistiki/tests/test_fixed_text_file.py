import os
from qlogistiki import fixed_text_file as ftf

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_fixed_text_file_01():
    bfile = os.path.join(dir_path, 'CSL01')
    apd = ftf.apd_builder()
    apd.parse(bfile)
    v1 = ftf.ColTextCapital()
    t1 = v1.render('αργυρίου', 10)
    assert t1 == 'ΑΡΓΥΡΙΟΥ  '

    # print(apd.lines)
    assert apd.check()
    rval = apd.render()
    assert rval.startswith('10101CSL01   0101218ΠΑΡΟΥ')
    assert rval[-3:] == 'EOF'
    assert apd.linetype_names == [
        'Header',
        'Stoixeia Ergazomenoy',
        'Stoixeia misthodosias',
        'Terminator line'
    ]

    # do1.malakia()
    # apd.correct_header()
    # apd.render2file('CSL01-corrected')
    print('')
    # print(apd.with_greek_lbl())
    print(apd.synodeftiko())
    # print(apd.linetypes_report())
