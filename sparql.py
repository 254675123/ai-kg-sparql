import urllib
import json
import urllib.parse
import urllib.request


#SPARQL_SERVICE_URI = 'http://120.26.58.228/sparql'

"""
ERROR_CODES = {
            TIMEOUT: 10,
            MALFORMED: 20,
            SERVER: 30,
            UNKNOWN: 100
    };
    """

class MySparql:
    def __init__(self,host):
        self.host = host


    def   query(self, querystr):
        querystr = urllib.parse.quote(querystr)
        url = self.host +  '?query=' + querystr

        #for test
        url = "http://120.26.58.228/sparql?query=1"
        request = urllib.request.Request(url)
        request.add_header('Accept', 'application/sparql-results+json')

        try:
            result = urllib.request.urlopen(request ).read()
        except urllib.error.HTTPError:
            print("exception!")

        print("query result: %s" % (result))

        result = result.decode()
        result = json.loads(result)
        return result


if __name__ == "__main__":
    mysql = MySparql("http://120.26.58.228/sparql")
    querystr = """SELECT ?root  ?rootLabel    ?zhuying  ?zhuyingLabel  ?zhuyingLinkto     WHERE {
        BIND (wd:Q42857 AS ?root)
        wd:Q42857 wdt:P77 ?zhuying .
        BIND("root" AS  ?zhuyingLinkto)
        SERVICE wikibase:label {
                bd:serviceParam wikibase:language "zh-cn" .
            }
        }"""

    mysql.query(querystr)





