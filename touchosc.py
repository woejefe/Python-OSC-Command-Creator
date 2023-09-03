import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import Tk, filedialog,messagebox,simpledialog,ttk
from pythonosc import udp_client
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider
from PIL import Image, ImageTk


# OSC client setup
client = udp_client.SimpleUDPClient("127.0.0.1", 7001)
client2 = udp_client.SimpleUDPClient("127.0.0.1", 4559)  # Replace with your OSC server IP and port

# Add a new variable to keep track of edit mode
edit_mode = False

#define osc argument value for switching on and off
arg_value=0

# Create the input menu
commands = ["/press/bank/1/1","/press/bank/1/2","/press/bank/1/3","/press/bank/1/4","/press/bank/1/5","/press/bank/1/6","/press/bank/1/7","/press/bank/1/8"]  # Add your object names here

# Variable to store the current project file path
current_file_path = None 

# Dictionary to store object placements
object_placements = {}

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


# if in edit mode dont send osc, if not in send mode send "object_name" as osc command
def send_osc_command(object_name, arg_value):  
    if edit_mode:
        print ("cant send commands in edit mode.")
    else:
        osc_command = f"{object_name}"        
        client.send_message(osc_command, 1-arg_value)
        client2.send_message(osc_command, 1-arg_value)

#Function im working on to eventually be able to choose different object types
def select_object_type():
    box=tk.Button(root, text=simpledialog.askstring("Name", "Enter:"), bg="blue", width=10, height=9)
    box1=tk.Button(root, text=simpledialog.askstring("Name", "Enter:"), bg="blue", width=20, height=20)
    
     
#Function to create a object to click on and send OSC command
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
        print("click send mode button to change to edit mode")


#Function to be able to move object while in edit mode
def move_object(event):
    if edit_mode:
        object = event.widget
        x = event.x_root - root.winfo_rootx() - object.winfo_width() // 2
        y = event.y_root - root.winfo_rooty() - object.winfo_height() // 2
        # Check if the new position is within the canvas boundaries
        if 0 <= x <= objectcanvas.winfo_width() - object.winfo_width() and 0 <= y <= objectcanvas.winfo_height() - object.winfo_height():
            object.place(x=x, y=y) 
            object_placements[object] = (event.x, event.y)
    else:
        print("not in edit mode. click edit button to enable moving of objects")                 

#Function to edit the object and or delete it
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
        else:
            print("Deletion canceled.")    
            
    else:
         print("not in edit mode. put in edit mode to edit or move object.")

def exit_program(event):
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

# Function to handle saving the project
def save_project():
    global current_file_path

    if current_file_path:
        # Save changes to the current file
        # Add your code here to save the project

        # Save object placements to the file
        with open(current_file_path, "w") as file:
            for object_id, placement in object_placements.items():
                file.write(f"{object_id},{placement[0]},{placement[1]}\n")

        messagebox.showinfo("Save", "Project saved successfully.")
    else:
        # If no current file path, prompt the user to choose a file path
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

        if file_path:
            # Save changes to the chosen file
            # Add your code here to save the project

            # Save object placements to the file
            with open(file_path, "w") as file:
                for object_id, placement in object_placements.items():
                    file.write(f"{object_id},{placement[0]},{placement[1]}\n")

            current_file_path = file_path
            messagebox.showinfo("Save", "Project saved successfully.")
            

# Function to load the saved file and restore object placements
def load_project():
    global current_file_path

    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

    if file_path:
        # Load the saved file and restore object placements
        with open(file_path, "r") as file:
             # Loop through the loaded data and move the objects
            for object_data in object_placements.items():
                object_id = object_data['id']
                x = object_data['x']
                y = object_data['y']
                move_object(str(object_id), x, y)
                
 
        current_file_path = file_path
        messagebox.showinfo("Load", "Project loaded successfully.")



# Create the main window
root = tk.Tk()
root.overrideredirect(True)
# Bind the Escape key event to the exit_program function
root.bind("<Escape>", exit_program)



#create canvas
objectcanvas = tk.Canvas(root, width=500, height=500, bg="white")
objectcanvas.pack()

#create canvas for control buttons
controlcanvas = tk.Canvas(root, width=500, height=500, bg="grey")
controlcanvas.pack()

#create dropdown for command osc command list
input = ttk.Combobox(controlcanvas, values=commands)
input.pack()

# Create the "Create Object" button
create_button = tk.Button(controlcanvas, text="Create Button", command=create_object)
create_button.pack()

# Create the "Edit Mode" toggle
edit_button = tk.Button(controlcanvas, text="Edit Mode",command=toggle_edit_mode)
edit_button.pack()

# Add a "Save" button to the window
save_button = tk.Button(controlcanvas, text="Save", command=save_project)
save_button.pack()

# Add a "Load" button to the window
load_button = tk.Button(controlcanvas, text="Load", command=load_project)
load_button.pack()

# Update the edit button color initially
update_button_color()


# Start the event loop
root.mainloop()
