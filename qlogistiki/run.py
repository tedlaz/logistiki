#!/usr/bin/env python

import argparse
import sys


class LogistikiRun:

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Εντολές Λογιστικής',
            usage=(
                "run <command> [<args>]\n\n"
                "Διαθέσιμες εντολές:\n"
                "   afm_validate Έλεγχοι ΑΦΜ (Αλγοριθμικά/online)\n"
                "   ee           Βιβλίο Εσόδων-Εξόδων\n"
                "   imerologio   Ημερολόγιο εγγραφών\n"
                "   isozygio     Ισοζύγιο περιόδου\n"
                "   kartella     Καρτέλλα λογαριασμού\n"
                "   myf          Συγκεντρωτική Τιμολογίων\n"
                "   fpa          ΦΠΑ περιόδου\n"
                "   fpa_check    Έλεγχος ΦΠΑ περιόδου\n"
            )
        )
        parser.add_argument('command', help='Εντολή για εκτέλεση')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Η εντολή δεν υπάρχει')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    # def commit(self):
    #     parser = argparse.ArgumentParser(
    #         description='Record changes to the repository')
    #     # prefixing the argument with -- means it's optional
    #     parser.add_argument('--amend', action='store_true')
    #     # now that we're inside a subcommand, ignore the first
    #     # TWO argvs, ie the command (git) and the subcommand (commit)
    #     args = parser.parse_args(sys.argv[2:])
    #     print(f'Running git commit, amend={args.amend}')

    # def fetch(self):
    #     parser = argparse.ArgumentParser(
    #         description='Download objects and refs from another repository')
    #     # NOT prefixing the argument with -- means it's not optional
    #     parser.add_argument('repository')
    #     args = parser.parse_args(sys.argv[2:])
    #     print(f'Running git fetch, repository={args.repository}')

    def isozygio(self):
        pars = argparse.ArgumentParser(description='Ισοζύγιο Λογαριασμών')
        pars.add_argument('-f', '--From', help='Από ημερομηνίαn')
        pars.add_argument('-t', '--To', help='Έως ημερομηνία')
        pars.add_argument('-i', '--Inifile', help='Όνομα αρχείου ini')
        args = pars.parse_args(sys.argv[2:])


if __name__ == '__main__':
    LogistikiRun()
