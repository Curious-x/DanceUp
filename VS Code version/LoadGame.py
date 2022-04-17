class PlayerRecordClass:
    def __init__(self,Player_n,U_levels=1,s_list=[0]):
        self.Name=Player_n
        self.Levels=U_levels
        self.Scores=s_list


 
def Loadgame(filename):
    try:
        SavedFile=open(filename,"rt") 

        Name=SavedFile.readline().rstrip()
        Levels=int(SavedFile.readline().rstrip())
        Scores=[]
        for counter in range(Levels):
            Scores.append(int(SavedFile.readline().rstrip()))
        
        SavedFile.close()

    except: return None
    else: return PlayerRecordClass(Name,Levels,Scores)