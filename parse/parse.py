import copy
from parse.knowledge_graph_extract import KnowledgeGraphExtract
from parse.regulation.syntacticalRule import SyntacticalRule
from parse.regulation.statementStructure import *

class   Parse:

    # 通过句法规则解析
    def parseByRule(self, querystring):
        # 实例化存储自然语言对象
        statement_data = StatementStructure()
        statement_data.input_origin = querystring

        # 对自然语言进行分词处理
        statement_data.reverseMaxSegmentation()


        # for value in extract_dict:
        #     print(value.text)
        # print('\n')
        # extract_dict = self.resolveConflict(extract_dict)
        # print("去掉重复的分词以后的结果(e.g:产品营收   产品  营收)")
        # for value in extract_dict:
        #     print(value.text)
        # print('\n')
        # sorted_dict = self.sort(extract_dict)
        # print("排完序后的结果")

        sr = SyntacticalRule()
        # 使用语法规则进行合并
        merged_dict = sr.combineNode(sorted_dict)

        # 检查是否符合句式规则
        sr.checkStatement(merged_dict)

        return merged_dict


    def parse(self, querystring):
        knowparse = KnowledgeGraphExtract()
        extract_dict = knowparse.extract_graph(querystring)
        print("原始的分词结果")
        for value in  extract_dict:
            print(value.text)
        print('\n')
        extract_dict = self.resolveConflict(extract_dict)
        print("去掉重复的分词以后的结果(e.g:产品营收   产品  营收)")
        for value in  extract_dict:
            print(value.text)
        print('\n')
        sorted_dict = self.sort(extract_dict)
        print("排完序后的结果")
        for value in  sorted_dict:
            print(value.text)
        result_array = self.resolveVirtualObject(sorted_dict)
        result_array = self.resolveFormula(result_array)
        print("最终结果")
        for value in  result_array:
            print("type:%s,   value:%s"%(value.type, value.text))
        return result_array

    def sort(self, dict_array):
        tmp_array = dict_array
        result_array = []
        while len(tmp_array)  >  0:
            index = self._findMin(tmp_array)
            entity = tmp_array[index]
            result_array.append(entity)
            del tmp_array[index]

        return result_array

    def resolveVirtualObject(self, dict_array):
        result  = copy.deepcopy(dict_array)
        for i in  range(0, len(result)) [::-1] :
            if  i == (len(result) -1):
                continue

            entity =result[i]
            compare_entity = result[i+1]
            if  entity.type == "virtual_object" and (entity.hiden_object_id == compare_entity.id):
                del result[i+1]

        return result

    # can't support :腾讯的营收最大的产品的竞品有哪些
    def resolveFormula(self, dict_array):
        result  = copy.deepcopy(dict_array)
        for i in  range(0, len(result)) [::-1] :
            entity = result[i]
            if  entity.type == "formula":
                pre = i - 1
                ne = i + 1
                if  pre >=0 and pre < len(result):
                    pre_entity = result[pre]
                    if pre_entity.type == "indicators_number":
                        pre_entity.formula = entity.dict_text
                        result.remove(entity)

                if  ne >=0 and ne < len(result):
                    ne_entity = result[ne]
                    if ne_entity.type == "indicators_number":
                        ne_entity.formula = entity.dict_text
                        result.remove(entity)

        for i in  range(0, len(result)) [::-1] :
            entity = result[i]
            if  entity.hasFormula():
                index = self._findEntity(result,  i, "indicators_object")
                index_virtual = self._findEntity(result,  i, "virtual_object")
                final_index = -1
                if min(index, index_virtual) == -1:
                    final_index = max(index, index_virtual)
                else:
                    final_index = min(index, index_virtual)

                if final_index != -1:
                    result.insert(final_index + 1, entity)
                    del result[i]


        return result

    # remove the conflict entity:
    def  resolveConflict(self, dict):
        result  = copy.deepcopy(dict)
        for i in  range(0, len(result)) [::-1] :
            entity = result[i]
            for  j in range(0, len(result)) [::-1]:
                if  j != i:
                    compare_entity = result[j]
                    if  entity.start >= compare_entity.start and entity.start < compare_entity.end:
                        print("find conflict:%s         :       %s"%(entity.text, compare_entity.text))
                        if(len(entity.text) <= len(compare_entity.text)):
                            result.remove(entity)
                            print("remove:%s, type:%s"%(entity.text, entity.type))

        return result

    def _findMin(self, array):
        min_index = 0
        for i  in range(len(array) ):
            min_entity = array[min_index]
            entity = array[i]
            if  entity.start < min_entity.start:
                min_index = i

        return min_index

    def  _findEntity(self, dict_array, start, entity_type):
         for i in  range(start, len(dict_array)):
            entity = dict_array[i]
            if entity.type ==  entity_type:
                return i
         return -1

if __name__ == "__main__":
    parse = Parse()
    #result = parse.parse("腾讯的手机游戏的营收和mau")
    #result = parse.parse("腾讯的智能手机游戏产品的营收最大的竞品")
    result = parse.parse("腾讯的营收最大的产品的竞品有哪些")

    #print(parse.parse("腾讯的智能手机游戏产品的竞品的营收"))
