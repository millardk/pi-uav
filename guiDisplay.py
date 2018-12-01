import tkinter
import random
import time
import threading


class Screen:
    def __init__(self, master):
        self.masterGui = master

        frameLeft = tkinter.Frame(master)
        frameLeft.pack(side="left")
        frameRight = tkinter.Frame(master)
        frameRight.pack(side="right")

        self.altitude = 0
        self.speed = 0
        self.degrees = 0
        self.randomStat = 0
        self.controllerIP = "129.82.44.147"
        self.droneIP = "129.82.44.148"
        self.inFlight = False
        self.getData = False
        self.flightTime = 0

        self.droneLabel = tkinter.Label(frameLeft, text="Drone IP: " + self.droneIP, relief="sunken", anchor="center")
        self.droneLabel.pack()

        self.controlLabel = tkinter.Label(frameLeft, text="Controller IP: " + self.controllerIP, relief="sunken",
                                          anchor="s")
        self.controlLabel.pack()

        self.altitudeScale = tkinter.Scale(frameLeft, label="Altitude(FEET)", orient="horizontal", length=200)
        self.altitudeScale.pack()

        self.speedScale = tkinter.Scale(frameLeft, label="Speed(MPH)", orient="horizontal", length=200)
        self.speedScale.pack()

        self.degreesScale = tkinter.Scale(frameLeft, label="Degrees", orient="horizontal", length=200, to=360)
        self.degreesScale.pack()

        self.randomScale = tkinter.Scale(frameLeft, label="Random Stat 1", orient="horizontal", length=200)
        self.randomScale.pack()

        self.logButton = tkinter.Button(frameLeft, text="Log Stats", command=self.setLogStats)
        self.logButton.pack(side="left")

        self.exitButton = tkinter.Button(frameLeft, text="Exit GUI", command=master.quit)
        self.exitButton.pack(side="right")

        self.statusLabel = tkinter.Label(frameLeft, text="Grounded...", relief="sunken", anchor="s")
        self.statusLabel.pack(side="bottom", fill="x")

        self.canvas0 = tkinter.Canvas(frameRight, bg="black", height=300, width=300)
        self.canvas0.pack()

        self.canvas0.create_arc(15, 15, 285, 285, start=0, extent=180, fill="blue")
        self.canvas0.create_arc(15, 15, 285, 285, start=180, extent=180, fill="brown")
        self.canvas0.create_line(15, 150, 285, 150, width=3, fill="white")

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

        if self.inFlight:
            self.statusLabel.config(text="In Flight...")
        else:
            self.statusLabel.config(text="Grounded...")
        self.altitude = random.randint(0, 100)
        self.altitudeScale.set(self.altitude)

        self.speed = random.randint(0, 100)
        self.speedScale.set(self.speed)

        self.degrees = random.randint(0, 360)
        self.degreesScale.set(self.degrees)

        self.randomStat = random.randint(0, 100)
        self.randomScale.set(self.randomStat)
        self.flightTime += 1
        if self.getData:
            print("%5d\t%5d\t%8d\t%6d"%(self.flightTime, self.speed, self.altitude, self.degrees))
            #str(self.flightTime) + "\t" + str(self.speed) + "\t" + str(self.altitude) + "\t\t" + str(self.degrees)
        self.masterGui.after(1000, self.updateScreen)


def runGui():
    gui = tkinter.Tk()
    gui.title("Drone Display")
    guiScreen = Screen(gui)
    gui.mainloop()


def main():
    t = threading.Thread(target=runGui)
    t.start()


if __name__ == "__main__":
    main()
