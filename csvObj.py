import pandas as pd
import operator
class csv :
    def __init__(self,path):
        self.path=path
        try:
            self.data =pd.read_csv(self.path)
            #print(self.data)
        except FileNotFoundError as ex:
            print(ex)


        print("#############################################################")
        #print(list(self.data.columns))
    def operator_fn(self,op):
        return {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '<=': operator.le,
            '>=': operator.ge,
            '<': operator.lt,
            '>': operator.gt,
            '=': operator.eq,
            '!=': operator.ne
        }[op]
    def savechanges(self):
       self.data.to_csv(self.path,index=False,encoding='utf8')

    def search_codition(self,df,condition):
        if(not(condition)):
            return self.data
        if(condition[0]=='and'):
            return pd.merge(self.search_codition(df,condition[1]),self.search_codition(df,condition[2]),how='inner')
        if(condition[0]=='or'):
            return pd.merge(self.search_codition(df, condition[1]), self.search_codition(df, condition[2]), how='outer')
        return df[self.operator_fn(condition[0])(df[condition[1]],condition[2])]

    def delete(self,condition):
        data = self.search_codition(self.data,condition)
        self.data=pd.concat([self.data, data]).drop_duplicates(keep=False)
        #print(data)
        #self.savechanges()
        print(self.data)



    def select(self,nodes):
        data = self.search_codition(self.data, nodes[3])
        if(nodes[4]):
            #order by nodes[4]
            data=data.sort_values(by=nodes[4])
        if(type(nodes[1]) is list):
            if(type(nodes[1][0])is int):
               names=list(self.data.columns)
               for i in range(len(nodes[1])):
                   nodes[1][i]=names[nodes[1][i]]
            data = data[nodes[1]]


       # print(data)
        return data


    def insert(self, nodes):
        if (type(nodes[2]) is list):

            #( list(self.data.columns))
            d= pd.DataFrame([nodes[2]], columns=list(self.data.columns)).drop_duplicates(keep="first")
            self.data = self.data.append(d)
        else:
            self.data = self.data.append(self.select(nodes[2])).drop_duplicates(keep="first")
        print(self.data)
        return self.data
#test area
#s=csv("student.csv")
#s.delete(('or', ('=', 'name','ahmed'), ('>', 'age', 20)))
#s.delete(('>', 'age', 33))
#print(s.select(('select', '*', 'student', None, None)))
#(s.select(('select', ['name', 'dept'], 'student', ('or', ('>', 'age', 30), ('=', 'name', 'dina')), 'name')))
#print(s.select(('select', [0,1], 'student', ('or', ('>', 'age', 30), ('=', 'name', 'dina')), 'name')))
#print(s.insert(('insert', 'ss', [7, 'omar', 'cs', 18])))
#print(s.insert(('insert', 'student', ('select', '*', 'student2', None, None))))