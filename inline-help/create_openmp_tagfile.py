# Python script that creates a doxygen tag file for the OpenMP documentation

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def get_all_website_links(url):
    # returns all URLs that are found on 'url'
    urls = set()
    soup = BeautifulSoup(requests.get(url).content, "html.parser")    
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href") #equals anchorfile
        for span in a_tag.findAll("span", attrs = {"class" : "texttt"}):
            text = span.contents #equals name
            if href == "" or href is None:
                # href empty tag
                continue
            urls.add(href)
            # write to xml file
            text[0] = text[0].replace(" ", "") # remove spaces
            f.write('\t\t<member kind="function">\n')
            f.write('\t\t\t<name>' + text[0] + '</name>\n')
            f.write('\t\t\t<anchorfile>' + href + '</anchorfile>\n')
            f.write('\t\t</member>\n')
            f.write('\t\t<member kind="function">\n')
            f.write('\t\t\t<name>omp::' + text[0] + '</name>\n')
            f.write('\t\t\t<anchorfile>' + href + '</anchorfile>\n')
            f.write('\t\t</member>\n')
    return urls

webpage = "https://kosl.github.io/openmp.org/spec-html/5.1/openmp.html"
f = open("openmp-doxygen-web.tag.xml", "w")
f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
f.write('<tagfile>\n')
f.write('\t<compound kind="namespace">\n')
f.write('\t\t<name>mpi</name>\n')
f.write('\t\t<filename></filename>\n')

links = get_all_website_links(webpage)

f.write('\t</compound>\n')
f.write('</tagfile>')
f.close()
