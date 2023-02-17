import pandas as pd
import os
import PySimpleGUI as sg
from WINDOW3 import window3
from WINDOW2 import window2

users_path = r"O:\613_OAE_BD\Relatorios\Treinamentos\Users.csv"

watched_videos_path = r"O:\613_OAE_BD\Relatorios\Treinamentos\watched_videos.csv"

# caminho para a pasta dos videos da 111
path_111 = "C:\\Treinamentos\\111"

# caminho para a pasta dos videos da 113
path_113 = "C:\\Treinamentos\\113"

# variavel que armazena o nome dos arquivos que estao na 111
p111 = os.listdir(path_111)

# variavel que armazena o nome dos arquivos que estao na 113
p113 = os.listdir(path_113)

# verifica se o usuario ja esta registrado no banco de dados
def is_registered(ID): #OK
    df = read_any_csv(users_path)
    x = df.loc[df["ID"] == ID]
    if x.empty:
        return False
    else:
        return True

# faz o cadastro do usuario
def register(ID,name,section,RE):  # OK
    global users_df  # need it to add to external variable 
    # com esse "global" nao precisa ler o csv de novo

    data = pd.DataFrame({'NAME': [name], 'ID': [ID], 'SECTION': [section], 'RE': [RE]})
    
    users_df = pd.concat([users_df, data])   # <-- add to original `users_df`

    users_df.to_csv(r"O:\613_OAE_BD\Relatorios\Treinamentos\Users.csv", index=False)

 # mostrar os videos ja assistidos
def already_watched(ID): #OK        
    df = read_any_csv(watched_videos_path)
    videos = df.loc[df["ID"] == ID,"LINK"] 
    return videos

# retorna os links que nao foram assistidos ainda
def videos_to_watch(section,ID): #OK        
    list_already_watched = already_watched(ID).tolist()
    if section == 111:
        list_to_watch = set(p111)-set(list_already_watched)
    elif section == 113:
        list_to_watch = set(p113)-set(list_already_watched)
    elif section == 000:
        list_to_watch = []
    return list(list_to_watch)  

# retorna setor do usuario
def current_user_section(df,ID):    
    current_user = df.loc[df["ID"] == ID]      	   
    section = int(current_user["SECTION"])
    return section

# retorna se a lista de videos a serem assistidos esta vazia ou nao
def is_list_empty(list,section,ID):
    list = videos_to_watch(section,ID)
    length = len(list)
    if length == 0:
        return True
    else:
        return False

# retorna o nome do usuario
def current_user_name(df,ID):
    current_user = df.loc[df["ID"] == ID]
    name = current_user["NAME"].to_string(index = False)
    return name

# retorna os dados do usuario -> nao da para ser essa funcao direto, pois ai o python nao consegue converte o section para int
def current_user_data(df,ID):
    name = current_user_name(df,ID)
    section = current_user_section(df,ID)
    return name,section

# faz a funcao read_csv do pandas
def read_any_csv(path): #OK
    df = pd.read_csv(path)
    return df

def window():

    global users_df

    # Definindo o fundo da tela como preto
    sg.theme('Black') 

    # Declarando o logo da mercedes
    myImg = sg.Image(filename='logo_meca_pret.png',size=(200,200))

    # Declarando os outputs
    output = sg.Text(font=("Arial",20),key="output") 
    output2 = sg.Text(font=("Arial",20),key="output2")
    output3 = sg.Text(font=("Arial",20),key="output3")    

    layout = [
            [myImg,sg.Text('PROGRAMA DE TREINAMENTOS',font=("Arial",35),justification="center")],
            [sg.Text("Passe o cracha no leitor: ",font=("Arial",20)),sg.InputText(size=(60),key="ID")],
            [sg.Text("Escreva seu nome:  ",font=("Arial",20),visible=False,key="NAMETEXT"),sg.InputText(size=(60),visible=False,key="NAME")],
            [sg.Text("Digite seu RE (sem ponto e barra): ",font=("Arial",20),visible=False,key="RETEXT"),sg.Input(size=(8),visible=False,key="RE")],
            [sg.Text("Digite seu setor(111/112/113): ",font=("Arial",20),visible=False,key="SECTIONTEXT"),sg.Input(size=(5),visible=False,key="SECTION")],
            [sg.Button('SubmitData', visible=False)],
            [output],
            [output2],
            [output3,sg.InputText(size=(1),key="w_a",visible=False)],           
            [sg.Text("CLIQUE AQUI E FECHE A JANELA",font=("Arial",20),visible=False,key="BOTAOERROR1"),sg.Text("CLIQUE NO BOTAO PARA ABRIR AS TELAS DOS TUTORIAIS",font=("Arial",20),visible=False,key="BOTAOW3"),sg.Button("W3",visible=False)],
            [sg.Text("CLIQUE NO BOTAO PARA ASSISTIR ALGUM TUTORIAL NOVAMENTE",font=("Arial",20),visible=False,key="BOTAOW5"),sg.Button("W5",size=(5),visible=False)],
            [sg.Button('Submit', visible=False, bind_return_key=True)],
            #[sg.Button("ERROR1",visible=False)],
    ]

    window = sg.Window('PROGRAMA DE TREINAMENTOS MERCEDES BENZ', layout,element_justification="center").Finalize()
    window.Maximize()

    while True:
        event, values = window.read()    

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        #print('You entered ', values[0])
        if event == 'Submit':    
            ID = values["ID"]  
            ID = ID.upper()              
        
        
        if is_registered(ID) == True:     
            if ID == "X":
                name,section = current_user_data(users_df,ID)
                window["BOTAOERROR1"].update(visible=True)
                #window["ERROR1"].update(visible=True) 
                window["W3"].update(visible=True)
            else:
                name,section = current_user_data(users_df,ID)
                output.update(f"Ola, {name}, bem vindo ao programa de treinamento Mercedes Benz Brasil!\n")
                videos = videos_to_watch(section,ID)
                if is_list_empty(videos,section,ID) == True:     
                    output2.update("Nao ha novos tutoriais disponiveis.")
                    output3.update("Deseja assistir algum tutorial novamente (S/N)?") 
                    window['w_a'].update(visible = True)       
                    w_a = values["w_a"]
                    if w_a == "s" or w_a == "S":
                        # abre a tela com todos os tutoriais da pasta daquela secao
                        window2(ID,section)   
                        window.find_element("ID").update("") 
                        window.find_element("output").update("")
                        window.find_element("output2").update("")
                        window.find_element("output3").update("") 
                        window.find_element("w_a").update("")
                        window['w_a'].update(visible = False)                                          

                    if w_a == "n" or w_a == "N":                         
                        # usa esses comandos para limpar a tela, para que um novo usuario use 
                            window.find_element("ID").update("") 
                            window.find_element("output").update("")
                            window.find_element("output2").update("")
                            window.find_element("output3").update("")                         
                            window['w_a'].update(visible = False) # deixa o input do w_a invisivel de novo
                           
                        
                 
                else:
                    # se tiverem videos a serem assistidos abrir a WINDOW3
                    window["BOTAOW3"].update(visible = True)
                    window["W3"].update(visible = True) 
                    if section == 113:
                        folder = p113
                    elif section == 111:
                        folder = p111
                    if len(videos_to_watch(section,ID)) != len(folder):
                        window["BOTAOW5"].update(visible = True)
                        window["W5"].update(visible=True)     
                
                          
                
                
        else:
            window["NAMETEXT"].update(visible = True)
            window["NAME"].update(visible = True)                                
            window["SECTIONTEXT"].update(visible = True)     
            window["SECTION"].update(visible = True)
            window["SubmitData"].update(visible = True)   
            window["RETEXT"].update(visible=True)
            window["RE"].update(visible=True)
        
        if event == "W5":
            window2(ID,section)

        # if event == "ERROR1":
        #      window3(ID,section)
        #      window.find_element("ID").update("") 
        #      window['BOTAOERROR1'].update(visible=False)
        #      window['ERROR1'].update(visible=False) 

        if event == 'SubmitData' :  
            name = values["NAME"]     
            name = name.title()      
            section = values["SECTION"]
            RE = values["RE"]
            output.update(f"Ola, {name}, bem vindo ao programa de treinamento Mercedes Benz Brasil!\n")                    
            register(ID,name,section,RE)  
            users_df = pd.read_csv(users_path)
            window["BOTAOW3"].update(visible = True)
            window["W3"].update(visible = True)      
            
        if event == "W3":           
            window3(ID,section)
            window.find_element("ID").update("") 
            window.find_element("output").update("")
            window.find_element("output2").update("")
            window.find_element("output3").update("") 
            window.find_element("w_a").update("")            
            window["W3"].update(visible = False)
            window["BOTAOW3"].update(visible = False)
            window["NAME"].update(visible = False)
            window["SECTION"].update(visible = False)
            window["NAMETEXT"].update(visible = False)
            window["SECTIONTEXT"].update(visible = False)
            window["SubmitData"].update(visible = False)
            window["W5"].update(visible = False)
            window["BOTAOW5"].update(visible = False)
            window["BOTAOERROR1"].update(visible=False)
            window["RETEXT"].update(visible=False)
            window["RE"].update(visible=False)

    window.close()  

users_df = pd.read_csv(users_path)
watched_videos_df = pd.read_csv(watched_videos_path)
window()

