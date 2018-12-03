import tkinter
import random
import time
import threading
import socket

altitude = 0
speed = 0
degrees = 0
randomStat = 0
controllerIP = socket.gethostbyname(socket.gethostname())
leftStickPosition = [0,0]
rightStickPosition = [0,0]
droneIP = "129.82.44.148"
guiInMotion = True
class Screen:
    def __init__(self, master):
        self.masterGui = master

        frameLeftStick = tkinter.Frame(master)
        frameLeftStick.pack(side="left")
        
        frameRightStick = tkinter.Frame(master)
        frameRightStick.pack(side="right")
        
        frameStats = tkinter.Frame(master)
        frameStats.pack(side="bottom")
        
        frameAttitudeInd = tkinter.Frame(master)
        frameAttitudeInd.pack(side="left")
        
        self.flightTime = 0
        self.getData = False
        
        self.droneLabel = tkinter.Label(frameStats, text="Drone IP: " + droneIP, relief="sunken", anchor="center")
        self.droneLabel.pack()

        self.controlLabel = tkinter.Label(frameStats, text="Controller IP: " + controllerIP, relief="sunken", anchor="s")
        self.controlLabel.pack()

        self.altitudeScale = tkinter.Scale(frameStats, label="Altitude(FEET)", orient="horizontal", length=300, to=1000)
        self.altitudeScale.pack()

        self.speedScale = tkinter.Scale(frameStats, label="Speed(MPH)", orient="horizontal", length=300)
        self.speedScale.pack()

        self.degreesScale = tkinter.Scale(frameStats, label="Degrees", orient="horizontal", length=300, to=360)
        self.degreesScale.pack()

        self.randomScale = tkinter.Scale(frameStats, label="Random Stat 1", orient="horizontal", length=300)
        self.randomScale.pack()

        self.logButton = tkinter.Button(frameStats, text="Log Stats", command=self.setLogStats)
        self.logButton.pack(side="left")

        self.exitButton = tkinter.Button(frameStats, text="Exit GUI", command=self.masterGui.quit)
        self.exitButton.pack(side="right")

        self.statusLabel = tkinter.Label(frameStats, text="Grounded...", relief="sunken", anchor="s")
        self.statusLabel.pack(side="bottom", fill="x")

        self.canvas0 = tkinter.Canvas(frameLeftStick, height=300, width=300)
        self.canvas0.pack()
        
        self.canvas0.create_oval(45, 45, 260, 260, fill="black")
        self.leftStick = self.canvas0.create_oval(75, 75, 225, 225, fill="grey")
        self.canvas0.create_text(150, 295,text="Left Stick")
        
        self.canvas2 = tkinter.Canvas(frameAttitudeInd, height=300, width=300)
        self.canvas2.pack()
        self.canvas2.create_arc(15, 15, 285, 285, start=0, extent=180, fill="blue")
        self.canvas2.create_arc(15, 15, 285, 285, start=180, extent=180, fill="brown")
        self.canvas2.create_line(15, 150, 285, 150, width=3, fill="white")

        self.canvas1 = tkinter.Canvas(frameRightStick, height=300, width=300)
        self.canvas1.pack()
        
        self.canvas1.create_oval(45, 45, 260, 260, fill="black")
        self.rightStick = self.canvas1.create_oval(75, 75, 225, 225, fill="grey")
        self.canvas1.create_text(150, 295,text="Right Stick")
        
        self.updateScreen()

    def setLogStats(self):
        if not self.getData:
            self.getData = True
            self.logButton.config(text="Stop Stats")
            print("Time\tSpeed\tAltitude\tDegree")
        else:
            print("End of stats!!")
            self.logButton.config(text="----", state="disabled")
            self.getData = False

    def updateScreen(self):
        if speed > 0:
            self.statusLabel.config(text="In Flight...")
        else:
            self.statusLabel.config(text="Grounded...")
        
        self.altitudeScale.set(altitude)
        self.speedScale.set(speed)
        self.degreesScale.set(degrees)
        self.randomScale.set(randomStat)
        
        self.canvas0.coords(self.leftStick, 75 + (leftStickPosition[0]*60), 75 + (-leftStickPosition[1]*60), 225 + (leftStickPosition[0]*60), 225 + (-leftStickPosition[1]*60))
        self.canvas1.coords(self.rightStick, 75 + (rightStickPosition[0]*60), 75 + (-rightStickPosition[1]*60), 225 + (rightStickPosition[0]*60), 225 + (-rightStickPosition[1]*60))
        
        self.flightTime += 0.5
        if self.getData and (self.flightTime).is_integer():
            print("%3.2f\t%5d\t%8d\t%6d"%(self.flightTime, speed, altitude, degrees))
            #str(self.flightTime) + "\t" + str(self.speed) + "\t" + str(self.altitude) + "\t\t" + str(self.degrees)
        self.masterGui.after(500, self.updateScreen)


def runGui():
    global guiInMotion
    gui = tkinter.Tk()
    gui.title("Drone Display")
    guiScreen = Screen(gui)
    gui.mainloop()
    guiInMotion = False

def changeValues():
    global altitude, speed, degrees, randomStat, leftStickPosition, rightStickPosition
    time.sleep(5)
    while guiInMotion:
        altitude = random.randint(0, 1000)
        speed = random.randint(0, 100)
        degrees = random.randint(0, 360)
        randomStat = random.randint(0, 100)
        leftStickPosition[0] = random.uniform(-1,1)
        leftStickPosition[1] = random.uniform(-1,1)
        rightStickPosition[0] = random.uniform(-1,1)
        rightStickPosition[1] = random.uniform(-1,1)
        time.sleep(0.5)
    
def main():
    guiThread = threading.Thread(target=runGui)
    controlThread = threading.Thread(target=changeValues)
    controlThread.start()
    guiThread.start()
    
if __name__ == "__main__":
    main()
    
