import tkinter
import winsound

from time import sleep
from tkinter import messagebox
from enum import Enum


#importing Game Modules
import LoadGame
import leaderboard
import SaveGame

#importing Classes
from LoadGame import PlayerRecordClass



#State Functions

def StartGame():
    """ It sets the Start Screen """


    #Change State
    global GameState
    GameState=State.SplashScreen

    #Setting image
    playground.create_image(400,250, image=SplashScreenImg, anchor="center",tag=State.SplashScreen)

    #Displaying text
    playground.create_text(WindowWidth//2,WindowHeight-40,text="Double Click to Continue!",anchor="center",font=("Helvetica",15),fill="#410069",tag=State.SplashScreen)
    playground.create_text(6,WindowHeight-6,text="Maximize screen now to maximize enjoyment!",anchor="sw",font=("Helvetica",10),fill="#410069",tag=State.SplashScreen)
    

def SetUser():
    """ It sets the Set User Screen """

    #Change State & Set Window Size    
    global GameState, WindowHeight, WindowWidth
    GameState= State.SetUser
    WindowHeight = playground.winfo_height()
    WindowWidth = playground.winfo_width()

    window.wm_minsize(height=WindowHeight-10,width=WindowWidth-10)
    window.wm_maxsize(height=WindowHeight,width=WindowWidth)

    #Clear Screen
    playground.delete(State.SplashScreen)
        
    #Setting Display
    playground.create_image(WindowWidth//2,WindowHeight//2, image=HomeScreenImg, anchor="center")

    EntryBox=tkinter.Entry(fg="#490069",font=("Helvetica",20),borderwidth=5,justify="center")
    Entry_window=playground.create_window(WindowWidth//2,WindowHeight//2-50,anchor="center",window=EntryBox,tag=State.SetUser)

    NewGameBtn=tkinter.Button(text="New Game",command=lambda:SetPlayer(EntryBox.get()),bg="white",fg="#490069",relief="raised",font=("Helvetica",15))
    NewGameBtn_window=playground.create_window(WindowWidth//2,WindowHeight//2,anchor="center",window=NewGameBtn,tag=State.SetUser)

    LoadGameBtn=tkinter.Button(text="Load Game",bg="white",fg="#490069",command=LoadGameWindow,relief="raised",font=("Helvetica",15))
    LoadGameBtn_window=playground.create_window(WindowWidth//2,WindowHeight//2+50,anchor="center",window=LoadGameBtn,tag=State.SetUser)

    EntryBox.insert(index=0, string="Enter your Name!")
    EntryBox.bind("<Button-1>",lambda e:EntryBox.delete(0,100))



def StartHome(PlayerX,IsPlayerUpdated=False):
    """
    PlayerX: Object of PlayerRecordClass
    IsPlayerUpdated: Boolean

    Set HomeScreen
    """


    #Change State
    global GameState
    GameState=State.Home

    #Clear Screen
    playground.delete(State.SetUser)
    playground.delete(State.LoadGame)

    #Def Functions:
    def NextSong(e):        
        PlayLevel[0]=Level(2)
        SongName.set(PlayLevel[0].name)
        SongRecord.set("Record\n"+str(PlayerX.Scores[PlayLevel[0].value-1]))

    def PrevSong(e):
        PlayLevel[0]=Level(1)
        SongName.set(PlayLevel[0].name)
        SongRecord.set("Record\n"+str(PlayerX.Scores[PlayLevel[0].value-1]))
    
    def Preview():
        winsound.PlaySound(f"Sound\\{PlayLevel[0].name}.wav", winsound.SND_ASYNC)

    def LetsPlay():
        PlayGame(playerX=PlayerX, p_level=PlayLevel[0],s_Setting=SongSettings[PlayLevel[0].value-1])

    def TrySave(FileName):
        IsSaved=SaveGame.savegame(filename=FileName.get(), Player=PlayerX)
        SaveGameWindow()
        if IsSaved:
            #As no progress is unsaved
            IsPlayerXUpdated[0]=False            
            messagebox.showinfo(title="Dance Up! | Saved",message="Your game is successfuly saved.")
        else:
            messagebox.showerror(title="Dance Up! | Unable to Save",message="No slot selected, so, Your game is not saved.")
        

    def InfoWindow():
        if OnScreen[0]==False:
            
            OnScreen[0]=True

            InfoFrame=tkinter.Frame(bg="white")
            InfoWindow=playground.create_window(20,80,anchor="nw",window=InfoFrame,tag="Info")

            tkinter.Label(InfoFrame,text="Click and Drag Ball!\nAlong the beat!",fg="white",bg="#c50059",font=("Helvetica",15),relief="flat").pack(expand=True,fill="both")

        else:
            playground.delete("Info")
            OnScreen[0]=False

    def LeaderBoardWindow():
        if OnScreen[1]==False:
            
            OnScreen[1]=True

            with open("DataFiles\LeaderBoard.txt") as FileVar:
                Records = FileVar.readlines()
    
            Records = [line.rstrip() for line in Records]
    
            leaders = []
            for Record in Records:
                leaders.append(Record.split())

            LeaderBoardFrame=tkinter.Frame(bg="#c50059")
            LeaderBoardWindow=playground.create_window(WindowWidth-20,80,anchor="ne",window=LeaderBoardFrame,tag="LeaderBoard")
            # tkinter.Label(LeaderBoardFrame,text="Test",bg="white",fg="#490069",font=("Helvetica",15),relief="flat").pack(expand=True,fill="both")
            tkinter.Label(LeaderBoardFrame,text="Beat",fg="white",bg="#c50059",font=("Helvetica",12,"bold"),relief="flat").grid(row=0,column=0)
            tkinter.Label(LeaderBoardFrame,text="Record",fg="white",bg="#c50059",font=("Helvetica",12,"bold"),relief="flat").grid(row=0,column=1)
            tkinter.Label(LeaderBoardFrame,text="Leader",fg="white",bg="#c50059",font=("Helvetica",12,"bold"),relief="flat").grid(row=0,column=2)

            for counter in range(1,len(leaders)+1):
                for index in range(len(leaders[counter-1])):
                    tkinter.Label(LeaderBoardFrame,text=leaders[counter-1][index],fg="white",bg="#c50059",font=("Helvetica",12),relief="flat",justify="center").grid(row=counter,column=index)
                    
                
            

        else:
            
            playground.delete("LeaderBoard")
            OnScreen[1]=False
        

    def SaveGameWindow():
        if OnScreen[2]==False:
            
            OnScreen[2]=True

            SaveGameFrame=tkinter.Frame(bg="white")
            SaveGameWindow=playground.create_window(20,WindowHeight-80,anchor="sw",window=SaveGameFrame,tag="SaveGame")

            FileName = tkinter.StringVar()

            with open("DataFiles\SlotsName.txt") as FileVar:
                SlotNames=[name.rstrip() for name in FileVar.readlines()]

            R1 = tkinter.Radiobutton(SaveGameFrame, text=SlotNames[0], variable=FileName,value="DataFiles\slot1.txt", indicator=0,fg="#490069",font=("Helvetica",12,"bold"),background="#c50059").pack(fill="x", ipady=5)
            R2 = tkinter.Radiobutton(SaveGameFrame, text=SlotNames[1], variable=FileName,value="DataFiles\slot2.txt", indicator=0,fg="#490069",font=("Helvetica",12,"bold"),background="#c50059").pack(fill="x", ipady=5)
            R3 = tkinter.Radiobutton(SaveGameFrame, text=SlotNames[2], variable=FileName,value="DataFiles\slot3.txt", indicator=0,fg="#490069",font=("Helvetica",12,"bold"),background="#c50059").pack(fill="x", ipady=5)
            R4 = tkinter.Radiobutton(SaveGameFrame, text=SlotNames[3], variable=FileName,value="DataFiles\slot4.txt", indicator=0,fg="#490069",font=("Helvetica",12,"bold"),background="#c50059").pack(fill="x", ipady=5)


            okaybutton=tkinter.Button(SaveGameFrame,text="OK",fg="#490069",font=("Helvetica",10),background="white",padx=10,pady=10,command=lambda:TrySave(FileName)).pack(fill="x", ipady=5)

        else:
            playground.delete("SaveGame")
            OnScreen[2]=False
    




    #Defining Variables
    IsPlayerXUpdated=[IsPlayerUpdated]
    PlayLevel=[Level(1)]
    SongName=tkinter.StringVar()
    SongName.set(PlayLevel[0].name)
    SongRecord=tkinter.StringVar()
    SongRecord.set("Recocrd\n"+str(PlayerX.Scores[PlayLevel[0].value-1]))
    #OnScreen=[IsInfo,IsLeader,IsSave]
    OnScreen=[False,False,False]



    
    #Especial Setting for different songs
    CollideSetting=SongSetting(Start_A=15, Start_V=55, Bar_V=1.3, BaseBarDetail=[0,150,500,50,10])
    SevenSetting=SongSetting(Start_A=2, Start_V=45, Bar_V=0.85, BaseBarDetail=[0,300,500,80,10])
    SongSettings=[CollideSetting,SevenSetting]





    #Seting Display
    playground.create_text(WindowWidth//2,20,text="Hello! "+PlayerX.Name,anchor="n",font=("Helvetica",25),fill="white",tag=State.Home)


    LeaderBoardBtn=tkinter.Button(text="Leader Board",command=LeaderBoardWindow,bg="#c50059",fg="white",relief="raised",font=("Helvetica",15))
    LeaderBoardBtn_window=playground.create_window(WindowWidth-20,20,anchor="ne",window=LeaderBoardBtn,tag=State.Home)

    InfoBtn=tkinter.Button(text="Info",command=InfoWindow,bg="#c50059",fg="white",relief="raised",font=("Helvetica",15))
    InfoBtn_window=playground.create_window(20,20,anchor="nw",window=InfoBtn,tag=State.Home)

    SaveGameBtn=tkinter.Button(text="Save Game",bg="#c50059",fg="white",command=SaveGameWindow,relief="raised",font=("Helvetica",15))
    SaveGameBtn_window=playground.create_window(20,WindowHeight-20,anchor="sw",window=SaveGameBtn,tag=State.Home)


    #Song Select
    SelectSongFrame=tkinter.Frame()
    SelectSongWindow=playground.create_window(WindowWidth//2,WindowHeight//2,anchor="center",window=SelectSongFrame,tag=State.Home)
    tkinter.Button(SelectSongFrame,textvariable=SongName,bg="#490069",fg="white",font=("Helvetica",15,"bold"),relief="raised",command=Preview).pack(ipadx=15,ipady=10,expand=True,fill="both")
    tkinter.Label(SelectSongFrame,textvariable=SongRecord,bg="white",fg="#c50059",font=("Helvetica",12),relief="flat").pack(ipady=5,expand=True,fill="both")

    #Play Button
    PlayBtn=tkinter.Button(text="Play!",bg="#490069",fg="white",relief="raised",font=("Helvetica",15),command=LetsPlay)
    PlayBtn_window=playground.create_window(WindowWidth//2,WindowHeight//2+150,anchor="n",window=PlayBtn,tag=State.Home)


    NextBtn=playground.create_polygon(WindowWidth//2+100,WindowHeight//2-50,WindowWidth//2+150,WindowHeight//2,WindowWidth//2+100,WindowHeight//2+50,fill="white",activefill="#490069",tag="NEXT")
    PrevBtn=playground.create_polygon(WindowWidth//2-100,WindowHeight//2-50,WindowWidth//2-150,WindowHeight//2,WindowWidth//2-100,WindowHeight//2+50,fill="white",activefill="#490069",tag="PREV")

    playground.tag_bind("NEXT","<Button-1>",NextSong)
    playground.tag_bind("PREV","<Button-1>",PrevSong)

    ExitGameBtn=tkinter.Button(text="EXIT",bg="#c50059",fg="white",command=lambda:ExitGame(not(IsPlayerXUpdated[0])),relief="raised",font=("Helvetica",12))
    ExitGameBtn_window=playground.create_window(WindowWidth-20,WindowHeight-20,anchor="se",window=ExitGameBtn,tag=State.Home)



def PlayGame(playerX,p_level,s_Setting):

    #Changing Game State
    global GameState
    GameState=State.PlayGame

    #Clear Screen
    playground.delete(State.Home)
    playground.delete("NEXT")
    playground.delete("PREV")
    playground.delete("LeaderBoard")
    playground.delete("SaveGame")
    playground.delete("Info")

    #Defining Local Functions
    def SetBarsFor(S_File):
        with open(S_File) as FileVar:
            DataList=FileVar.readlines()
        #Removing Trailing Characters
        DataList=[Data.rstrip() for Data in DataList]

        for Data in DataList:
            Detail=[int(detail) for detail in Data.split()]
            #Detail=[rel_x,rel_y,width,bounce_velocity]
            Bars.append(ClassBar(Detail[0], Detail[1], Detail[2], Detail[3],Detail[4]))
    
    def PlayNow(e):
        playground.delete("PlayNow")
        winsound.PlaySound(f"Sound\\{p_level.name}.wav", winsound.SND_ASYNC)    
        PlayBall.FreeFall()


    #Defining Variables
    CurrentScoreTXT=tkinter.IntVar()
    CurrentScoreTXT.set(0)
    BaseBar=s_Setting.BaseDetail


    #Setting Game
    Bars=[ClassBar(rel_x=BaseBar[0], rel_y=BaseBar[1]+20, w=BaseBar[2], bounce_v=BaseBar[3], acceleration=BaseBar[4])]
    SetBarsFor(f"DataFiles\\{p_level.name}.txt")

    PlayBall=BallClass(Player=playerX,PlayLevel=p_level,BaseBar=Bars[0], Start_V=s_Setting.Start_V, Start_a=s_Setting.Start_A, Bar_V=s_Setting.Bar_V,Bars=Bars,C_Score_TXT=CurrentScoreTXT)

    ScoreLabel=tkinter.Label(window,textvariable=CurrentScoreTXT,fg="#410069",bg="white",font=("Helvetica",20))
    Score_window=playground.create_window(WindowWidth//2,10,anchor="n",window=ScoreLabel,tag=State.PlayGame)
    
    OldScoreLabel=tkinter.Label(window,text="Your Record\n"+str(playerX.Scores[p_level.value-1]),fg="#410069",bg="white",font=("Helvetica",20))
    OldScore_window=playground.create_window(10,10,anchor="nw",window=OldScoreLabel,tag=State.PlayGame)

    PlayNowBtn=playground.create_polygon(WindowWidth//2-50,WindowHeight//2-50,WindowWidth//2+50,WindowHeight//2,WindowWidth//2-50,WindowHeight//2+50,fill="white",activefill="#490069",tag="PlayNow")
   
    playground.tag_bind("PlayNow","<Button-1>",PlayNow)



    



def EndGame(PlayerX,SongLevel,CurrentScore,IsWin):

    #Change Game State
    global GameState
    GameState=State.EndGame
    
    #Clear Screen
    playground.delete(State.PlayGame)
    playground.delete("Ball")
    playground.delete("Bar")

    #Definig Local Function
    def GoToHome():
        playground.delete(State.EndGame)
        StartHome(PlayerX=PlayerX,IsPlayerUpdated=IsPlayerXUpdated)

    #Defining Variables
    IsPlayerXUpdated=False

    #Processing Info

    if IsWin:
        WinMsg="You Danced Up the Beat!"
    else:
        winsound.PlaySound("Sound\oh_no.wav", winsound.SND_ASYNC)
        WinMsg= "Follow the beat to win the BEAT!"
    
    if CurrentScore>PlayerX.Scores[SongLevel.value-1]:
        PlayerX.Scores[SongLevel.value-1]=CurrentScore
        IsPlayerXUpdated=True
        PrimaryMsg="Hurray! New High-Score!"
    else:
        PrimaryMsg="Keep Playing, Keep Enjoying!"


    #Check if PlayerX is new leader
    IsRecordBroken,CurrentHighest=leaderboard.UpdateLeaderBoard(songx=SongLevel.name, scorex=CurrentScore, playerx=PlayerX.Name)
    
    if IsRecordBroken:
        SecondMsg="Congratulations! Now you are Leader of "+SongLevel.name+"!"
    else:
        SecondMsg="Leader of "+SongLevel.name+" score: "+str(CurrentHighest)


    #Setting Display
    playground.create_text(WindowWidth//2,40,text=WinMsg,anchor="n",font=("Helvetica",15,"bold"),fill="white",tag=State.EndGame)
    playground.create_text(WindowWidth//2,WindowHeight//2-40,text=PrimaryMsg,anchor="s",font=("Helvetica",15,"bold"),fill="white",tag=State.EndGame)
    playground.create_text(WindowWidth//2,WindowHeight//2,text="Score: "+str(CurrentScore),anchor="s",font=("Helvetica",20,"bold"),fill="white",tag=State.EndGame)
    playground.create_text(WindowWidth//2,WindowHeight//2+40,text=SecondMsg,anchor="n",font=("Helvetica",15,"bold"),fill="white",tag=State.EndGame)
    HomeBtn=tkinter.Button(text="Continue",command=GoToHome,bg="white",fg="#490069",relief="raised",font=("Helvetica",15,"bold"))
    InfoBtn_window=playground.create_window(WindowWidth//2,WindowHeight-20,anchor="s",window=HomeBtn,tag=State.EndGame)



    
    

    

#SubStates
def LoadGameWindow():
    global GameState
    if GameState==State.SetUser:
        GameState=State.LoadGame
        LGFrame=tkinter.Frame()
        LGWindow=playground.create_window(WindowWidth//2,WindowHeight//2+100,anchor="center",window=LGFrame,tag=State.LoadGame)
        playground.move(State.SetUser,0,-100)


        FileName = tkinter.StringVar()

        with open("DataFiles\SlotsName.txt") as FileVar:
            SlotNames=[name.rstrip() for name in FileVar.readlines()]

        R1 = tkinter.Radiobutton(LGFrame, text=SlotNames[0], variable=FileName,value="DataFiles\slot1.txt", indicator=0,bg="#490069",font=("Helvetica",12,"bold"),fg="#c50059").pack(fill="x", ipady=5)
        R2 = tkinter.Radiobutton(LGFrame, text=SlotNames[1], variable=FileName,value="DataFiles\slot2.txt", indicator=0,bg="#490069",font=("Helvetica",12,"bold"),fg="#c50059").pack(fill="x", ipady=5)
        R3 = tkinter.Radiobutton(LGFrame, text=SlotNames[2], variable=FileName,value="DataFiles\slot3.txt", indicator=0,bg="#490069",font=("Helvetica",12,"bold"),fg="#c50059").pack(fill="x", ipady=5)
        R4 = tkinter.Radiobutton(LGFrame, text=SlotNames[3], variable=FileName,value="DataFiles\slot4.txt", indicator=0,bg="#490069",font=("Helvetica",12,"bold"),fg="#c50059").pack(fill="x", ipady=5)


        okaybutton=tkinter.Button(LGFrame,text="OK",fg="#490069",font=("Helvetica",10),background="white",padx=10,pady=10,command=lambda:StartLoad(FileName)).pack(fill="x", ipady=5)

    elif GameState==State.LoadGame:
        GameState=State.SetUser
        playground.delete(State.LoadGame)
        playground.move(State.SetUser,0,100)

def ExitGame(IsProgressSaved):
    if IsProgressSaved:
        if messagebox.askyesno(title="Dance UP! | Bye Bye!", message="Do you want to exit?\n\nClick 'Yes' to exit or click 'No' to return to game.") :
            window.destroy()
    else:
        ExitAnyway=messagebox.askyesno(title="Dance UP! | Progress Unsaved", message="Your pogress is unsaved. Do you want to exit?\n\nClick 'Yes' to exit or click 'No' to return to game and save progress.")
        if ExitAnyway:
            window.destroy()




#Class Definations
class State(Enum):
    """Game States"""
    SplashScreen=1
    SetUser=2
    LoadGame=3
    Home=4
    PlayGame=5
    EndGame = 6


class Level(Enum):
	Collide = 1
	Seven = 2
	

class ClassBar:
    def __init__(self,rel_x,rel_y,w,bounce_v,acceleration):
        """
        rel_y: INT height of bar relative to base(start position), ref_Y
        rel_x: INT x coordinate of the centre of the bar relative to centre of the screen, ref_X
        w: INT width of th bar
        bounce_v: INT Velocity of the ball after it jumps of this bar
        """
        ref_Y=WindowHeight
        ref_X=int(WindowWidth//2)
        
        xy=((ref_X+rel_x-(w//2)),(ref_Y-rel_y),(ref_X+rel_x+(w//2)),(ref_Y-rel_y+5))

        self.Bar=playground.create_rectangle(xy,fill="Grey",tag="Bar")
        self.Bounce_V=-bounce_v
        self.Acc=acceleration
    
    

    def Activate(self):
        playground.itemconfig(self.Bar,fill="White")

class BallClass:
    def __init__(self,Player,PlayLevel,BaseBar,Start_V,Start_a,Bar_V,Bars,C_Score_TXT):
        self.PlayerX=Player
        self.level=PlayLevel

        self.Ball=playground.create_oval(WindowWidth//2,450,WindowWidth//2+20,470,fill="white",tag="Ball")
        self.ActiveBar = BaseBar
        self.ActiveBar.Activate()

        self.Velocity = -Start_V
        self.Acceleration=Start_a

        self.Bar_V=Bar_V
        self.Bars=Bars

        self.CurrentScoreTXT=C_Score_TXT
        self.CurrentScore=0
    
    def FreeFall(self):
        playground.move("Bar",0,self.Bar_V)
        acc=10
        dt=0.2
        
        dy=round(self.Velocity*dt,2)

        
        playground.move("Ball",0,dy)
                
        self.Velocity=round(((self.Acceleration*dt)+self.Velocity),2)
                
        BallCentre=(playground.bbox("Ball")[0]+playground.bbox("Ball")[2])/2
        BallBox=playground.bbox("Ball")
        BarBox=playground.bbox(self.ActiveBar.Bar)
      
        if self.Velocity>0 and BallBox[3]>BarBox[3] and BallBox[3]<BarBox[3]+20 and BallCentre>BarBox[0]and BallCentre<BarBox[2]:            
            self.Bounce()

        elif BallBox[3]<playground.winfo_height():
            window.after(10,self.FreeFall)
        else:
            EndGame(PlayerX=self.PlayerX, SongLevel=self.level, CurrentScore=self.CurrentScore, IsWin=False)

    def Bounce(self):

        self.Velocity=self.ActiveBar.Bounce_V
        self.Acceleration=self.ActiveBar.Acc
        playground.delete(self.ActiveBar.Bar)
        self.Bars.pop(0)

        try:
            self.ActiveBar=self.Bars[0]
            self.ActiveBar.Activate()
            self.CurrentScore += 20
            self.FreeFall()
        except:
            self.CurrentScore += 100
            EndGame(PlayerX=self.PlayerX, SongLevel=self.level, CurrentScore=self.CurrentScore, IsWin=True)

        finally:
            self.CurrentScoreTXT.set(self.CurrentScore)            


class SongSetting:
    def __init__(self,Start_A,Start_V,Bar_V,BaseBarDetail):
        self.Start_A=Start_A
        self.Start_V=Start_V
        self.Bar_V=Bar_V
        self.BaseDetail=BaseBarDetail
        
            




#Functions Definations

def SetPlayer(name,levels=2,scores=[0,0]):
    if len(name)!=0 and name!="Enter your Name!":
        name="_".join(name.split())
        Player=PlayerRecordClass(name,levels,scores)
        StartHome(Player)
    else:
        messagebox.showinfo(title="DanceUp! | No User Name",message="Enter your name to start new game!")

def StartLoad(FileName):
    Player=LoadGame.Loadgame(FileName.get())
    if Player!= None:
        StartHome(Player)
    else:
        #mean there is no saved data in slot slected
        messagebox.showinfo(title="DanceUp! | Empty Slot",message="There is no saved game in selected slot!")



#Binded Function Definations

def Continue(event):
    if GameState== State.SplashScreen: SetUser()

 
def move(e):
    if GameState==State.PlayGame:
        # my_image=my_canvas.create_image(e.x,e.y,anchor=NW,image=circle)
        playground.moveto("Ball",e.x)




#Define window
window=tkinter.Tk()
window.title("DANCE UP!")
window.iconbitmap("Graphics\DanceUp.ico")
window.geometry("800x500")
window.resizable(True,True)
window.wm_minsize(width=800,height=500)
# window.wm_maxsize(width=800,height=500)
# window.wm_minsize(width=500,height=500)

#Global Variable
WindowHeight=500
WindowWidth=800
GameState=None

#Global Resources
SplashScreenImg=tkinter.PhotoImage(file="Graphics\SplashScreen.png")
HomeScreenImg=tkinter.PhotoImage(file="Graphics\HomeScreen.png")

#Creating canvas
playground=tkinter.Canvas(window, width=800,height=500,background="white")
playground.pack(fill="both",expand=True)


#####################

StartGame()

#####################

# Binding Functions
playground.bind('<B1-Motion>',move)

window.bind('<Double 1>', Continue)


window.mainloop()