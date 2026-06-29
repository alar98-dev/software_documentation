import sqlite3
from datetime import datetime


class con:
    def __init__(self) -> None:
        self.con = sqlite3.connect('./db.db')
        self.cursor = self.con.cursor()

        self.__create_db()

    def __create_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS thinks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                coment TEXT NOT NULL,
                datetime TEXT NOT NULL
            )
                            ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                name TEXT NOT NULL,
                objective TEXT NOT NULL,
                target TEXT NOT NULL,
                coment TEXT NOT NULL,
                spornsors TEXT NOT NULL,
                users TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects_functional_requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                functional_requirements TEXT NOT NULL,
                description TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects_system_requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                system_requirements TEXT NOT NULL,
                nature TEXT NOT NULL,
                type TEXT NOT NULL
            )
        
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS related_non_functional_requirements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                functional_requirements TEXT NOT NULL,
                related_non_functional_requirements TEXT NOT NULL,
                nature TEXT NOT NULL,
                type TEXT NOT NULL
            )
        
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS feasibility (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                deadline TEXT NOT NULL,
                costs TEXT NOT NULL,
                restriction TEXT NOT NULL,
                aspects TEXT NOT NULL,
                scope TEXT NOT NULL,
                no_scope TEXT NOT NULL
            )
        
        ''')


        self.con.commit()
    
    def add_think(self,data):
        #print(data)
        
        self.cursor.execute('''
            INSERT into thinks (description,coment,datetime)
            VALUES (?,?,?)
        ''',(data["description"],data["coment"],str(datetime.now())[0:16])
            )
        
        self.con.commit()

    def add_project(self,data):
        print((data['description'],data['name'],data['objective'],data['target'],data['coment'],data['spornsors'],data['users']))

        print('INICIO DO ADD_PROJECT CONECTION')

        self.cursor.execute('''
            INSERT into projects (description,name,objective,target,coment,spornsors,users)
            VALUES (?,?,?,?,?,?,?)
        ''',(data['description'],data['name'],data['objective'],data['target'],data['coment'],data['spornsors'],data['users'])
        )

        

        print("FINAL CURSOR")



        self.con.commit()




        #MODULO ENCAMINHADO PARA A CHAMADA DE FUNÇÃO DEIXANDO A CONECTION SOMENTE PARA A INTERAÇÃO COM O BANCO DE DADOS
        #--------------------------------------------------------------------------------------------------------------

        #req = str(data['functional_requirements'])
        #des_req = str(data['functional_description'])
        #print(req)
        #print(req.split(';'))

        

        #function_requeriments = req.split(';')
        #description_requeriments = des_req.split(';')
        #function_requeriments = 'a'

        #print(function_requeriments)

        ###AQUI ESTAMOS ADICIONANDO O SISTEMA NO SISTEMA OS REQUISITOS FUNCIONAIS
        #print("CONSTRUÇÃO DOS METODO")
        
        #method = [self.add_project_functional_requeriments(requeriments) for requeriments in function_requeriments]
        #for requeriment in function_requeriments:
        #    #print(requeriment,data['name'])
        #    if requeriment != '':
        #        self.add_project_functional_requeriments(requeriment=requeriment,project_name=str(data['name']))


        #AQUI VAMOS ADICIONAR OS REQUISITOS SISTEMICOS NÃO FUNCIONAIS

        #sys_req = str(data['system_requirements'])

        #system_requeriments = sys_req.split(';')

        #for requeriment in system_requeriments:
        #    if requeriment != "":
        #        self.add_project_system_requeriments(requeriment=requeriment,project_name=str(data['name']))



        #--------------------------------------------------------------------------------------------------------
        #FINAL DO MODULO QUE FOI ENCAMINHADO PARA O CALL_FUNCTION

    def add_project_functional_requeriments(self,requeriment,project_name):
        print("AQUI ESTA O ", requeriment, project_name)
        
        print("CONSTRUINDO A QUERY")
        self.cursor.execute('''
            INSERT into projects_functional_requirements (project_name,functional_requirements)
            VALUES (?,?)
        ''',(project_name,requeriment)        
        )

        self.con.commit()

        print("QUERY DO REQUISITOS SALVA")

    def add_project_system_requeriments(self,requeriment,project_name,nature,type):
        print("AQUI ESTA O system requeriment", requeriment, project_name)
        
        print("CONSTRUINDO A QUERY")
        self.cursor.execute('''
            INSERT into projects_system_requirements (project_name,system_requirements,nature,type)
            VALUES (?,?,?,?)
        ''',(project_name,requeriment,nature,type)        
        )

        self.con.commit()

    def add_functional_description(self,requirement,description):
        #print("AQUI ESTA O NOME DO PROJETO",project_name)
        print("AQUI ESTA O NOME DO REQUISITO FUNCIONAL",requirement)
        #print("AQUI ESTA O REQUISITO RELACIONADO",related_functional)
        print("AQUI ESTA A DESCRIÇÃO DO REQUISITO", description)




        print("EXECUTANDO A QUERY")
        self.cursor.execute(f'''
            UPDATE projects_functional_requirements
            SET description = "{description}"
            WHERE functional_requirements = "{requirement}"
        ''')

        self.con.commit()
        print("QUERY SALVA")
        pass

    def build_requirement(self,project_name,functional_requirements,related_functional_requirements,nature,type):
        print("INICIO build_requirement - conection")
        self.cursor.execute(f'''
            INSERT into related_non_functional_requirements (project_name,functional_requirements,related_non_functional_requirements,nature,type)
            VALUES(?,?,?,?,?)
        ''',(project_name,functional_requirements,related_functional_requirements,nature,type)
        )

        self.con.commit()

        print("FINAL build_requirement - conection")

    def add_feasibility(self,project_name,deadline,costs,restriction,aspects,scope,no_scope):
        print("INICIO feasibility  - conection")
        self.cursor.execute(f'''
            INSERT into feasibility (project_name,deadline,costs,restriction,aspects,scope,no_scope)
            VALUES(?,?,?,?,?,?,?)
        ''',(project_name,deadline,costs,restriction,aspects,scope,no_scope)
        )

        self.con.commit()

        print("FINAL feasibility - conection")


#a = con()
#a.add_project_functional_requeriments(requeriment="CADASTRO DE USUARIO",project_name="Scambio")
#a.build_requirement(project_name="Sistema de Chamados Centralizado",requirement="Criar um painel de atendimento online com chat ao vivo",description=)