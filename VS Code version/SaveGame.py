class PlayerRecordClass:
    def __init__(self,Player_n,U_levels,s_list):
        self.Name=Player_n
        self.Levels=U_levels
        self.Scores=s_list

def savegame(filename,Player):
    list_of_lines = []
    list_of_lines.append(Player.Name)
    list_of_lines.append(str(Player.Levels))
    list_of_lines.extend([str(s) for s in Player.Scores])
    # Introducing new line character
    list_of_lines = [line + "\n" for line in list_of_lines]
    try:
        SavegameFile = open(filename, "w")
        SavegameFile.writelines(list_of_lines)

        SavegameFile.close()
    except:
        return False
        
    else:
        with open("DataFiles\SlotsName.txt") as FileVar:
            SlotNames=[name.rstrip() for name in FileVar.readlines()]

        SlotNames[int(filename[14])-1]=Player.Name
        SlotNames=[Name+"\n" for Name in SlotNames]

        with open("DataFiles\SlotsName.txt","w") as FileVar:
            FileVar.writelines(SlotNames)

        return True


