
_PROPERTY_VIRTUAL_OBJECT = "P111"

class WikiEntity:
    def __init__(self, id, jsonobj):
        self.id =  id
        self.jsonobj = jsonobj
        obj = jsonobj[id]
        self.type = obj["type"]
        #self.label = obj["labels"]["zh-cn"]["value"]
        labels = obj["labels"]
        if "zh-cn" in labels:
            self.label = labels["zh-cn"]['value']
        else:
            self.label = ""

        self.aliases = []
        aliases = obj["aliases"]
        if "zh-cn" in aliases:
            aliasescn = aliases["zh-cn"]
            for alias in aliasescn:
                self.aliases.append(alias["value"])

        #wikibase-item, quantity
        if "datatype" in obj:
            self.datatype = obj['datatype']
        else:
            self.datatype = ""

        self.claims = obj["claims"]


    def hasProperty(self, id):
        return id in self.claims

    def  isNumberProperty(self):
        return self.datatype == "quantity"

    def isObjectProperty(self):
        return self.datatype ==  "wikibase-item"

    def isNormalProperty(self):
        return self.datatype !=  "wikibase-item" and self.datatype !=  "quantity"

    def isVirtualObject(self):
        return self.hasProperty(_PROPERTY_VIRTUAL_OBJECT)

    def getVirtualObjectId(self):
        if self.isVirtualObject() != True:
            return ""

        vitualclaim = self.claims[_PROPERTY_VIRTUAL_OBJECT]
        if len(vitualclaim) > 0:
            id = vitualclaim[0]["mainsnak"]["datavalue"]["value"]['id']
            return id

        return ""
