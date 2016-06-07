import urllib2
import requests
import re

#xsrf is a parameter specifically for zhihu.com. This may require a different parameter
# and more than one parameters for other application
# You need to check on your own
def get_xsrf(headers):
    firstURL = "http://www.zhihu.com/#signin"
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    request = urllib2.Request(firstURL,headers = headers)
    response = urllib2.urlopen(request)
    content = response.read()
    pattern = re.compile(r'name="_xsrf" value="(.*?)"/>',re.S)
    _xsrf = re.findall(pattern,content)
    return _xsrf[0]

def set_connection(headers,loginURL,email,password, afterURL):
    # setup header for HTTP request
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # loginURL = "http://www.zhihu.com/login/email"
    # LoginURL is the address where you sent your login request, check it on your browser.
    # Open a new request session
    s = requests.session()
    xsrf = get_xsrf()
    # your sign_up information
    data = {"email":email,"password":password,"_xsrf":xsrf}
    #sent out your login request and receive the response
    login = s.post(loginURL,data, headers = headers)
    #the URL you want to spiter after you log in.
    afterURL = "https://www.zhihu.com/explore"
    #start the spider
    response = s.get(afterURL, cookies = login.cookies, headers = headers)
    return response