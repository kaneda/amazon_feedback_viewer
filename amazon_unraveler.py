import urllib2
from BeautifulSoup import BeautifulSoup

b = "http://www.amazon.c"
us = "om"
ca = "a"
m = "/gp/aag/ajax/paginatedFeedback.html?"

def extractInfo(comment,ratingFilter):
        cSplit = comment.findAll('li',text=True)
        try:
                if(len(cSplit) == 3 and int(cSplit[0][0]) < ratingFilter): return (cSplit[0],cSplit[1],cSplit[2]) # rating,comment,rater
        except Exception:
                pass
        return None

def formatPage(p,ratingFilter):
        ret = []
        for comment in BeautifulSoup(p).findAll("li")[1:-1]:
                ex = extractInfo(comment,ratingFilter)
                if(ex): ret.append(ex)
        return ret

def getPage(u,n):
        res = None
        try: res = urllib2.urlopen("{0}&&currentPage={1}".format(u,n)).read()
        except Exception as e: pass
        finally: return res

def formatUrl(u,usMode):
        params = u.split('?')
        if(len(params) != 2): return ""
        e = params[1]
        s = params[0].split('/')[-1]

        res = ""
        if(usMode): res = "{0}{1}{2}{3}&{4}".format(b,us,m,e,s)
        else: res = "{0}{1}{2}{3}&{4}".format(b,ca,m,e,s)

        return res

def getPages(u,usMode,n,ratingFilter):
        ratings = []
        count = 0
        total_len = 0
        baseUrl = formatUrl(u,usMode)
        for i in range(n):
                f = formatPage(getPage(baseUrl,i),ratingFilter)
                if(f):
                        total_len += len(f)
                        ratings.append(f)
        return (ratings,total_len)

