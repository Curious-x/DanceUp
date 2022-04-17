class LeaderClass:
    def __init__(self,R):
        [self.Song,self.Score,self.PlayerN]=R.split()



def UpdateLeaderBoard(songx,scorex,playerx):

    IsRecordBroken=False
    with open("DataFiles\LeaderBoard.txt") as FileVar:
        Records = FileVar.readlines()
    
    Records = [line.rstrip() for line in Records]
    

    for index in range(len(Records)):

        if Records[index].split()[0]==songx:
            if int(Records[index].split()[1])<scorex :
                Records[index]=songx + " " + str(scorex) + " " + playerx
                CurrentHighest=scorex
                IsRecordBroken=True
            else:
                CurrentHighest=int(Records[index].split()[1])
            break
        
    
    Records=[r +  "\n" for r in Records]
    
    with open ("DataFiles\LeaderBoard.txt", "w") as FileVar:
        FileVar.writelines(Records)

    return IsRecordBroken,CurrentHighest














