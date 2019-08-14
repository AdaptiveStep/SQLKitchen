from tkinter import *

root = Tk()
root2 = Tk()


root.title("Simple GUI")
root.geometry("200x100")
app = Frame(root)
app2 = Frame(root2)

app2.grid()
app.grid()

bttn2 = Button(app2)
bttn2.configure(text = "testing button")


lbl = Label(app,text="im a label")

lbl.grid()
bttn2.grid()
root2.mainloop()
root.mainloop()
