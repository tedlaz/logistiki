from .book import Book


class Partner:
    partner_type = "unknown"
    default_status = "MIXED"

    def __init__(self, afm, name, country):
        self.afm = afm
        self.name = name
        self.country = country

    def in_myf(self):
        return False

    def in_intrastat(self):
        return False

    def check(self):
        """
        Εδώ γίνεται ο έλεγχος βάσει ΑΦΜ ανάλογα με την περίπτωση
        Σε περίπτωση που έχουμε πελάτες/προμηθευτές εσωτερικού η
        ενδοκοινοτικούς το σύστημα ελέγχει online.
        Σε περίπτωση που έχουμε Ελληνικό ΑΦΜ τρέχει πρώτα ο αλγόριθμος
        τοπικά.
        """
        pass

    def __str__(self):
        return f"{self.afm} {self.name} {self.country}"

    def __repr__(self):
        return (
            f"Partner(afm={self.afm!r}, "
            f"name={self.name!r}, "
            f"country={self.country!r})"
        )


class Customer(Partner):
    partner_type = "Πελάτης"
    default_status = "DEBIT"
    account = "Πελάτες"


class CustomerGreece(Customer):
    account = "Πελάτες.Εσωτερικού"

    def __init__(self, afm, name):
        super().__init__(afm, name, "Ελλάδα")

    def in_myf(self):
        return True


class CustomerEuro(Customer):
    account = "Πελάτες.Ενδοκοινοτικοί"

    def in_intrastat(self):
        return True


class CustomerAbroad(Customer):
    account = "Πελάτες.Εξωτερικού"


class Vendor(Partner):
    partner_type = "Προμηθευτής"
    default_status = "CREDIT"
    account = "Προμηθευτές"


class VendorGreece(Vendor):
    account = "Προμηθευτές.Εσωτερικού"

    def in_myf(self):
        return True


class VendorEuro(Vendor):
    account = "Προμηθευτές.Ενδοκοινοτικοί"

    def in_intrastat(self):
        return True


class VendorAbroad(Vendor):
    account = "Προμηθευτές.Εξωτερικού"


class Enterprise:
    def __init__(self, afm: str, name: str) -> None:
        self.afm = afm
        self.name = name
        self.book = Book(self.afm, self.name, [], [], {}, [])

    def buy_assets(self, date, par, per, afm):
        pass

    def sell_assets(self):
        pass

    def buy_goods(self):
        pass

    def sell_goods(self):
        pass

    def sell(self):
        pass

    def expense(self):
        pass
