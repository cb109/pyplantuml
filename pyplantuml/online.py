import os
import re
import webbrowser

try:  # 3.x
    import urllib.parse as urllib
    import urllib.request as urllib2
except ImportError:  # 2.x
    import urllib
    import urllib2

ENC = "utf-8"
URL_FORM = "http://www.plantuml.com/plantuml/form"
URL_PNG = '"(?P<png>http://www.plantuml.com:80/plantuml/png/\w+)"'


def getResultFromPlantUmlServer(uml):
    """Takes either uml text or a file as input."""
    if os.path.isfile(uml):
        with open(uml) as f:
            uml = f.read()

    data = urllib.urlencode({"text" : uml})
    binaryData = data.encode(ENC)
    results = urllib2.urlopen(URL_FORM, binaryData)
    binaryHtml = results.read()
    html = binaryHtml.decode(ENC)
    return html


def displayInBrowser(html):
    """Extracts the png url from the
    html and opens it in the browser."""
    pattern = re.compile(URL_PNG)
    match = pattern.search(html)
    if match:
        url = match.group("png")
        webbrowser.open(url)
        return url