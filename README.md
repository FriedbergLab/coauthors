# coauthors
Find coauthors and their affiliations on all papers from a given author. Good for grant application conflict lists

```
usage: coauthors [-h] -n [NAME] -o [OUTFILE] -m EMAIL [-a AFFIL]
                 [-y YEARS YEARS]
                 [-s {Forward,Reverse,f,F,r,R,forward,reverse}] [-e [EXCLUDE]]
                 [-v] [-t {excel,csv}]

options:
  -h, --help            show this help message and exit
  -n, --name [NAME]     The name for which to find coauthors on publications
  -o, --outfile [OUTFILE]
  -m, --email EMAIL     A valid email is required by Entrez
  -a, --affil AFFIL     Institutional affiliation
  -y, --years YEARS YEARS
                        Two years for publication year range. Earliest is
                        1930, latest is one year in the future
  -s, --datesort {Forward,Reverse,f,F,r,R,forward,reverse}
                        Sort by publication year. Default: forward (ascending)
                        publication year.
  -e, --exclude [EXCLUDE]
                        Journal titles to exclude
  -v, --verbose
  -t, --outtype {excel,csv}
```
