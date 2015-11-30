try:  # 3.x
    import urllib.parse as urllib
    import urllib.request as urllib2
except ImportError:  # 2.x
    import urllib
    import urllib2

import webbrowser

uml = """
@startuml
class foo <-- class bar : extends
@enduml
"""

url = "http://www.plantuml.com/plantuml/form"
data = urllib.urlencode({"text" : uml})
binary = data.encode("utf-8")
results = urllib2.urlopen(url, binary)
with open("results.html", "wb") as f:
    f.write(results.read())

webbrowser.open("results.html")