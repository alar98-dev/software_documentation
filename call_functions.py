import json
import conection as con
from time import sleep


#VARIAVEL GLOBAL DE CONEXÃO

conec = con.con()


#para cada interação com o banco de dados vamos precisar de uma função no conection
class add_think:
    def __init__(self,function_call) -> None:
        
        #AQUI RECEBEMOS A FUNCTION CALL
        #print(function_call)
        #print("TESTANDO SE ESTA CHAMANDO O OBJETO CORRETO") #esta chamando o objeto
        data = json.loads(function_call.arguments)
        #print(data)
        conec.add_think(data=data)

        print("IDEIA ADICIONADA NO BANCO DE DADOS")

class add_project:
    def __init__(self,function_call,obj) -> None:
        data = json.loads(function_call.arguments)
        #print(data['functional_requirements'])
        #print(obj)
        conec.add_project(data=data)

        req = str(data['functional_requirements'])
        function_requeriments = req.split(';')

        for requeriment in function_requeriments:
            requeriment = requeriment.replace(".",'')
            if requeriment != "":
                if requeriment[0] == " ":
                    requeriment = requeriment[1:]
                conec.add_project_functional_requeriments(requeriment=requeriment,project_name=str(data['name']))
                #TESTE DE ENCAPSULAMENTO AVANÇADO
                obj.send_chat(prompt=F"NO PROJETO DE NOME {str(data['name'])} vamos construir o requisito funcional para o requisito {requeriment}")

        
        sys_req = str(data['system_requirements'])
        sys_nature = str(data['system_requirements_nature'])
        sys_type = str(data['system_requirements_type'])

        system_requeriments = sys_req.split(';')
        system_nature = sys_nature.split(";")
        system_type = sys_type.split(";")

        for requeriment,nature,type in zip(system_requeriments,system_nature,system_type):
            if requeriment != "":
                conec.add_project_system_requeriments(requeriment=requeriment,project_name=str(data['name']),nature=nature,type=type)

        obj.send_chat(prompt=f"Vamos usar o build_feasibility para esse projeto {data}")
        print("adicionado com sucesso")

class build_requirement:
    def __init__(self,function_call,obj) -> None:
        data = json.loads(function_call.arguments)

        print(data)
        print("TESTANDO O BUILD REQUIREMENT")
        conec.add_functional_description(requirement=data['requirement'],description=data['requirement_description'])

        rel = str(data['related_non-functional_requirements'])
        nat = str(data['nature_related_non-functional_requirements'])
        typ = str(data['type_related_non-functional_requirements'])

        related = rel.split(';')
        nature = nat.split(';')
        type = typ.split(';')

        print(F"AQUI ESTA O RELATED: {related}, aqui esta o nature {nature}, aqui esta o type {type}")
        #EDIATANDO AQUI 26/12/2024

        for related_functional,na,ty in zip(related,nature,type):
            print(f"AQUI ESTA O related:{related_functional}, a natureza: {na}, o tipo: {ty}")
            if related_functional != "":
                if related_functional[0] == " ":
                    related_functional = related_functional[1:]
                related_functional = related_functional.replace('.','')
                conec.build_requirement(project_name=data['project_name'],functional_requirements=data['requirement'],related_functional_requirements=related_functional,nature=na,type=ty)

class build_feasibility:
    def __init__(self,function_call,obj):
        
        print("INICIO BUILD FEASIBILITY - call_function")
        data = json.loads(function_call.arguments)
        print(data)
        
        #sleep(10)

        conec.add_feasibility(project_name=data['project_name'],deadline=data['deadline'],costs=data['costs'],restriction=data['restriction'],aspects=data['aspects'],scope=data['scope'],no_scope=data['no_scope'])