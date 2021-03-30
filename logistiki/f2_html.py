F2_HTML = """
<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<style>
table, th, td {{
    border: 1px solid black;
    border-collapse: collapse;
}}
th, td {{
    padding: 3px;
}}
</style>
</head>
<body style=" font-size:8pt; font-weight:400; font-style:normal; text-decoration:none;">
<h2><center>ΠΕΡΙΟΔΙΚΗ ΔΗΛΩΣΗ ΦΠΑ</center></h2>
<br>
<p>Από : <b>{apo}</b> Έως :  <b>{eos}</b></p>
<br>
<table border="1" align="center" width="100%" cellspacing="0" cellpadding="4">
  <tbody>
    <tr>
      <td colspan=12>Α. ΠΙΝΑΚΑΣ ΜΕ ΤΑ ΣΤΟΙΧΕΙΑ ΤΟΥ ΥΠΟΚΕΙΜΕΝΟΥ ΣΤΟ ΦΟΡΟ Ή ΛΗΠΤΗ</td>
    </tr>
    <tr>
      <td colspan=12>101.ΕΠΩΝΥΜΟ Ή ΕΠΩΝΥΜΙΑ <b>{epon}</b></td>
    </tr>
    <tr>
      <td colspan=4>102.ΟΝΟΜΑ <br> <b>{onom}</b></td>
      <td style="background-color:#D8EBF9"><center>103<center></td>
      <td colspan=4>ΟΝΟΜΑ ΠΑΤΕΡΑ <br><b>{patr}</b></td>
      <td style="background-color:#D8EBF9"><center>104<center></td>
      <td colspan=2>ΑΦΜ <br><b>{afm}</b></td>
    </tr>
  </tbody>
</table>
<br>
<table>
  <tbody>
    <tr>
      <td colspan=12>Β. ΠΙΝΑΚΑΣ ΕΚΡΟΩΝ - ΕΙΣΡΟΩΝ μετά την αφαίρεση (κατά συντελεστή) των επιστροφών - εκπτώσεων.</td>
    </tr>
    <tr>
      <td rowspan=3><center>Ι. ΕΚΡΟΕΣ, ΕΝΔΟΚ. ΑΠΟΚΤΗΣΕΙΣ & ΠΡΑΞΕΙΣ ΛΗΠΤΗ σε λοιπή Ελλάδα</center></td>
      <td width="3%" style="background-color:#D8EBF9"><center>301</center></td>
      <td align="right" width="9%">{i301}</td>
      <td width="3%"><center>13</center></td>
      <td width="3%" style="background-color:#D8EBF9" ><center>331</center></td>
      <td align="right" width="7%">{i331}</td>
      <td><center>Αγορές & δαπάνες εσωτερικού</center></td>
      <td width="3%" style="background-color:#D8EBF9" ><center>361</center></td>
      <td align="right" width="9%">{i361}</td>
      <td width="3%" style="background-color:#D8EBF9" ><center>381</center></td>
      <td align="right" width="7%">{i381}</td>
    </tr>
    <tr>
      <td style="background-color:#D8EBF9"><center>302</center></td>
      <td align="right">{i302}</td>
      <td><center>6</center></td>
      <td style="background-color:#D8EBF9"><center>332</center></td>
      <td align="right">{i332}</td>
      <td><center>Αγορές & εισαγωγές παγίων</center></td>
      <td style="background-color:#D8EBF9"><center>362</center></td>
      <td align="right">{i362}</td>
      <td style="background-color:#D8EBF9"><center>382</center></td>
      <td align="right">{i382}</td>
    </tr>
    <tr>
      <td style="background-color:#D8EBF9"><center>303</center></td>
      <td align="right">{i303}</td>
      <td><center>24</center></td>
      <td style="background-color:#D8EBF9"><center>333</center></td>
      <td align="right">{i333}</td>
      <td><center>Λοιπες εισαγωγές εκτός παγίων</center></td>
      <td style="background-color:#D8EBF9"><center>363</center></td>
      <td align="right">{i363}</td>
      <td style="background-color:#D8EBF9"><center>383</center></td>
      <td align="right">{i383}</td>
    </tr>
    <tr>
      <td rowspan=3><center>ΙΙ. ΕΚΡΟΕΣ, ΕΝΔΟΚ. ΑΠΟΚΤΗΣΕΙΣ & ΠΡΑΞΕΙΣ ΛΗΠΤΗ στα νησιά Αιγαίου</center></td>
      <td style="background-color:#D8EBF9"><center>304</center></td>
      <td align="right">{i304}</td>
      <td><center>9</center></td>
      <td style="background-color:#D8EBF9"><center>334</center></td>
      <td align="right">{i334}</td>
      <td><center>Ενδοκοινοτικές αποκτήσεις αγαθών</center></td>
      <td style="background-color:#D8EBF9"><center>364</center></td>
      <td align="right">{i364}</td>
      <td style="background-color:#D8EBF9"><center>384</center></td>
      <td align="right">{i384}</td>
    </tr>
    <tr>
      <td style="background-color:#D8EBF9"><center>305</center></td>
      <td align="right">{i305}</td>
      <td><center>4</center></td>
      <td style="background-color:#D8EBF9"><center>335</center></td>
      <td align="right">{i335}</td>
      <td><center>Ενδοκοινοτικές λήψεις υπηρεσιών</center></td>
      <td style="background-color:#D8EBF9"><center>365</center></td>
      <td align="right">{i365}</td>
      <td style="background-color:#D8EBF9"><center>385</center></td>
      <td align="right">{i385}</td>
    </tr>
    <tr>
      <td style="background-color:#D8EBF9"><center>306</center></td>
      <td align="right">{i306}</td>
      <td><center>17</center></td>
      <td style="background-color:#D8EBF9"><center>336</center></td>
      <td align="right">{i336}</td>
      <td><center>Λοιπές πράξεις λήπτη</center></td>
      <td style="background-color:#D8EBF9"><center>366</center></td>
      <td align="right">{i366}</td>
      <td style="background-color:#D8EBF9"><center>386</center></td>
      <td align="right">{i386}</td>
    </tr>
    <tr>
      <td><center><b>ΣΥΝΟΛΟ ΦΟΡ. ΕΚΡΟΩΝ</b></center></td>
      <td style="background-color:#D8EBF9"><center><b>307</b></center></td>
      <td align="right"><b>{i307}</b></td>
      <td><center>ΣΥΝ</center></td>
      <td style="background-color:#D8EBF9"><center><b>337</b></center></td>
      <td align="right"><b>{i337}</b></td>
      <td><center><b>ΣΥΝΟΛΟ ΦΟΡΟΛ. ΕΙΣΡΟΩΝ</b></center></td>
      <td style="background-color:#D8EBF9"><center><b>367</b></center></td>
      <td align="right"><b>{i367}</b></td>
      <td style="background-color:#D8EBF9"><center><b>387</b></center></td>
      <td align="right"><b>{i387}</b></td>
    </tr>
    <tr>
      <td><center>Ενδοκοινοτικές παραδόσεις</center></td>
      <td style="background-color:#D8EBF9"><center>342</center></td>
      <td align="right">{i342}</td>
      <td colspan=3 rowspan=10><center></center></td>
      <td colspan=3><center>δ. ΠΡΟΣΤΙΘΕΜΕΝΑ ΠΟΣΑ ΣΤΟ ΣΥΝΟΛΟ ΦΟΡΟΥ ΕΙΣΡΟΩΝ</center></td>
      <td colspan=2 rowspan=2><center>+</center></td>
    </tr>
    <tr>
      <td><center>Ενδοκοινοτικές παροχές υπηρεσιών</center></td>
      <td style="background-color:#D8EBF9"><center>345</center></td>
      <td align="right">{i345}</td>
      <td><center>Επιστροφή φόρου</center></td>
      <td style="background-color:#D8EBF9"><center>400</center></td>
      <td align="right">{i400}</td>
    </tr>
    <tr>
      <td><center>Εξαγωγές & απαλλαγές πλοίων και αεροσκαφών</center></td>
      <td style="background-color:#D8EBF9"><center>348</center></td>
      <td align="right">{i348}</td>
      <td><center>Λοιπά προστιθ. ποσά</center></td>
      <td style="background-color:#D8EBF9"><center>402</center></td>
      <td align="right">{i402}</td>
      <td style="background-color:#D8EBF9"><center>410</center></td>
      <td align="right">{i410}</td>
    </tr>
    <tr>
      <td><center>Λοιπές εκροές με Δικ Εκπ.</center></td>
      <td style="background-color:#D8EBF9"><center>349</center></td>
      <td align="right">{i349}</td>
      <td><center>Ποσά διακαν.</center></td>
      <td style="background-color:#D8EBF9"><center>407</center></td>
      <td align="right">{i407}</td>
      <td colspan=2 rowspan=3><center>-</center></td>
    </tr>
    <tr>
      <td><center>Εκροές χωρις δικ. εκπτ.</center></td>
      <td style="background-color:#D8EBF9"><center>310</center></td>
      <td align="right">{i310}</td>
      <td colspan=3><center>ε. ΑΦΑΙΡΟΥΜΕΝΑ ΠΟΣΑ ΑΠΟ ΣΥΝΟΛΟ ΦΟΡΟΥ ΕΙΣΡΟΩΝ</center></td>
    </tr>
    <tr>
      <td rowspan=2><center><b>ΣΥΝΟΛΟ ΕΚΡΟΩΝ</b></center></td>
      <td rowspan=2 style="background-color:#D8EBF9"><center><b>311</b></center></td>
      <td rowspan=2 align="right"><b>{i311}<b></td>
      <td><center>ΦΠΑ prorata</center></td>
      <td style="background-color:#D8EBF9"><center>411</center></td>
      <td align="right">{i411}</td>
    </tr>
    <tr>

      <td><center>Λοιπά αφαιρούμ. ποσά</center></td>
      <td style="background-color:#D8EBF9"><center>422</center></td>
      <td align="right">{i422}</td>
      <td style="background-color:#D8EBF9"><center>428</center></td>
      <td align="right">{i428}</td>
    </tr>
    <tr>
      <td rowspan=2><center><b>Κύκλος εργασιών ΦΠΑ</b></center></td>
      <td rowspan=2 style="background-color:#D8EBF9"><center><b>312</b></center></td>
      <td rowspan=2 align="right"><b>{i312}</b></td>
      <td><center>Ποσά διακανονισμών</center></td>
      <td style="background-color:#D8EBF9"><center>423</center></td>
      <td align="right">{i423}</td>
    </tr>
    <tr>
      <td colspan=3><center><b>ΥΠΟΛΟΙΠΟ ΦΟΡΟΥ ΕΙΣΡΟΩΝ</b></center></td>
      <td style="background-color:#D8EBF9"><center><b>430</b></center></td>
      <td align="right"><b>{i430}</b></td>
    </tr>
  </tbody>
</table>
<br>
<table border="1" align="center" width="100%" cellspacing="0" cellpadding="4">
  <tbody>
    <tr>
      <td colspan=7><center><b>Γ. ΠΙΝΑΚΑΣ ΕΚΚΑΘΑΡΙΣΗΣ ΦΟΡΟΥ</b> για καταβολή, έκπτωση ή επιστροφή (κωδ.337 μείον κωδ.430)</center></td>
    </tr>
    <tr>
      <td><center><b>ΠΙΣΤΩΤΙΚΟ ΥΠΟΛΟΙΠΟ</b></center></td>
      <td style="background-color:#D8EBF9"><center>470</center></td>
      <td align="right">{i470}</td>
      <td><center><b>ΧΡΕΩΣΤΙΚΟ ΥΠΟΛΟΙΠΟ</b></center></td>
      <td style="background-color:#D8EBF9"><center>480</center></td>
      <td align="right">{i480}</td>
      <td rowspan=7>Σημειώσεις ......................................</td>
    </tr>
    <tr>
      <td colspan=6>Προσδιορισμός οριστικού ποσού προς καταβολή, έκπτωση ή επιστροφή</td>
    </tr>
    <tr>
      <td><center>Πιστ.υπολ. προηγ. περιόδου</center></td>
      <td style="background-color:#D8EBF9"><center>401</center></td>
      <td align="right">{i401}</td>
      <td><center>Χρεωστικό μέχρι 30€ προηγ. περιόδου</center></td>
      <td style="background-color:#D8EBF9"><center>483</center></td>
      <td align="right">{i483}</td>
    </tr>
    <tr>
      <td><center>Βεβαιωμ. ποσά προηγ.</center></td>
      <td style="background-color:#D8EBF9"><center>403</center></td>
      <td align="right">{i403}</td>
      <td><center>Ποσό που επιστράφηκε</center></td>
      <td style="background-color:#D8EBF9"><center>505</center></td>
      <td align="right">{i505}</td>
    </tr>
    <tr>
      <td><center>Φόρος που έχει δεσμευτεί μέσω τραπεζών</center></td>
      <td style="background-color:#D8EBF9"><center>404</center></td>
      <td align="right"></td>
    </tr>
    <tr>
      <td><center>ΠΟΣΟ για έκπτωση</center></td>
      <td style="background-color:#D8EBF9"><center>502</center></td>
      <td align="right">{i502}</td>
      <td><center>Ποσό προς καταβολή</center></td>
      <td style="background-color:#D8EBF9"><center>511</center></td>
      <td align="right">{i511}</td>
    </tr>
    <tr>
      <td><center>ΑΙΤΟΥΜΕΝΟ ΠΟΣΟ για επιστροφή</center></td>
      <td style="background-color:#D8EBF9"><center>503</center></td>
      <td align="right"></td>
      <td><center>Καταβολή ποσού</center></td>
      <td style="background-color:#D8EBF9"><center>523</center></td>
      <td align="right"></td>
    </tr>
  <tbody>
</table>
<br>
<br>
<br>
<br>

</body>
</html>
"""