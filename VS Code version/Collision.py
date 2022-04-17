import tkinter

def Movement():
    global xspeed,yspeed

    xy=playground.bbox(Ball)

    if xy[0]<0 or xy[2]>w:
        xspeed=-xspeed
    if xy[1]<0 or xy[3]>h:
        yspeed=-yspeed
       

    playground.move(Ball,xspeed,yspeed)
    root.after(30,Movement)

def Movement2():
    global xspeed2,yspeed2,xspeed,yspeed

    xy=playground.bbox(Ball2)
    xyObstacle=playground.bbox(Ball)

    if xy[1]<xyObstacle[3] and xy[3]>xyObstacle[1]:

        if xy[2]>xyObstacle[0] and  abs(xy[2]-xyObstacle[0])<10:
            xspeed2=-xspeed2
            xspeed=-xspeed
            print("Colision1")

        if xy[0]<xyObstacle[2] and abs(xy[0]-xyObstacle[2])<10  :
            xspeed2=-xspeed2
            xspeed=-xspeed
            print("Colision2")

    if xy[0]<xyObstacle[2] and xy[2]>xyObstacle[0]:
        if xy[3]>xyObstacle[1] and  abs(xy[3]-xyObstacle[1])<10:
            yspeed2=-yspeed2
            yspeed=-yspeed

        if xy[1]<xyObstacle[3] and abs(xy[1]-xyObstacle[3])<10  :
            yspeed2=-yspeed2
            yspeed=-yspeed

    if xy[0]<0 or xy[2]>w:
        xspeed2=-xspeed2
    if xy[1]<0 or xy[3]>h:
        yspeed2=-yspeed2
       

    playground.move(Ball2,xspeed2,yspeed2)
    root.after(30,Movement2)


root = tkinter.Tk()
root.geometry("800x500")
w=800
h=500

playground=tkinter.Canvas(root)
playground.pack(expand=True,fill="both")

Ball=playground.create_oval(w//2,h//2+100,w//2+50,h//2+50+100,fill="black")
xspeed=-10
yspeed=5

Ball2=playground.create_oval(w//2,h//2,w//2+50,h//2+50,fill="red")
xspeed2=10
yspeed2=-5

Movement()
Movement2()

root.mainloop()