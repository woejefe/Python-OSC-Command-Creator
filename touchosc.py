import tkinter as tk
from tkinter import ttk
from pythonosc import udp_client
from tkinter import simpledialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider
from tkinter.colorchooser import askcolor

# OSC client setup
client = udp_client.SimpleUDPClient("127.0.0.1", 7001)
client2 = udp_client.SimpleUDPClient("127.0.0.1", 4559)  # Replace with your OSC server IP and port

# Add a new variable to keep track of edit mode
edit_mode = False

# Add a new method to toggle edit mode
def toggle_edit_mode():
    global edit_mode
    edit_mode = not edit_mode

def send_osc_command(object_name):
    # Replace with your OSC command format
    if edit_mode:
        print ("in edit mode.")
    else:
        osc_command = f"{object_name}"
        client.send_message(osc_command, 0)
        client2.send_message(osc_command, 0)

def create_object():
    if edit_mode:
        object_name = input.get()
        object = tk.Button(root, text=simpledialog.askstring("Name Object", "Enter a name:"), bg="lightblue", width=16, height=9)
        object.bind("<Button-1>", lambda event: send_osc_command(object_name))
        object.bind("<ButtonRelease-1>", lambda event: send_osc_command(object_name))
        object.bind("<B1-Motion>", move_object)  # Bind the motion event for dragging
        object.bind("<Button-3>", lambda event: edit_object(object))
        object.place(x=100, y=100)  # Set the initial position of the object
        objects.append(object)  # Add the object to the list
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
            
    else:
           print("not in edit mode")

        
        
# Create the main window
root = tk.Tk()
root.title("Object Selector")


# Create the input menu
objects = ["/press/bank/1/1","/press/bank/1/2","/press/bank/1/3","/press/bank/1/4","/press/bank/1/5","/press/bank/1/6","/press/bank/1/7","/press/bank/1/8"]  # Add your object names here
input = ttk.Combobox(root, values=objects)
input.pack()

# Create the "Create Object" button
create_button = tk.Button(root, text="Create Button", command=create_object)
create_button.pack()

# Create the "Edit Mode" toggle
edit_button = tk.Button(root, text="Edit Mode",command=toggle_edit_mode)
edit_button.pack()


canvas = tk.Canvas(root, width=1280, height=720, bg="white")
canvas.pack()

# Start the Tkinter event loop
root.mainloop()
