from csvObj import csv as table
import sqlparser
#s="import student.csv as st \n"
#o=sqlparser.SqlParser(s)
#print(o.parse ())
#file=open("script1.txt",'r')
#ss=table("student.csv")
class MainClaas:
    def __init__(self):
        self.tables=[]
        self.pycmd=''
    def compile(self,parsedcmd):
        pycmd = self.pycmd
        for cmd in parsedcmd:
            reserved=self.tables
            if (cmd[0] == 'import'):
                pycmd = pycmd + str(cmd[2]) + '= table("' + str(cmd[1])+'")\n'
                pycmd=pycmd+'reserved=reserved.append("'+str(cmd[2])+'")\n'
                self.data=reserved
            elif(cmd[0]=="select"):
                pycmd=pycmd+cmd[2]+'.select('+str(cmd)+')\n'
            elif (cmd[0] == "delete"):
                pycmd = pycmd + cmd[1] + '.delete(' + str(cmd[2]) + ')\n'
            elif (cmd[0] == "insert"):
                pycmd = pycmd + cmd[1] + '.insert(' + str(cmd) + ')\n'
        objectCode = compile(pycmd, 'pyGenCode.py', 'exec')
        print(pycmd)
        exec(objectCode)
        # tables = tables.update({cmd[2]: table(cmd[1])})

            #print(reserved)




            #print(type(tables['s']))
            #break


while(True):
    print("compile file_path")
    print("run file_path")
    command=input(">>>").strip()
    if(command[0]=='c'):
        path=command.split()[1]
        file=open(path, 'r')
        sql_cmd= file.read()
        #print(sql_cmd)
        parser=sqlparser.SqlParser(str(sql_cmd))
        m=MainClaas()
        m.compile(parser.parse())
           # print('error: invalid file')