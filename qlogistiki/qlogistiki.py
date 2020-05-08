import os
import sys
from datetime import date

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

from qlogistiki.book import Book
from qlogistiki.parser_text import parse
from qlogistiki.utils import dec2gr


class Dmodel(qc.QAbstractTableModel):
    """
    We pass a dictionary of values as data source
    headers : list of Header titles
    vals    : list of [list of column values]
    align   : list of (1=left, 2=center, 3=right)
    typos   : list of (1=decimal, ...)
    """

    def __init__(self, model_data, parent=None):
        super().__init__(parent)
        self.mdata = model_data

    def set_data(self, model_data):
        self.mdata = model_data
        # self.headers, self.vals, self.align, self.typos, self.siz = model_data

    def rowCount(self, parent):
        return len(self.mdata.values)

    def columnCount(self, parent):
        return len(self.mdata.headers)

    def headerData(self, section, orientation, role):
        if role == qc.Qt.DisplayRole:
            if orientation == qc.Qt.Horizontal:
                return self.mdata.headers[section]
            else:
                pass
                # return section + 1
        if role == qc.Qt.TextAlignmentRole:
            return qc.Qt.AlignCenter

    # def index(self, row, column, parent):
    #     return qc.QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == qc.Qt.DisplayRole:
            if self.mdata.types[index.column()] == 1:
                return dec2gr(self.mdata.values[index.row()][index.column()])
            else:
                return self.mdata.values[index.row()][index.column()]
        if role == qc.Qt.TextAlignmentRole:
            if self.mdata.aligns[index.column()] == 1:
                return qc.Qt.AlignLeft
            elif self.mdata.aligns[index.column()] == 2:
                return qc.Qt.AlignCenter
            elif self.mdata.aligns[index.column()] == 3:
                return qc.Qt.AlignRight


class Dialog(qw.QWidget):
    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.book = Book('', '')
        if os.path.isfile(filename):
            self.book = Book.from_parsed(*parse(filename))
        mainlayout = qw.QVBoxLayout()
        self.setLayout(mainlayout)
        hlayout = qw.QHBoxLayout()
        mainlayout.addLayout(hlayout)
        leftv = qw.QVBoxLayout()
        rightv = qw.QSplitter()
        rightv.setOrientation(qc.Qt.Vertical)
        hlayout.addLayout(leftv)
        hlayout.addWidget(rightv)

        self.iso = qw.QTableView()
        font = qg.QFont()
        font.setFamily("Arial")
        self.iso.setFont(font)

        self.iso.setMaximumWidth(450)
        self.iso.setSelectionBehavior(qw.QAbstractItemView.SelectRows)
        self.iso.setSelectionMode(qw.QAbstractItemView.SingleSelection)
        self.iso.setModel(Dmodel(self.book.isozygio_model()))
        self.iso.resizeColumnsToContents()
        self.iso.resizeRowsToContents()
        leftv.addWidget(self.iso)
        bvalidate = qw.QPushButton("Ελεγχος Λογαριασμών")
        leftv.addWidget(bvalidate)

        self.lbl = qw.QLabel(rightv)
        self.lbl.setAlignment(qc.Qt.AlignCenter)
        bold_font = qg.QFont()
        bold_font.setFamily("Arial")
        bold_font.setBold(True)
        bold_font.setPointSize(16)
        bold_font.setWeight(75)
        self.lbl.setFont(bold_font)
        self.lbl.setMaximumHeight(25)
        self.tbl = qw.QTableView(rightv)
        self.tbl.setFont(font)
        self.tbl.setWordWrap(True)
        self.tbl.setAlternatingRowColors(True)
        self.tbl.setSelectionMode(qw.QAbstractItemView.SingleSelection)
        self.setWindowTitle("Ισοζύγιο Λογαριασμών")
        if self.parent:
            self.parent.setWindowTitle(f"Ισοζύγιο Λογαριασμών ({filename})")
        # Connections
        bvalidate.clicked.connect(self.validate_ypoloipa)
        # self.sbar.some_acc_clicked.connect(self.refresh_model)
        self.iso.clicked.connect(self.refresh_model_from_iso)
        self.iso.activated.connect(self.refresh_model_from_iso)
        # self.tbl.doubleClicked.connect(self.model_rowdata)

    def validate_ypoloipa(self):
        correct_no, err = self.book.validate()
        errm = '\n'.join(err)
        message = f'Number of correct checks: {correct_no}\n'
        message += f'Errors:\n{errm}'
        qw.QMessageBox.about(self, 'Validations', message)

    def refresh_model_from_iso(self, acc):
        """
        iso means isozygio
        """
        self.lbl.setText('Loading data ...')
        account = acc.sibling(acc.row(), 0).data()
        lred_color = ('Εξοδα', 'Αγορές', 'Προμηθευτές',
                      'Πιστωτές', 'ΦΠΑ', 'Εργαζόμενοι')
        lgreen_color = ('Πωλήσεις', 'Πελάτες', 'Εσοδα', 'Χρεώστες')
        lblue_color = ('Ταμείο', 'Μετρητά')
        if account.startswith(lred_color):
            self.tbl.setStyleSheet("alternate-background-color: #FFDEE3;")
        elif account.startswith(lgreen_color):
            self.tbl.setStyleSheet("alternate-background-color: #deffde;")
        elif account.startswith(lblue_color):
            self.tbl.setStyleSheet("alternate-background-color: #DEF3FF;")
        else:
            self.tbl.setStyleSheet("alternate-background-color: #CCCCCC;")
        self.refresh_model(account)

    def refresh_model(self, lmos):
        self.model_lmos = Dmodel(self.book.kartella_model(lmos))
        self.tbl.setModel(self.model_lmos)
        self.tbl.verticalScrollBar().setValue(0)  # reset scrollbar position
        for i, size in enumerate(self.model_lmos.mdata.sizes):
            self.tbl.setColumnWidth(i, size)
        self.tbl.resizeRowsToContents()
        self.lbl.setText(f"{lmos} (lifo 200)")


class MainWindow(qw.QMainWindow):
    def __init__(self, filename=None):
        super().__init__()
        self.setAttribute(qc.Qt.WA_DeleteOnClose)
        self.settings = qc.QSettings()
        self.setMinimumSize(1300, 800)
        # self.isUntitled = True
        self.fnam = filename
        self.createMenus()
        if self.fnam:
            self.init_vals(self.fnam)
        else:
            self.fnam = self.settings.value("filename", defaultValue=None)
            if self.fnam:
                self.init_vals(self.fnam)

    def init_vals(self, filename):
        self.dlg = Dialog(filename, self)
        self.setCentralWidget(self.dlg)

    def createMenus(self):
        self.openAct = qw.QAction(
            'Open',
            self,
            statusTip='Open file',
            triggered=self.open)
        self.filemenu = self.menuBar().addMenu("&File")
        self.filemenu.addAction(self.openAct)

    def open(self):
        fnam, _ = qw.QFileDialog.getOpenFileName(self, 'Open', self.fnam, '')
        if fnam:
            self.init_vals(fnam)
            self.settings.setValue("filename", fnam)


def main(filename=None):
    app = qw.QApplication(sys.argv)
    app.setOrganizationName("TedLazaros")
    app.setOrganizationDomain("Tedlaz")
    app.setApplicationName("qlogistiki")
    dlg = MainWindow(filename)
    dlg.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
