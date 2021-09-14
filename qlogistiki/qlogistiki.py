import os
import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw

from . import data_operations_text as dot


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
                return str(self.mdata.values[index.row()][index.column()])
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
        self.book = None
        self.checked_account = ""
        if os.path.isfile(filename):
            self.book = dot.load_from_text(filename)
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
        self.tbl.doubleClicked.connect(self.show_arthro)

    def show_arthro(self, val):
        fixed_font = qg.QFontDatabase.systemFont(qg.QFontDatabase.FixedFont)
        num = val.sibling(val.row(), 0).data()
        tr1 = self.book.get_transaction(num)
        qw.QMessageBox.information(self, f"Αρθρο {num}", tr1.as_str())

    def validate_ypoloipa(self):
        correct_no, err, cor = self.book.validate()
        errm = "\n".join(err)
        corm = "\n".join(cor)
        message = f"Number of correct checks: {correct_no}\n"
        message += corm + "\n"
        if err:
            message += f"Errors:\n{errm}"
        else:
            message += "No errors :-)"
        qw.QMessageBox.about(self, "Validations", message)

    def refresh_model_from_iso(self, acc):
        """
        iso means isozygio
        """
        account = acc.sibling(acc.row(), 0).data()
        # Για να μην κάνει refresh όταν επιλέγεται ο ίδιος λογαριασμός
        if account == self.checked_account:
            return
        self.checked_account = account
        lred_color = (
            "Εξοδα",
            "Αγορές",
            "Προμηθευτές",
            "Πιστωτές",
            "ΦΠΑ",
            "Εργαζόμενοι",
        )
        lgreen_color = ("Πωλήσεις", "Πελάτες", "Εσοδα", "Χρεώστες")
        lblue_color = ("Ταμείο", "Μετρητά")
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
        self.lbl.setText(f"{lmos}")


class MainWindow(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(qc.Qt.WA_DeleteOnClose)
        self.settings = qc.QSettings()
        self.setMinimumSize(1300, 700)
        self.createMenus()
        self.fnam = self.get_filename()

    def get_filename(self):
        filename = self.settings.value("filename", defaultValue=None)
        if filename:
            if os.path.isfile(filename):
                self.init_vals(filename)
                return filename
            else:
                self.setWindowTitle(f"Το {filename} δεν είναι διαθέσιμο")
        return None

    def init_vals(self, filename):
        self.dlg = Dialog(filename, self)
        self.setCentralWidget(self.dlg)

    def createMenus(self):
        self.openAct = qw.QAction(
            "Open", self, statusTip="Open file", triggered=self.open
        )
        self.filemenu = self.menuBar().addMenu("&File")
        self.filemenu.addAction(self.openAct)

    def open(self):
        fnam, _ = qw.QFileDialog.getOpenFileName(self, "Open", self.fnam, "")
        if fnam:
            self.init_vals(fnam)
            self.settings.setValue("filename", fnam)


def main():
    app = qw.QApplication(sys.argv)
    app.setOrganizationName("TedLazaros")
    app.setOrganizationDomain("Tedlaz")
    app.setApplicationName("qlogistiki")
    dlg = MainWindow()
    dlg.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
