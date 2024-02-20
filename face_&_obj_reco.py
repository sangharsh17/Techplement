import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog, Menu, messagebox
from PIL import Image, ImageTk
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import mysql.connector

# Load pre-trained model
model = keras.applications.MobileNetV2(weights='imagenet')

# Initialize Tkinter
root = Tk()
root.title("Image Classifier")

# Set background color
root.configure(bg='#2C3E50')

# Variables for image and label
image_label = Label(root, bg='#2C3E50')
result_label = Label(root, text="", bg='#2C3E50', fg='#ECF0F1', font=('Helvetica', 12))
status_bar = Label(root, text="Welcome to Image Classifier", bd=1, relief='sunken', anchor='w', bg='#34495E', fg='#ECF0F1', font=('Helvetica', 10))

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="imgrec"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create a table to store image classifications
cursor.execute("CREATE TABLE IF NOT EXISTS image_classifications (id INT AUTO_INCREMENT PRIMARY KEY, image_path VARCHAR(255), classification TEXT)")

# Commit the changes
db.commit()

# Load an image for classification
def load_and_preprocess_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

# Classify the image and store in the database
def classify_image(image_path):
    try:
        img_array = load_and_preprocess_image(image_path)
        predictions = model.predict(img_array)
        decoded_predictions = keras.applications.mobilenet_v2.decode_predictions(predictions)
        
        # Display the top predictions
        result = ""
        for i, (_, label, score) in enumerate(decoded_predictions[0]):
            result += f"{label} ({score:.2f})\n"
        
        result_label.config(text=result)

        # Store the classification in the database
        cursor.execute("INSERT INTO image_classifications (image_path, classification) VALUES (%s, %s)", (image_path, result))
        db.commit()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Open file dialog to choose an image
def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Display the selected image
        img = Image.open(file_path)
        img = img.resize((300, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
        
        # Classify the selected image and store in the database
        classify_image(file_path)

# Clear the displayed image and classification result
def clear_display():
    image_label.config(image=None)
    result_label.config(text="")

# Create and place widgets
select_button = Button(root, text="Select Image", command=open_file_dialog, bg='#3498DB', fg='#ECF0F1', font=('Helvetica', 12))
clear_button = Button(root, text="Clear", command=clear_display, bg='#E74C3C', fg='#ECF0F1', font=('Helvetica', 12))

select_button.pack(pady=10)
clear_button.pack(pady=10)
image_label.pack()
result_label.pack(pady=10)
status_bar.pack(side='bottom', fill='x')

# Create Menu Bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# File Menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open Image", command=open_file_dialog)
file_menu.add_command(label="Clear Display", command=clear_display)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

# Help Menu
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Image Classifier v1.0"))

# Run the Tkinter main loop
root.mainloop()

# Close the database connection when the GUI is closed
cursor.close()
db.close()
