
#"subject"  "indicators_number" "indicators_object"  "indicators_normal"   "virtual_object"   "formula"   "conjunction"  "date_time"

class NLEntity:

    def __init__(self):
        self.text = None
        self.standard_text = None
        self.dict_text = None
        self.type = None
        self.name = None
        self.formula = None
        self.id = None
        self.hiden_object_id = None
        self.start = None
        self.end = None

    def __init__(self, text, dict_text, type, start, end):
        self.text = text
        self.dict_text = dict_text
        self.type = type
        self.name = None
        self.formula = None
        self.id = None
        self.hiden_object_id = None
        if (type == "virtual_object"):
            index = dict_text.rindex(':')
            self.hiden_object_id = dict_text[index+1:]
            tmp = dict_text[:index]
            index = tmp.rindex(':')
            self.id = tmp[index+1:]
        else:
            index = dict_text.rfind(':')
            if  index != -1:
                self.id = dict_text[index+1:]

        self.start = start
        self.end = end

    def setValue(self, key_val, complex_val):
        if complex_val is None:
            return
        self.dict_text = complex_val
        self.text = key_val
        item_list = complex_val.split(':')
        length = len(item_list)
        if length == 0:
            return

        # 第一个位置为type
        # 第二个位置为text
        if length > 1:
            self.type = item_list[0]
            self.standard_text = item_list[1]

        # 第三个位置为id
        if length > 2:
            self.id = item_list[2]

        # 第四个位置为hidden id
        if length > 3:
            self.hiden_object_id = item_list[3]

    def getJson(self):
        data_dict = {}
        data_dict["text"] = self.text
        data_dict["dict_text"] = self.dict_text
        data_dict["type"] = self.type
        data_dict["name"] = self.name
        data_dict["formula"] = self.formula
        data_dict["id"] = self.id
        data_dict["start"] = self.start
        data_dict["end"] = self.end
        data_dict["hiden_object_id"] = self.hiden_object_id

        return data_dict

    def hasFormula(self):
        return self.formula != None
