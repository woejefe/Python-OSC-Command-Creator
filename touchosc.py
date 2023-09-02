import tkinter as tk
from tkinter import ttk
from pythonosc import udp_client
from tkinter import simpledialog


# OSC client setup
client = udp_client.SimpleUDPClient("127.0.0.1", 4559)  # Replace with your OSC server IP and port



def send_osc_command(object_name):
    # Replace with your OSC command format
    osc_command = f"/object/{object_name}/pressed"
    client.send_message(osc_command, 0)

def create_object():
    object_name = input.get()
    object = tk.Button(root, text=object_name, bg="lightblue", width=10, height=5)
    object.bind("<Button-1>", lambda event: send_osc_command(object_name))
    object.bind("<B1-Motion>", move_object)  # Bind the motion event for dragging
    object.bind("<Button-3>", lambda event: edit_object(object))
    object.place(x=100, y=100)  # Set the initial position of the object
    objects.append(object)  # Add the object to the list

def move_object(event):
    object = event.widget
    x = event.x_root - root.winfo_rootx() - object.winfo_width() // 2
    y = event.y_root - root.winfo_rooty() - object.winfo_height() // 2
    # Check if the new position is within the canvas boundaries
    if 0 <= x <= canvas.winfo_width() - object.winfo_width() and 0 <= y <= canvas.winfo_height() - object.winfo_height():
        object.place(x=x, y=y)             
                 

def edit_object(object):
    new_name = simpledialog.askstring("Edit Object", "Enter a new name:")
    if new_name:
        object.config(text=new_name)

# Create the main window
root = tk.Tk()
root.title("Object Selector")

# Create the input menu
objects = []  # Add your object names here
input = ttk.Combobox(root, values=objects)
input.pack()

# Create the "Create Object" button
create_button = tk.Button(root, text="Create Object", command=create_object)
create_button.pack()

canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
canvas.pack()

# Start the Tkinter event loop
root.mainloop()
