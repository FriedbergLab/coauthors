# coauthors

`coauthors` finds all coauthors in PubMed for a given year range, and
then outputs them to a csv, ods or Excel file.

Useful for declaring conflict of interest in grant applications and for
COI disclosures.

Example:

```
coauthors -n "Iddo Friedberg" -m "idoerg@iastate.edu" -y 2021 2025 -o
"IddoConflicts.xlsx" -t excel
```
```
usage: coauthors [-h] -n NAME -o OUTFILE -m EMAIL [-a AFFIL] [-y YEARS YEARS]
                 [-v] [-t {excel,csv}]

options:
  -h, --help            show this help message and exit
  -n, --name NAME       The name for which to find coauthors on publications
  -o, --outfile OUTFILE
  -m, --email EMAIL     A valid email is required by Entrez
  -a, --affil AFFIL     Institutional affiliation
  -y, --years YEARS YEARS
                        Two years for publication year range. Earliest is
                        1930, latest is one year in the future
  -v, --verbose
  -t, --outtype {excel,csv}
```
