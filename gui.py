from stopwatch    import Stopwatch
from tkinter      import *
from tkinter.font import BOLD
from PIL import Image
from datetime import *
import time

# Plot specific imports
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Initialize the MESSAGE_SENT_TIMER global variable.
MESSAGE_SENT_TIMER: int = 0

class Dashboard:
    def __init__(self, ssd1306, ws2812b, data):
        self.ssd1306 = ssd1306
        self.ws2812b = ws2812b
        self.data = data
        
        self.window = Tk()
        self.window.title('System Management Dashboard')
        self.window.geometry('1920x1080')
        self.window.state('normal')
        self.window.config(background='#FFFFFF') # Light blue background

        # Header with icy blue color
        self.header = Frame(self.window, bg='#243D5D') 
        self.header.place(x=0, y=0, width=1920, height=150) # Full width header

        #Heading
        self.heading = Label (self.window, text='SEAKU DASHBOARD', font=("", 25, "bold"), fg='#ffffff', bg='#243D5D')
        self.heading.place (x=50, y=15)

        # Content area with grey background
        self.content = Frame(self.window, bg='#FFFFFF')
        self.content.place(x=0, y=60, width=1920, height=1020) # Full width and height below header
        
        # Statistics block within the content area
        self.statistics_frame = Frame(self.content, bg='#eff5f6')
        self.statistics_frame.place(x=50, y=50, width=1800, height=900)

        # Grid layout for statistics blocks
        self.statistics_frame.grid_rowconfigure(0, weight=2)
        self.statistics_frame.grid_rowconfigure(1, weight=1)
        self.statistics_frame.grid_rowconfigure(2, weight=1)
        self.statistics_frame.grid_rowconfigure(3, weight=1)
        self.statistics_frame.grid_rowconfigure(4, weight=1)
        self.statistics_frame.grid_rowconfigure(5, weight=1)
        self.statistics_frame.grid_rowconfigure(6, weight=2)
        self.statistics_frame.grid_columnconfigure(0, weight=1)
        self.statistics_frame.grid_columnconfigure(1, weight=2)
        self.statistics_frame.grid_columnconfigure(2, weight=2)
        self.statistics_frame.grid_columnconfigure(3, weight=1)
        self.statistics_frame.grid_columnconfigure(4, weight=1)
        self.statistics_frame.grid_columnconfigure(5, weight=1)
        self.statistics_frame.grid_columnconfigure(6, weight=1)
        self.statistics_frame.grid_columnconfigure(7, weight=1)
        
        # ONGOING DIVE BLOCK
        self.block_ongoing = Canvas(self.statistics_frame, bg='#688DBD', bd=0, highlightthickness=0)
        self.block_ongoing.grid(row=1, column=7, padx=15, pady=15)
        self.block_ongoing.create_rectangle(0, 0, 300, 100, fill='#688DBD', outline='#688DBD', width=0)
        
        self.ongoing_label = Label(self.block_ongoing, text="ONGOING", bg='#688DBD', fg='#FF0000', font=("Helvetica", 20, BOLD))
        self.ongoing_label.place(x=15, y=15)
        
        self.ongoing_label = Label(self.block_ongoing, text="MISSION DIVE IN THE FUTURE", bg='#688DBD', fg='#FFFFFF', font=("Helvetica", 14, BOLD))
        self.ongoing_label.place(x=15, y=60)

        # Statistics blocks 1
        self.stat_block1 = Canvas(self.statistics_frame, bg='#688DBD', bd=0, highlightthickness=0)
        self.stat_block1.grid(row=0, column=0, padx=15, pady=15)
        self.stat_block1.create_rectangle(0, 0, 300, 100, fill='#688DBD', outline='#688DBD', width=0)
        
        # Create a StringVar to assign to the stat_value1 and stat_value1bis Labels to be created.
        self.stat_value1_var = StringVar()
        self.stat_value1_var.set("Heart Rate")
        self.stat_value1bis_var = StringVar()
        self.stat_value1bis_var.set("O2%")

        self.stat_label1 = Label(self.stat_block1, text="Heart & O2 rate:", bg='#688DBD', fg='#243D5D', font=("Helvetica", 20, BOLD))
        self.stat_label1.place(x=15, y=15)
        self.stat_value1 = Label(self.stat_block1, textvariable=self.stat_value1_var, bg='#688DBD', fg='#ffffff', font=("Helvetica", 30))
        self.stat_value1.place(x=15, y=65)
        self.stat_value1bis = Label(self.stat_block1, textvariable=self.stat_value1bis_var, bg='#688DBD', fg='#ffffff', font=("Helvetica", 30))
        self.stat_value1bis.place(x=15, y=110)

        self.stat_block2 = Canvas(self.statistics_frame, bg='#688DBD', bd=0, highlightthickness=0)
        self.stat_block2.grid(row=2, column=0, padx=15, pady=15)
        self.stat_block2.create_rectangle(0, 0, 300, 100, fill='#688DBD', outline='#688DBD', width=0)

        # Create a StringVar to assign to the stat_value2 and stat_value2bis Labels to be created.
        self.stat_value2_var = StringVar()
        self.stat_value2_var.set("Pressure")
        self.stat_value2bis_var = StringVar()
        self.stat_value2bis_var.set("Altitude")

        self.stat_label2 = Label(self.stat_block2, text="Pressure & Altitude:", bg='#688DBD', fg='#243D5D', font=("Helvetica", 20, BOLD))
        self.stat_label2.place(x=15, y=15)
        self.stat_value2 = Label(self.stat_block2, textvariable=self.stat_value2_var, bg='#688DBD', fg='#ffffff', font=("Helvetica", 30))
        self.stat_value2.place(x=15, y=65)
        self.stat_value2 = Label(self.stat_block2, textvariable=self.stat_value2bis_var, bg='#688DBD', fg='#ffffff', font=("Helvetica", 30))
        self.stat_value2.place(x=15, y=110)

        self.stat_block3 = Canvas(self.statistics_frame, bg='#688DBD', bd=0, highlightthickness=0)
        self.stat_block3.grid(row=1, column=0, padx=15, pady=15)
        self.stat_block3.create_rectangle(0, 0, 300, 100, fill='#688DBD', outline='#688DBD', width=0)

        # Create a StringVar to assign to the stat_value3 Label to be created.
        self.stat_value3_var = StringVar()
        self.stat_value3_var.set("Temperature")

        self.stat_label3 = Label(self.stat_block3, text="Temperature:", bg='#688DBD', fg='#243D5D', font=("Helvetica", 20, BOLD))
        self.stat_label3.place(x=15, y=15)
        self.stat_value3 = Label(self.stat_block3, textvariable=self.stat_value3_var, bg='#688DBD', fg='#ffffff', font=("Helvetica", 30))
        self.stat_value3.place(x=15, y=65)

        self.stat_block4 = Canvas(self.statistics_frame, bg='#688DBD', bd=0, highlightthickness=0)
        self.stat_block4.place(x=490, y=50, width=820, height=380)
        #self.stat_block4.grid(row=1, columnspan=1, padx=10, pady=10)

        self.stat_label4 = Label(self.stat_block4, text="Temperature-Time Graph", bg='#688DBD', fg='#243D5D', font=("Helvetica", 20, BOLD))
        self.stat_label4.place(x=15, y=15)
        
        self.stat_block5 = Canvas(self.statistics_frame, bg='#688DBD', bd=0, highlightthickness=0)
        self.stat_block5.place(x=490, y=465, width=820, height=380)
        #self.stat_block4.grid(row=1, columnspan=1, padx=10, pady=10)

        self.stat_label5 = Label(self.stat_block5, text="Diver Profile", bg='#688DBD', fg='#243D5D', font=("Helvetica", 20, BOLD))
        self.stat_label5.place(x=15, y=15)
        
        
        # Create the temperature/pressure figures and plots
        temperature_fig = Figure(figsize=(5, 4), dpi=100)
        pressure_fig = Figure(figsize=(5, 4), dpi=100)
        self.temperature_plot_ax = temperature_fig.add_subplot(111)
        self.pressure_plot_ax = pressure_fig.add_subplot(111)

        # Initialize the plots lists.
        self.plot_x = []
        self.temperature_plot_y = []
        self.pressure_plot_y = []

        # Plot the data
        self.temperature_plot_ax.plot(self.plot_x, self.temperature_plot_y)
        self.pressure_plot_ax.plot(self.plot_x, self.pressure_plot_y)

        # Create a canvas containing the temperature figure
        self.temperature_plot_canvas = FigureCanvasTkAgg(temperature_fig, master=self.stat_block4)
        self.temperature_plot_canvas.draw()
        
        # Create a canvas containing the pressure figure
        self.pressure_plot_canvas = FigureCanvasTkAgg(pressure_fig, master=self.stat_block5)
        self.pressure_plot_canvas.draw()

        # Place the canvas on the Tkinter window
        self.temperature_plot_canvas.get_tk_widget().place(x=20, y=70, width=700, height=250)
        self.pressure_plot_canvas.get_tk_widget().place(x=20, y=70, width=700, height=250)

        # Statistic block with entry and submit button
        self.stat_block_with_entry = Canvas(self.statistics_frame, bg='#688DBD', bd=0, highlightthickness=0)
        self.stat_block_with_entry.grid(row=2, column=7, padx=10, pady=10)
        self.stat_block_with_entry.create_rectangle(0, 0, 300, 100, fill='#688DBD', outline='#688DBD', width=0)
        
        # Customized Entry Box
        self.entry_widget = Entry(self.stat_block_with_entry, bg='#FFFFFF', fg='#000000', font=("Helvetica", 14), width=30)
        self.stat_block_with_entry.create_window(180, 100, window=self.entry_widget)
        
        self.label_widget = Label(self.stat_block_with_entry, text="Chat Box", bg='#688DBD', fg='#243D5D', font=("Helvetica", 20, BOLD))
        self.label_widget.place(x=15, y=15)
        
        self.emergency_label = Label(self.stat_block_with_entry, text="EMERGENCY", bg='#688DBD', fg='#FF0000', font=("Helvetica", 20, BOLD))
        self.emergency_label.place(x=15, y=45)

        # Customized Submit Button
        def submit_data():
            # Make the MESSAGE_SENT_TIMER global variable writable.
            global MESSAGE_SENT_TIMER
            
            # Retrieve the input from the user.
            text: str = self.entry_widget.get()
            
            # Clear the entry widget after data is submitted
            self.entry_widget.delete(0, END)

            # Transmit the message to the ssd1306 screen once processed.
            texts: typing.List[str] = []
            tmp: str
            while True:
                if len(text) <= 20:
                    texts.append(text.strip())
                    break
                tmp = text[:20]
                if not tmp.endswith(' '):
                    if ' ' not in tmp:
                        text = text[20:]
                        texts.append(tmp.strip())
                        continue
                    tmp = ' '.join(tmp.split(' ')[:-1])
                    text = text[len(tmp):]
                    texts.append(tmp.strip())
                else:
                    text = text[len(tmp):]
                    texts.append(tmp.strip().strip())
            
            # Initialize a lineno variable.
            lineno: int = 0
            
            # If the ssd1306 device is busy, wait for it to be not busy anymore.
            while self.ssd1306.is_busy:
                pass
            
            # Set the ssd1306 as busy.
            self.ssd1306.is_busy = True
            
            # Clear the screen.
            self.ssd1306.clear()
            
            # Write the obtained texts.
            for text_ in texts:
                if lineno == 4:
                    # Wait 5 seconds for the display's content to be read.
                    time.sleep(5)

                    # Clear the display.
                    self.ssd1306.clear()
                    lineno = 0
                # Write the text_ content and increment the lineno variable.
                self.ssd1306.write(text_.strip(), 0, 15*lineno)
                lineno += 1
            
            # Set the global variable MESSAGE_SENT_TIMER to 5.
            MESSAGE_SENT_TIMER = 5
            
            # Set the ssd1306 as not busy anymore.
            self.ssd1306.is_busy = False
            
            # Show a "message sent" message on the GUI.
            self.submit_value_var.set("Message sent")
            self.after(3000, lambda: self.submit_value_var.set(""))

        self.submit_button = Button(self.stat_block_with_entry, text='Submit', command=submit_data, bg='#243D5D', fg='#FFFFFF', font=("Helvetica", 14), activebackground='#FF8A00')
        self.stat_block_with_entry.create_window(285, 165, window=self.submit_button)
        
        # Create a StringVar to assign to the submit_value Label to be created.
        self.submit_value_var = StringVar()
        self.submit_value_var.set("")
        
        self.submit_value = Label(self.stat_block_with_entry, textvar=self.submit_value_var, bg='#688DBD', font=("Helvetica", 14))
        self.submit_value.place(x=55, y=175)
        
        # Stopwatch block
        self.stopwatch_block = Canvas(self.statistics_frame, bg="#eff5f6", bd=0, highlightthickness=0)
        self.stopwatch_block.grid(row=0, column=7, padx=15, pady=15)
        self.stopwatch_block.create_rectangle(0, 0, 300, 100, fill='#eff5f6', outline='#eff5f6', width=0)
        
        # Ad the Stopwatch to the stopwatch block.
        Stopwatch(self.stopwatch_block)
    
    def update_plots(self):
        """Update the plots of the temperature/pressure over time."""
        
        # Update the plot X.
        self.plot_x.append(datetime.now())
        if len(self.plot_x) == 101:
            self.plot_x = self.plot_x[1:]
        
        # Update the temperature plot Y.
        self.temperature_plot_y.append(self.data["temperature"])
        if len(self.temperature_plot_y) == 101:
            self.temperature_plot_y = self.temperature_plot_y[1:]

        # Update the pressure plot Y.
        self.pressure_plot_y.append(self.data["pressure"])
        if len(self.pressure_plot_y) == 101:
            self.pressure_plot_y = self.pressure_plot_y[1:]
        
        # Update and re-draw the canvas.
        self.temperature_plot_ax.plot(self.plot_x, self.temperature_plot_y)
        self.pressure_plot_ax.plot(self.plot_x, self.pressure_plot_y)
        self.temperature_plot_canvas.draw()
        self.pressure_plot_canvas.draw()
    
    def update_data(self):
        """Update the data received from the sensors through the data dictionary."""
        
        # Update the StringVars.
        self.stat_value1_var.set(f"""{self.data["heart_rate"]} BPM""")
        self.stat_value1bis_var.set(f"""{self.data["O2_rate"]} 02%""")
        self.stat_value2_var.set(f"""{self.data["pressure"]} bar""")
        self.stat_value2bis_var.set(f"""{self.data["altitude"]} m""")
        self.stat_value3_var.set(f"""{self.data["temperature"]} °C""")
        
        if self.emergency_label is not None:
            self.emergency_label.place_forget()
            self.emergency_label = None

        time.sleep(0.5)
        
        # If the LED strip is in emergency mode, show up the associated Label.
        if self.ws2812b.is_emergency:
            self.emergency_label = Label(self.stat_block_with_entry, text="EMERGENCY", fg="#FF0000", bg='#FF8A00', font=("Helvetica", 20, BOLD))
            self.emergency_label.place(x=15, y=45)

        
    def mainloop(self):
        """Wrapper method to access self.window.mainloop."""
        self.window.mainloop()
        
    def after(self, time_ms, func):
        """Wrapper method to access self.window.after."""
        self.window.after(time_ms, func)

# d = Dashboard(None, None, None)
# d.mainloop()
