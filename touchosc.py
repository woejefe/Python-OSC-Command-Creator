import tkinter as tk
from tkinter import ttk
from pythonosc import udp_client
from tkinter import simpledialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider
from tkinter.colorchooser import askcolor
from tkinter import Tk, filedialog
from PIL import Image, ImageTk

# OSC client setup
client = udp_client.SimpleUDPClient("127.0.0.1", 7001)
client2 = udp_client.SimpleUDPClient("127.0.0.1", 4559)  # Replace with your OSC server IP and port

# Add a new variable to keep track of edit mode
edit_mode = False

#define osc argument value for switching on and off
arg_value=0
    

# Add a new method to toggle edit mode
def toggle_edit_mode():
    global edit_mode
    edit_mode = not edit_mode
    update_button_color()

#Update Button Color definition/function
def update_button_color():
    if edit_mode:
        edit_button.config(bg='green',text='Edit Mode')  # Set button color to green when edit mode is true
    else:
        edit_button.config(bg='orange',text='Send mode')  # Set button color to red when edit mode is false    


# if in edit mode dont send osc, if not in edit mode send "object_name" as osc command
def send_osc_command(object_name, arg_value):  
    if edit_mode:
        print ("in edit mode.")
    else:
        osc_command = f"{object_name}"        
        client.send_message(osc_command, 1-arg_value)
        client2.send_message(osc_command, 1-arg_value)

#def my_object():
    #box=tk.Button(root, text=simpledialog.askstring("Name", "Enter:"), bg="blue", width=10, height=9)
    #box1=tk.Button(root, text=simpledialog.askstring("Name", "Enter:"), bg="blue", width=20, height=20)
    
     

def create_object():
    if edit_mode:
        object_name = input.get()
        object = tk.Button(root, text=simpledialog.askstring("Name Object", "Enter a name:"), bg="lightblue", width=5, height=2)
        object.bind("<Button-1>", lambda event: send_osc_command(object_name,arg_value))
        object.bind("<Button-3>", lambda event: send_osc_command(object_name,arg_value))
        object.bind("<ButtonRelease-1>", lambda event: send_osc_command(object_name,1-arg_value))
        object.bind("<B1-Motion>", move_object)  # Bind the motion event for dragging
        object.bind("<Button-2>", lambda event: edit_object(object))
        object.place(x=100, y=100)  # Set the initial position of the object              
    else:
        print("not in edit mode")

def move_object(event):
    if edit_mode:
        object = event.widget
        x = event.x_root - root.winfo_rootx() - object.winfo_width() // 2
        y = event.y_root - root.winfo_rooty() - object.winfo_height() // 2
        # Check if the new position is within the canvas boundaries
        if 0 <= x <= root.winfo_width() - object.winfo_width() and 0 <= y <= root.winfo_height() - object.winfo_height():
            object.place(x=x, y=y)  
    else:
        print("not in edit mode")                 

def edit_object(object):
    if edit_mode:       
        new_name = simpledialog.askstring("Edit Object", "Enter a new name:")
        if new_name:
            object.config(text=new_name)       
        new_width = simpledialog.askstring("Edit width", "Enter a new width:")
        if new_width:
            object.config(width=new_width)            
        new_height = simpledialog.askstring("Edit height", "Enter a new height:")
        if new_height:
            object.config(height=new_height)       
        new_color = askcolor(title="Tkinter Color Chooser")
        if new_color:
            object.config(bg=new_color[1])           
        confirmation = simpledialog.askstring("Delete Object", "Are you sure you want to delete object? (yes/no)")
        if confirmation and confirmation.lower() == "yes":
        # Code to delete the object
            print(f"Deleting {object}...")
            object.destroy()
        # Add your code to delete the object here
        else:
            print("Deletion canceled.")           
    else:
         print("not in edit mode")

# Create the main window
root = tk.Tk()
root.title("OSC command Send")


# Create the input menu
commands = ["/press/bank/1/1","/press/bank/1/2","/press/bank/1/3","/press/bank/1/4","/press/bank/1/5","/press/bank/1/6","/press/bank/1/7","/press/bank/1/8"]  # Add your object names here

input = ttk.Combobox(root, values=commands)
input.pack()

# Create the "Create Object" button
create_button = tk.Button(root, text="Create Button", command=create_object)
create_button.pack()

# Create the "Edit Mode" toggle
edit_button = tk.Button(root, text="Edit Mode",command=toggle_edit_mode)
edit_button.pack()

# Update the edit button color initially
update_button_color()


canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Start the Tkinter event loop
root.mainloop()
