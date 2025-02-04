import csv
from lxml import etree as ElementTree


def parseDBLP():
    authors = {}

    with open("/home/shashankr/CSrankings/dblp2.xml", mode="rb") as f:
        # was: with gzip.open('dblp.xml.gz') as f:

        oldnode = None

        foundArticle = False
        authorName = ""

        for (_, node) in ElementTree.iterparse(f, events=["start", "end"]):

            if oldnode is not None:
                oldnode.clear()
            oldnode = node

            if node.tag == "inproceedings" or node.tag == "article":

                for child in node:
                    if child.tag == "booktitle" or child.tag == "journal":
                        foundArticle = True
                        break

                if not foundArticle:
                    # Nope.
                    continue

                # Now, count up how many faculty from our list are on this paper.

                for child in node:
                    if child.tag == "author":
                        authorName = child.text
                        if authorName is not None:
                            authorName.strip()
                            if authorName not in authors:
                                authors[authorName] = 1

    return authors


#    a = sorted(authors.iteritems(), key=operator.itemgetter(1))
#    for k in a:
#        print k[0]


def csv2dict_str_str(fname):
    with open(fname, mode="r") as infile:
        reader = csv.reader(infile)
        # for rows in reader:
        #    print rows[0], "-->", rows[1]
        d = {
            str(rows[0].strip()) : str( rows[1].strip() )
            for rows in reader
        }
    return d


facultydict = csv2dict_str_str("/home/shashankr/CSrankings/csrankings.csv")

authors = parseDBLP()

# for name in facultydict:
#     if name not in authors:
#         print(name.encode("utf-8"))

# print "Total faculty: ", len(facultydict)
print( len(parseDBLP() ) )