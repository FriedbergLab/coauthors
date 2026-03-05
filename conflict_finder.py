#!/usr/bin/env python

# Copyright (C) 2026 Iddo Friedberg
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import argparse
import re
from datetime import datetime
from Bio import Entrez, Medline
import pandas as pd

def get_papers_by_author(name, affiliation):
    """
    
    Accepts an author name and (optional) institutional affiliation.  Returns
    all the papers for which they are a co-author, maximum 300. 

    The pubmed IDs are returned as a set. This is to avoid duplications with
    other authors: if a paper was authored by 2 authors, it will only count
    once

    """

    if not affiliation:
        handle = Entrez.esearch(db="pubmed", 
            term=f"{name}[AU]",retmax=300)
    else:
        handle = Entrez.esearch(db="pubmed", 
                term=f"{name}[AU] AND {affiliation}[AD]",retmax=300)
    record = Entrez.read(handle)
    handle.close()
    id_set = set(record['IdList'])
    return id_set

def get_papers_by_ids(id_set):
    """
    Receives a set of pubmed IDs, returns a list of paper records in
    XML.

    """
    stream = Entrez.efetch(db="pubmed", id=list(id_set), rettype="medline", retmode="xml")
    paper_recs = Entrez.read(stream)
    return(paper_recs)

def in_year_range(paper_rec,year_range):
    """ Check if a paper is in the request publication year range"""
    #try:
        #pub_year = int(paper_rec["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
    #except IndexError:
    pub_year = int(paper_rec["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"])
    print(f"WOW {pub_year}")
    if pub_year in year_range:
        retval = True
    else:
        retval = False
    return retval


def get_paper_authors(paper_recs, year_range):
    author_set = set()
    affil_dict = {}
    for paper_rec in paper_recs["PubmedArticle"]:
        if not in_year_range(paper_rec, year_range):
            continue
        for author in paper_rec["MedlineCitation"]["Article"]["AuthorList"]:
            author_set.add((author['ForeName'],author['LastName']))
            if not author["AffiliationInfo"]:
                affil_dict[(author['ForeName'],author['LastName'])] = None
            else:
                affil_dict[(author['ForeName'],author['LastName'])] = author["AffiliationInfo"][0]["Affiliation"]
    return (author_set, affil_dict)

def main(author, email, years,datesort="F",outfile=None):
    print("author", author)
    print("looking...")
    Entrez.email = email
    year_range = range(years[0],years[1]+1)
    id_set = get_papers_by_author(author,None)
    print(id_set)
    paper_recs = get_papers_by_ids(id_set)
    author_set, affil_dict = get_paper_authors(paper_recs,year_range)
    for i in affil_dict.items():
        print(i)
    print(len(affil_dict.items()))
    df = pd.DataFrame([(k[0],k[1],v) for k,v in affil_dict.items()],
                      columns=["forename","lastname","affiliation"])
    df.to_excel("coauthors.xlsx",index=False)
if __name__ == '__main__':

    print("""
    coauthors Copyright (C) 2026 Iddo Friedberg 
    This program comes with ABSOLUTELY NO WARRANTY. 
    This is free software, and you are welcome to redistribute it
    under certain conditions. See the GNU General Public License 
    for more details:
    <https://www.gnu.org/licenses/gpl-3.0.txt>
    """)
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n','--name',nargs='+',default=None)
    
    parser.add_argument('-o','--outfile',nargs='?',type=argparse.FileType('w'),
                        default=sys.stdout)
    parser.add_argument('-m','--email',required=True,
                        help="A valid email is required by Entrez")
    parser.add_argument('-a','--affil',
                       help="Institutional affiliation")
    parser.add_argument('-y','--years',nargs=2,type=int,
                        default=[int(datetime.now().year)-4, int(datetime.now().year)],
                        help="Two years for publication year range. Earliest is 1930, latest is one year in the future")
    parser.add_argument('-s','--datesort',
                        choices=['Forward','Reverse','f','F','r','R','forward','reverse'],
                        default='forward',
                        help="Sort by publication year. Default: forward (ascending) publication year.")
    parser.add_argument('-e','--exclude',nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help="Journal titles to exclude")
    parser.add_argument('--verbose','-v', action='count', default=0)

    args = parser.parse_args()
    # Check year range is good. Nothing before 1930 or after a year in the future from now.
    args.years.sort()
    if args.years[0] < 1930 or args.years[1] > int(datetime.now().year)+1:
        raise ValueError(f'Bad year range {args.years[0]}, {args.years[1]}')
    # Check validity of email addresss
    # if not re.match('^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,}$',args.email):
    if not re.match('^[A-z0-9._%+-]+@[A-z0-9.-]+.[A-z]{2,}$',args.email):
        raise ValueError(f'Invalid email address {args.email}')
    # print(args.infile)
    # print(args.names)
    # print(args.years)
    author = args.name[0]
    print(author)
    print(args.years)
    main(author,args.email, args.years,args.datesort)
