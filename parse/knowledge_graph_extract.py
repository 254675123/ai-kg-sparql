#coding=utf-8
import os
import sys
sys.path.append('./parse')
from parse.nlentity import NLEntity



class KnowledgeGraphExtract:
    def __init__(self, extract_manager=None):
        """
        :param extract_manager:
            extract_manager that enable subject extract for query
        :return:
        """
        self.extract_manager = extract_manager

    def  extract(self, query, file):
        dictionary = self.load(file)
        type = os.path.basename(file)
        entity_list = []
        # print len(self.dictionary)
        for key in dictionary:
            for value in dictionary[key]:
                index = query.find(value)
                end = index + len(value) - 1
                if index != -1:
                    entity = NLEntity(value,  key,  type,  index, end)
                    entity_list.append(entity)
                    break

        return entity_list

    # Subject Extract for query
    # return slot_value
    def load(self, dict_name):
        # print os.getcwd()
        company_dict = {}
        f = open(dict_name, 'r',encoding='UTF-8')
        lines = f.readlines()
        for line in lines:
            seg = line.strip().split()
            if len(seg):
                if seg[0] in company_dict.keys():
                    pass
                else:
                    company_dict[seg[0]] = []
                for index in  range(1, len(seg)):
                    company_dict[seg[0]].append(seg[index])
        f.close()

        return company_dict

    def extract_graph(self, query):
        #knowledge_graph_extract = intelligentDrawing.knowledge_graph_extract.KnowledgeGraphExtract()
        final_dict = []
        dict_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dict/lexicon_graph'))
        list = os.listdir(dict_dir)
        for i in range(0,len(list)):
            file_name = list[i]
            file_path = os.path.join(dict_dir,file_name)
            if os.path.isfile(file_path):
                result = self.extract(query, file_path)
                if len(result):
                    final_dict.extend(result)

        return final_dict


if __name__ == "__main__":
    knowparse = KnowledgeGraphExtract()
    final_dict = knowparse.extract_graph("腾讯的手游的竞品的营收")
    print(final_dict)
