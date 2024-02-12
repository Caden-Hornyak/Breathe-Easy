import csv
import json

class ReadData:

    def __init__(self, collective_dic):
        self.coldic = collective_dic
        self.dic = {}

    def read_csv(self, filepath, d_col):
        if self.coldic:
            curr_dic = self.dic
        else:
            curr_dic = {}

        f = open(filepath)
        datareader = csv.reader(f)

        for row in datareader:
            curr_dic[d_col] = 1

        return curr_dic


    def read_txt(self, filepath):
        if self.coldic:
            curr_dic = self.dic
        else:
            curr_dic = {}

        with open(filepath, 'r', encoding="mbcs") as f:
            for line in f:
                curr_dic[line.rstrip()] = 1
        
        return curr_dic


    def read_json(self, filepath, outername, d_field):
        if self.coldic:
            curr_dic = self.dic
        else:
            curr_dic = {}

        with open(filepath, 'r', encoding="mbcs") as f:
            d = json.load(f)

            for row in d[outername]:
                ele = row[d_field]
                curr_dic[ele] = 1