import pymysql
import urllib
import json
import urllib.parse
import urllib.request
import datetime
import time
import json

_HOST = 'http://120.26.58.228/w/api.php'

_COMPANY_PROPERTY = "Q9"
_ITEM_TYPE_ID = "P3"
_TYPE_COMPANY_PROPERTY = "11"
_TYPE_PEOPLE_PROPERTY = "33"

def  getToken():
    '''
    Setup logger to log start daemon error
    '''
    body_value = {"action":"query", "meta":"tokens", "format":"json" }
    body_value  = urllib.parse.urlencode(body_value)
    request = urllib.request.Request(_HOST + '?' + body_value)
    #request.add_header(keys, headers[keys])
    result = urllib.request.urlopen(request ).read()
    result = result.decode()
    result = json.loads(result)
    #print("result:%s"%(result))
    #print("getToken:%s" % (result['query']['tokens']['csrftoken']))
    return result['query']['tokens']['csrftoken']

def addStringClaim(token, entity, property_type, value):
    if  value =="":
        return None

    value = "\"" + value + "\""
    claims = { 'token':token, "entity":entity, "snaktype":"value", "property":property_type,"value": value}
    claims = urllib.parse.urlencode(claims).encode('utf8')

    action = {"action":"wbcreateclaim", "format":"json"}
    action = urllib.parse.urlencode(action)

    request = urllib.request.Request(url = _HOST + '?' + action , data = claims)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Content-Length',  len(claims))
    result = urllib.request.urlopen(request ).read()
    print("addStringClaim result: %s" % (result))

    result = result.decode()
    result = json.loads(result)

    if  "error" in result:
        print("addStringClaim error:%s,"%(entity))
        return None

    return result["claim"]["id"]

def addDateClaim(token, entity, property_type, time ):


  #  time":"+00000002010-01-02T00:00:00Z",

    #claims = dict()
    value = {"time": time, "timezone": 0, "before":0,"after":0,"precision":11, "calendarmodel":"http://www.wikidata.org/entity/Q1985727"}
    value = json.dumps(value)

    claims = { 'token':token, "entity":entity, "snaktype":"value", "property":property_type,"value": value}
    claims = urllib.parse.urlencode(claims).encode('utf8')


    action = {"action":"wbcreateclaim", "format":"json"}
    action = urllib.parse.urlencode(action)

    request = urllib.request.Request(url = _HOST + '?' + action , data = claims)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Content-Length',  len(claims))
    result = urllib.request.urlopen(request ).read()
    print("addClaim result: %s" % (result))

    result = result.decode()
    result = json.loads(result)
    return result["claim"]["id"]

def addClaim(token, entity, property_type, value_id ):
    #claims = dict()
    value = {"entity-type": "item", "numeric-id": value_id}
    value = json.dumps(value)

    claims = { 'token':token, "entity":entity, "snaktype":"value", "property":property_type,"value": value}
    claims = urllib.parse.urlencode(claims).encode('utf8')


    action = {"action":"wbcreateclaim", "format":"json"}
    action = urllib.parse.urlencode(action)

    request = urllib.request.Request(url = _HOST + '?' + action , data = claims)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Content-Length',  len(claims))
    result = urllib.request.urlopen(request ).read()
    print("addClaim result: %s" % (result))

    result = result.decode()
    result = json.loads(result)
    return result["claim"]["id"]


def  createItem(token,label,description):
    '''
    Setup logger to log start daemon error
    '''
    #token = getToken()

    data = dict()
    item_label = {"language":"zh","value":label}
    #item_descriptions = {"language":"zh","value":description}
    item_descriptions = {"language":"zh","value":description}
    data["labels"] = [item_label]
    data["descriptions"] = [item_descriptions]
    data = json.dumps(data)

    #body_value = { "token":token, "new":"item","data":data}
    body_value = { 'token':token, "data":data, "new":"item" }
    body_value = urllib.parse.urlencode(body_value).encode('utf8')
    action = {"action":"wbeditentity", "format":"json"}
    action = urllib.parse.urlencode(action)

    #body_value = json.dumps(body_value).encode('utf8')
    #print("createItem : %s" % (body_value))

    request = urllib.request.Request(url = _HOST + '?' + action , data = body_value)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Content-Length',  len(body_value))
    result = urllib.request.urlopen(request ).read()
    #print("createItem result: %s" % (result))

    result = result.decode()
    result = json.loads(result)
    if  "error" in result:
        print("createItem error:%s,  result:%s"%(label, result))
        return None

    id = result["entity"]["id"]
    print ("createItem ID:%s"%(id))
    return id
    #addClaim(token, id,  "P3", "13213")
    #addStringClaim(token, id,  "P59", "12312fsd")
#    addClaim(token, id,  "P64", "+00000002010-01-02T00:00:00Z")

def   searchItem(item_name):
    body_value = { "search":item_name, "language":"zh" }
    body_value = urllib.parse.urlencode(body_value).encode('utf8')
    action = {"action":"wbsearchentities", "format":"json"}
    action = urllib.parse.urlencode(action)

    request = urllib.request.Request(url = _HOST + '?' + action , data = body_value)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Content-Length',  len(body_value))
    result = urllib.request.urlopen(request ).read()
    print("searchItem result: %s" % (result))

    result = result.decode()
    result = json.loads(result)
    success = result["success"]
    if success != 1:
        return

    search_result = result["search"]
    if len(search_result) > 0:
        #return search_result[0]["id"]
        for x in search_result:
            if  x["label"] == item_name:
                return x["id"]

        return
    else:
        return

def  readJson(filename):
    file_object = open(filename)
    try:
         data = json.load(file_object)
         return data
    finally:
         file_object.close( )

if __name__ == "__main__":
    """
    data = readJson("/home/bywang/work/dd/222.json")
    data = data["data"]
    token = getToken()
    for v in data:
        item = v["zhuying"]
        num = item.find('Q')
        if  num != -1 :
            item =  item[num:]
            addClaim(token, item, "P75", "43076")
            print(item)
    """
    searchItem("手游");

    #print(data)
