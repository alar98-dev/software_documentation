import sqlite3

class con:
    def __init__(self) -> None:
        self.con = sqlite3.connect('../db.db')
        self.cursor = self.con.cursor()

    def projects_consult(self):
        self.cursor.execute('''
            SELECT * FROM projects
        '''
        )
        res = self.cursor.fetchall()
        return res
    
    def funcitional_requirements_consult(self,project_name):
        self.cursor.execute(f'''
            SELECT * FROM projects_functional_requirements
            WHERE project_name = "{project_name}"
    ''')
        
        res = self.cursor.fetchall()
        print(res)

        return res
    
    def related_non_functional_requirements_consult(self,project_name,functional_requirement):
        self.cursor.execute(f'''
            SELECT * FROM related_non_functional_requirements
            WHERE project_name =  "{project_name}" AND functional_requirements = "{functional_requirement}"
        ''')

        res = self.cursor.fetchall()

        return res
    
    def system_requirements_consult(self,project_name):
        self.cursor.execute(F'''
            SELECT * FROM projects_system_requirements
            WHERE project_name = "{project_name}"
        ''')

        res = self.cursor.fetchall()

        return res
    
    def feasibility_consult(self,project_name):
        self.cursor.execute(f'''
            SELECT * FROM feasibility
            WHERE project_name = "{project_name}"
                            ''')
        
        res = self.cursor.fetchall()
        return res

    
#a = con()
#print(a.projects_consult())