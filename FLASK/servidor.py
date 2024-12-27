from flask import Flask, render_template
import connection

#VARIAEVEIS GLOBIAS

#con = connection.con()

class project:
    def __init__(self,dados,con) -> None:
        
        self.id = dados[0]
        self.name = dados[2]
        self.description = dados[1]
        self.objective = dados[3]
        self.target = dados[4]
        self.coment = dados[5]
        self.functional_requirements = [functional_requirement(func,con) for func in con.funcitional_requirements_consult(project_name=self.name)]
        for func in self.functional_requirements:
            print(func.functional_requirement)
        self.spornsors = dados[6] #clientes/patrocinadores
        self.users = dados[7] #usuarios do sistema

        self.system_requiriments = [system_requiriment(data=sys) for sys in con.system_requirements_consult(project_name=self.name)]

        for s in self.system_requiriments:
            print(s.project_name,s.system_requirement)

        #AQUI VAMOS ADICIONAR A VIABILIDADE DO SISTEMA
        feasibility = con.feasibility_consult(self.name)[0]

        print(feasibility)

        self.deadline = feasibility[2]
        self.costs = feasibility[3]
        self.restriction = feasibility[4]
        self.aspects = feasibility[5]
        self.scope = feasibility[6]
        self.no_scope = feasibility[7]


class projetcs:
    def __init__(self) -> None:
        con = connection.con()
        self.projects = [project(proj,con=con) for proj in con.projects_consult()]
        #projects = con.projects_consult()

        #for proje in projects:
        #    a = project(proje)
        #    self.projects.append(a)
        for p in self.projects:
            print(p.name)

class functional_requirement:
    def __init__(self,data,con) -> None:
        self.id = data[0]
        self.project_name = data[1]
        self.functional_requirement = data[2]
        self.description = data[3]
        self.related_functional = [related_non_functional_requirement(data=related) for related in con.related_non_functional_requirements_consult(project_name=self.project_name,functional_requirement=self.functional_requirement)]
        for rela in self.related_functional:
            print(rela.related_non_functtional_requirement)

class system_requiriment:
    def __init__(self,data) -> None:
        self.id = data[0]
        self.project_name = data[1]
        self.system_requirement = data[2]
        self.nature = data[3]
        self.type = data[4]

class related_non_functional_requirement:
    def __init__(self,data) -> None:
        self.id = data[0]
        self.project_name = data[1]
        self.functional_requirement = data[2]
        self.related_non_functtional_requirement = data[3]
        self.nature = data[4]
        self.type = data[5]

        



app = Flask(__name__)

@app.route('/painel')
def painel():

    proj = projetcs()
    return render_template('painel.html',projects=proj)

@app.route('/projeto/<int:project_id>')
def project_detail(project_id):
    # Conectar-se ao banco de dados novamente
    con = connection.con()
    # Procurar o projeto específico
    proj = next((p for p in projetcs().projects if p.id == project_id), None)
    if proj:
        return render_template('projeto.html', project=proj)
    else:
        return "Projeto não encontrado", 404



if __name__ == "__main__":
    app.run(debug=True)