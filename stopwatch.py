# Python program to illustrate a stop watch 
# using Tkinter 
#importing the required libraries 
import tkinter as Tkinter 
from datetime import datetime
counter = -3600
running = False
label   = None
f       = None
start   = None
stop    = None
reset   = None
def counter_label(label): 
    def count(): 
        if running: 
            global counter
            global label
   
            # To manage the initial delay. 
            if counter==-3600:             
                display="Starting..."
            else:
                tt = datetime.fromtimestamp(counter)
                string = tt.strftime("%H:%M:%S")
                display=string 
   
            label['text']=display   # Or label.config(text=display) 
   
            # label.after(arg1, arg2) delays by  
            # first argument given in milliseconds 
            # and then calls the function given as second argument. 
            # Generally like here we need to call the  
            # function in which it is present repeatedly. 
            # Delays by 1000ms=1 seconds and call count again. 
            label.after(1000, count)  
            counter += 1
   
    # Triggering the start of the counter. 
    count()      
   
# start function of the stopwatch 
def Start(label): 
    global running
    global start
    global stop
    global reset
    running=True
    counter_label(label) 
    start['state']='disabled'
    stop['state']='normal'
    reset['state']='normal'
   
# Stop function of the stopwatch 
def Stop(): 
    global running
    global start
    global stop
    global reset
    start['state']='normal'
    stop['state']='disabled'
    reset['state']='normal'
    running = False
   
# Reset function of the stopwatch 
def Reset(label): 
    global counter
    global reset
    counter=-3600
   
    # If rest is pressed after pressing stop. 
    if running==False:       
        reset['state']='disabled'
        label['text']='Diving start'
   
    # If reset is pressed while the stopwatch is running. 
    else:                
        label['text']='Starting...'

def Stopwatch(canva):
    """Return a StopWatch Widget."""
    
    global label
    global f
    global start
    global stop
    global reset
       
    # Fixing the window size.
    label = Tkinter.Label(canva, text="Diving start", fg="#688DBD", bg="#eff5f6", font="Verdana 30 bold") 
    label.pack() 
    f = Tkinter.Frame(canva, bg="#eff5f6",)
    start = Tkinter.Button(f, text='Start', bg="#eff5f6", command=lambda:Start(label))
    stop = Tkinter.Button(f, text='Stop',state='disabled', bg="#eff5f6", command=Stop)
    reset = Tkinter.Button(f, text='Reset', state='disabled', bg="#eff5f6", command=lambda:Reset(label))
    f.pack(anchor = 'center')
    start.pack(side="left")
    stop.pack(side ="left")
    reset.pack(side="left")
