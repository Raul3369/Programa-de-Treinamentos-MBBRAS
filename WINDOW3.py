import PySimpleGUI as sg
import os
import pandas as pd
import cv2
from ffpyplayer.player import MediaPlayer
from datetime import datetime,date 
from WINDOW2 import window2

# caminho para o arquivo "watched_videos.csv"
watched_videos_path = r"O:\613_OAE_BD\Relatorios\Treinamentos\watched_videos.csv"

# caminho para a pasta dos videos da 111
path_111 = "C:\\Treinamentos\\111"

# caminho para a pasta dos videos da 113
path_113 = "C:\\Treinamentos\\113"

# variavel que armazena o nome dos arquivos que estao na 111
p111 = os.listdir(path_111)

# variavel que armazena o nome dos arquivos que estao na 113
p113 = os.listdir(path_113)

def play_video(path):
  # Create a VideoCapture object and read from input file
      cap = cv2.VideoCapture(path)
      player = MediaPlayer(path)

      video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
      
      #deixar o video em fullscreen

      cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
      cv2.setWindowProperty("Frame",cv2.WND_PROP_FULLSCREEN ,cv2.WINDOW_FULLSCREEN)
        
      # Check if camera opened successfully
      if (cap.isOpened()== False): 
        print("Error opening video  file")

      # fara a contagem dos frames dos videos    
      counter = 0

      # Read until video is completed
      while(cap.isOpened()):
            
        # Capture frame-by-frame
        ret, frame = cap.read()
        audio_frame, val = player.get_frame()
        if ret == True:
        
          # Display the resulting frame
          cv2.imshow('Frame', frame)
        
          # Press Q on keyboard to  exit
          if cv2.waitKey(25) & 0xFF == ord('q'):
            break

          if val != 'eof' and audio_frame is not None:
            #audio
            img, t = audio_frame
        
        # Break the loop
        else: 
          break
        
        counter +=1

      # When everything done, release 
      # the video capture object
      cap.release()
        
      # Closes all the frames
      cv2.destroyAllWindows()
      return counter,video_length

# funcao que abre arquivos .ppsx e .pdf
def open_pdf_ppsx(path):
    #method 1    
    os.system(path)

# retorna a data atual
def get_date():
  today = date.today()
  date_str = today.strftime("%d/%m/%Y")
  return date_str

# retorna o horario atual
def get_time():
  time = datetime.now().time()
  time_str = time.strftime("%H:%M")
  return time_str

# registra no watched_videos.csv o video que acabou de ser assistido
def update_already_watched(path,ID): #OK
    global watched_videos_df
    name = os.path.split(path)[1]
    date = get_date()
    time = get_time()
    data = pd.DataFrame({'LINK': [name], 'ID': [ID],'DATE':[date],'TIME':[time]})
    watched_videos_df = pd.concat([watched_videos_df, data])   # <-- add to original `users_df`
    watched_videos_df.to_csv(r"O:\613_OAE_BD\Relatorios\Treinamentos\watched_videos.csv", index=False)

# retorna se a lista de videos a serem assistidos esta vazia ou nao
def is_list_empty(list,section,ID):
    list = videos_to_watch(section,ID)
    length = len(list)
    if length == 0:
        return True
    else:
        return False 

# retorna se a lista de videos ja assistidos esta vazia ou nao
def is_already_watched_empty(ID):
    list = already_watched(ID).tolist()
    length = len(list)
    if length == 0:
        return True
    else:
        return False 

# retorna os links que nao foram assistidos ainda
def videos_to_watch(section,ID): #OK        
    list_already_watched = already_watched(ID).tolist()
    if section == 111:
        list_to_watch = set(p111)-set(list_already_watched)
    elif section == 113:
        list_to_watch = set(p113)-set(list_already_watched)
    return list(list_to_watch)  

 # mostrar os videos ja assistidos
def already_watched(ID): #OK        
    df = read_any_csv(watched_videos_path)
    videos = df.loc[df["ID"] == ID,"LINK"] 
    return videos

# faz a funcao read_csv do pandas
def read_any_csv(path): #OK
    df = pd.read_csv(path)
    return df

def window3(ID,section):
    # Outputs da tela

    output = sg.Text(font=("Arial",20),key="output",visible=False) 
    output2 = sg.Text(font=("Arial",20),key="output",visible=False) 
    output3 = sg.Text("ERROR!! FECHE A TELA!!",font=("Arial",40),key="output3",visible=False)#,text_color="Red")

    # fazendo o layout da tela
    sg.theme('Black')

    myImg = sg.Image(filename='logo_meca_pret.png',size=(200,200))

    if section == 111:
      path = path_111
    elif section == 113:
      path = path_113

    tutorials = {filename.split('.')[0]:filename for filename in videos_to_watch(section,ID)}

    column_layout = [[sg.Button(text, enable_events=True, expand_x=True, key=text)] for text in tutorials]

    layout = [
            [myImg,sg.Text('PROGRAMA DE TREINAMENTOS',font=("Arial",35),justification="center")],
            [sg.Text("TREINAMENTOS",font=("Arial",40))],       
            [sg.Column(column_layout,scrollable=True,visible=True,vertical_scroll_only=True,key="Column")],     
            [output],
            [output2],
            [output3],
            [sg.Text("Clique no botao para assistir algum tutorial novamente!",font=("Arial",20),visible=False,key="ButtonTxt"),sg.Button('',visible=False, key = "W2",size=(5))],
            [sg.Button('Submit', visible=False, bind_return_key=True)]
    ]

    window = sg.Window('PROGRAMA DE TREINAMENTOS MERCEDES BENZ', layout,element_justification="center").Finalize()
    window.Maximize()


    while True:
        event, values = window.read()

        pd.read_csv(watched_videos_path)

        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

        if is_already_watched_empty(ID) == False:
          window["ButtonTxt"].update(visible = True)
          window['W2'].update(visible = True)

        if event == "W2":
          window2(ID,section)

        if event in tutorials:           
            output.update(visible=False)
            fullpath = path + '\\' + tutorials[event]
            file_name_without_extension = tutorials[event].split('.')[0]
            file_name_extension = '.' + tutorials[event].split('.')[1]
            if file_name_extension == ".ppsx" or file_name_extension == ".pdf":
                  open_pdf_ppsx(fullpath)
                  window[file_name_without_extension].update(visible=False)
                  update_already_watched(fullpath,ID)
                  output.update(f"Parabens, voce concluiu o tutorial {file_name_without_extension}!",visible=True)
                  videos = videos_to_watch(section,ID)
                  if is_list_empty(videos,section,ID) == True:
                    output2.update("Nao ha novos tutoriais disponiveis. Feche a janela!",visible=True)
            if file_name_extension == ".mov" or file_name_extension == ".mp4":
              counter, video_length = play_video(fullpath)
              if counter == video_length: 
                  window[file_name_without_extension].update(visible=False)
                  update_already_watched(fullpath,ID)
                  output.update(f"Parabens, voce concluiu o tutorial {file_name_without_extension}!",visible=True)
                  videos = videos_to_watch(section,ID)
                  if is_list_empty(videos,section,ID) == True:
                    output2.update("Nao ha novos tutoriais disponiveis. Feche a janela!",visible=True)
              elif counter != video_length:
                  output.update("Voce nao concluiu o video, por favor assista novamente.")
           
            
                     
                
        
    window.close()  


watched_videos_df = pd.read_csv(watched_videos_path)

