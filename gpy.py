import openai
import os
import call_functions
import json

#VARIAVEIS GLOBAIS

with open("./api_key.txt",'r') as arq:
    api_key = arq.read()

#functions = []

class gpt:
    def __init__(self) -> None:
        self.object = self
        self.client = openai.Client(api_key=api_key)
        self.model = "gpt-4-turbo"
        self.prompts = []
        

        #CARRECAR AS PERSONAS
        with open('./PERSONAS/friendly.json', 'r') as arq:
            self.persona = arq.read()

        self.functions = []
        self.names_functions = []

        for filename in os.listdir('./CALL FUNCTIONS/'):
            print(filename)
            with open(f"./CALL FUNCTIONS/{filename}", 'r') as arq:
                self.names_functions.append(filename[:-5]) #ADICIONA O NOME DA FUNÇÃO NA VARIAVEL
                
                self.functions.append(json.loads(arq.read()))
                #print(self.names_functions)
        

    def send_chat(self,prompt):
        self.completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {'role': 'system', 'content':f'{self.persona},{self.prompts}'},
                {"role": 'user','content': f'{prompt}'}
            ],
            functions=self.functions,
            #function_call='auto'
        )

        self.prompts.append(prompt)


        if self.completion.choices[0].finish_reason == "function_call":
            function_call = self.completion.choices[0].message.function_call
            res_function = function_call.name
            print("TOKENS DE ENTRADA",self.completion.usage.prompt_tokens)
            print('TOKENS DE RESPOSTA' , self.completion.usage.completion_tokens)
            print("TOKENS TOTAL", self.completion.usage.total_tokens)
            #print(res_function)
            try:
                attr = getattr(call_functions,res_function)
                b = attr(function_call,self.object)
                text = "FUNÇÃO CHAMADA"
            except:
                print("FALHA NA CONTRUÇÃO DO OBJETO FUNCTION")
                text = "FALHA NA CONTRUÇÃO DA CHAMADA DE OBJETO"
        else:
            res_function = self.completion.choices[0].finish_reason
            text = self.completion.choices[0].message.content

        print('nome da função retornada',res_function)
        return text
    

class build_requiriment_functional:
    def __init__(self) -> None:
        pass

#a = gpt()
#a.send_chat("criar um sistema de shorts do que esta escrito na wikipedia")