# Python script that creates a doxygen tag file for the MPI documentation

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def get_all_website_links(url):
    # returns all URLs that are found on 'url'
    urls = set()
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        text = a_tag.contents #equals name
        href = a_tag.attrs.get("href") #equals anchorfile
        if href == "" or href is None:
            # href empty tag
            continue
        if href.startswith('man'): #only man pages
            urls.add(href)
            # write to xml file
            f.write('\t\t<member kind="function">\n')
            f.write('\t\t\t<name>' + text[0] + '</name>\n')
            f.write('\t\t\t<anchorfile>' + href + '</anchorfile>\n')
            f.write('\t\t</member>\n')
            f.write('\t\t<member kind="function">\n')
            f.write('\t\t\t<name>MPI::' + text[0] + '</name>\n')
            f.write('\t\t\t<anchorfile>' + href + '</anchorfile>\n')
            f.write('\t\t</member>\n')
            f.write('\t\t<member kind="function">\n')
            f.write('\t\t\t<name>mpi::' + text[0] + '</name>\n')
            f.write('\t\t\t<anchorfile>' + href + '</anchorfile>\n')
            f.write('\t\t</member>\n')
    return urls

webpage = "https://open-mpi.org/doc/v4.0/"
f = open("mpi-doxygen-web.tag.xml", "w")
f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
f.write('<tagfile>\n')
f.write('\t<compound kind="namespace">\n')
f.write('\t\t<name>mpi</name>\n')
f.write('\t\t<filename></filename>\n')

links = get_all_website_links(webpage)

f.write('\t</compound>\n')
f.write('</tagfile>')
f.close()

f = open("mpi.json", "w")
f.write('{\n\t"url": "https://open-mpi.org/doc/v4.0/",\n\t"tagfile": "mpi-doxygen-web.tag"\n}')
f.close()
