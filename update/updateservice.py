import sys
import os
sys.path.append("..")
from  api import *

_HOST1 = 'http://120.26.58.228/w/api.php'

class UpdateService:
    "docstring for UpdateServi"
    def __init__(self):
        self.dict_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),   os.path.pardir, 'parse/dict'))


    def  getRecentChange(self):
        # 设置action
        action = {"action": "query", "format": "json", "list":"recentchanges", "rctype":"edit|new", "rclimit":"10","rcstart":"2017-04-07T01:22:01Z", "rcdir":"newer"}
        action_encode = urllib.parse.urlencode(action)

        # 定义请求
        request = urllib.request.Request(url=_HOST1 + '?' + action_encode)
        print(request)
        res_data = urllib.request.urlopen(request)
        res = res_data.read()
        # 解码数据，并返回json对象
        result = res.decode()
        result = json.loads(result)
        if "query" in result:
               print(result["query"])


    def getAllObject(self):
        sql =     ( "SELECT ?obj  ?objLabel WHERE {"
                "?obj wdt:P75 ?pro ."
                "SERVICE wikibase:label {"
                "bd:serviceParam wikibase:language \"zh-cn\" ."
            "}"
           "}")
        api = Wikiapi()
        result = api.getQueryDataBySparql(sql)

        objs = result["results"]["bindings"]
        for obj in objs:
            id = obj["obj"]["value"]
            id = id[id.find('Q'):]
            print(id)
            self.addEntityToDict(id)


    def addEntityToDict(self, id):
        api = Wikiapi()
        entityobj = api.getwbentitiesByid(id)
        entity = WikiEntity(id, entityobj)
        if entity.label == "":
            print("Error, % has no label"%entity.id)
            return

        if entity.type == "property" or   (entity.type == "item" and entity.isVirtualObject() != True):
            dict_file = ""
            if entity.isNumberProperty():
                dict_file = self._getIndicatorsNumberFile()
                print("add number property")
            elif entity.isObjectProperty():
                dict_file = self._getIndicatorsObjectFile()
                print("add object property")
            elif entity.isNormalProperty():
                dict_file = self._getIndicatorsNormalFile()
                print("add normal property")
            elif entity.type == "item":
                dict_file = self._getSubjectFile()
                print("add subject")

            if dict_file != "":
                newitem = []
                newitem.append(entity.label + ':' + entity.id)
                newitem.append(entity.label)
                for aliaes in entity.aliases:
                    newitem.append(aliaes)
                self._addItemToDict(dict_file, id, newitem)

        if entity.isVirtualObject():
            print("add a virtual object..")
            print("obj id:%s"%entity.getVirtualObjectId())
            newitem = []
            newitem.append(entity.label + ':' + entity.id + ':' + entity.getVirtualObjectId())
            newitem.append(entity.label)
            for aliaes in entity.aliases:
                newitem.append(aliaes)
            self._addItemToDict(self._getVirtualObjectFile(), id, newitem)



    def _getSubjectFile(self):
        return os.path.join(self.dict_dir, "test")

    def _getIndicatorsNormalFile(self):
        return os.path.join(self.dict_dir, "indicators_normal")

    def _getIndicatorsNumberFile(self):
        return os.path.join(self.dict_dir, "indicators_number")

    def _getIndicatorsObjectFile(self):
        return os.path.join(self.dict_dir, "indicators_object")

    def _getVirtualObjectFile(self):
        return os.path.join(self.dict_dir, "virtual_object")

    def _addItemToDict(self, file,  id, item):
        #erase the old line

        with open(file,"r",encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        with open(file,"w",encoding="utf-8") as f_w:
            for line in lines:
                if  id in line:
                    continue
                f_w.write(line)

            newline = ""
            for text in item:
                newline += text;
                newline +="          "
            f_w.write(newline)
            f_w.write('\n')

            f_w.close()

if __name__ == '__main__':
    #api = Wikiapi()
    #result = api.getwbentitiesByid("Q30")

    # Q42862 个人电脑客户端游戏
    service = UpdateService()
    #service.addEntityToDict("Q42862")
    service.getRecentChange()
    #service.getAllObject()


