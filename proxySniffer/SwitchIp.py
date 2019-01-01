import urllib.request
import requests

ip="58.243.50.184"
port="53281"
newIpData = {
    "http":ip+":"+port
}
proxy_support = urllib.request.ProxyHandler(newIpData)
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)


requests.request()
 