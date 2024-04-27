from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance, ImageFilter, ImageTk, ImageOps,ImageFont, ImageDraw
from tkinter import messagebox
from tkinter import simpledialog

# Global variables
original_image = None
edited_image = None

def open_image():
    global original_image, edited_image

    # Open file dialog to select an image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])

    if file_path:
        # Open the image using Pillow
        original_image = Image.open(file_path)
        edited_image = original_image.copy()

        # Display the image on the canvas
        canvas.image = ImageTk.PhotoImage(original_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

def apply_changes():
    global edited_image

    # Apply the changes to the edited image
    edited_image = original_image.copy()

    # Blur
    blur_amount = blur_slider.get()
    edited_image = edited_image.filter(ImageFilter.GaussianBlur(blur_amount))

    # Contrast
    contrast_amount = contrast_slider.get()
    enhancer = ImageEnhance.Contrast(edited_image)
    edited_image = enhancer.enhance(contrast_amount)

    # Brightness
    brightness_amount = brightness_slider.get()
    enhancer = ImageEnhance.Brightness(edited_image)
    edited_image = enhancer.enhance(brightness_amount)

    # Sharpness
    sharpness_amount = sharpness_slider.get()
    enhancer = ImageEnhance.Sharpness(edited_image)
    edited_image = enhancer.enhance(sharpness_amount)

    # Saturation
    saturation_amount = saturation_slider.get()
    enhancer = ImageEnhance.Color(edited_image)
    edited_image = enhancer.enhance(saturation_amount)

    # Filter
    selected_filter = filter_var.get()
    if selected_filter == "None":
        pass
    elif selected_filter == "Grayscale":
        edited_image = edited_image.convert("L")
    elif selected_filter == "Sepia":
        edited_image = sepia_filter(edited_image)
    elif selected_filter == "Invert":
        edited_image = edited_image.convert("L")
        edited_image = ImageOps.invert(edited_image)
        edited_image = edited_image.convert("RGB")

    # Display the edited image on the canvas
    canvas.image = ImageTk.PhotoImage(edited_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

def reset_changes():
    global edited_image

    # Reset the edited image to the original image
    edited_image = original_image.copy()

    # Reset all sliders to their default values
    blur_slider.set(0)
    contrast_slider.set(1.0)
    brightness_slider.set(1.0)
    sharpness_slider.set(1.0)
    saturation_slider.set(1.0)
    filter_var.set("None")

    # Display the original image on the canvas
    canvas.image = ImageTk.PhotoImage(original_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
    if file_path:
        edited_image.save(file_path)

def crop_image(aspect_ratio):
    global edited_image

    # Calculate the desired crop size based on the aspect ratio
    width, height = edited_image.size
    if aspect_ratio > 1:
        new_width = width
        new_height = int(width / aspect_ratio)
    else:
        new_width = int(height * aspect_ratio)
        new_height = height

    # Calculate the crop coordinates
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    # Crop the image
    edited_image = edited_image.crop((left, top, right, bottom))

    # Display the cropped image on the canvas
    canvas.image = ImageTk.PhotoImage(edited_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

def circle_crop():
    global edited_image

    # Calculate the crop size based on the minimum dimension of the image
    width, height = edited_image.size
    size = min(width, height)

    # Calculate the crop coordinates to form a square centered in the image
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size

    # Crop the image
    cropped_image = edited_image.crop((left, top, right, bottom))

    # Create a new circular mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # Apply the mask to the cropped image
    cropped_image.putalpha(mask)

    # Create a new image with a white background
    circle_cropped_image = Image.new("RGB", (size, size), (255, 255, 255))
    circle_cropped_image.paste(cropped_image, (0, 0), cropped_image)

    # Display the circle cropped image on the canvas
    canvas.image = ImageTk.PhotoImage(circle_cropped_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

    # Update the edited image
    edited_image = circle_cropped_image

def rotate_left():
    global edited_image
    edited_image = edited_image.rotate(90, expand=True)
    canvas.image = ImageTk.PhotoImage(edited_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

def rotate_right():
    global edited_image
    edited_image = edited_image.rotate(-90, expand=True)
    canvas.image = ImageTk.PhotoImage(edited_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

def rotate_180():
    global edited_image
    edited_image = edited_image.rotate(180)
    canvas.image = ImageTk.PhotoImage(edited_image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

def add_text_on_image():
    global edited_image
    
    # Prompt the user for the text to be added
    text = simpledialog.askstring("Add Text", "Enter the text to be added:", parent=window)
    
    if text:
        # Prompt the user for the position on the image
        position = simpledialog.askstring("Add Text", "Enter the position (x,y) on the image:", parent=window)
        
        try:
            x, y = map(int, position.split(","))
            
            # Create a copy of the edited image
            image_with_text = edited_image.copy()
            
            # Create a new PIL ImageDraw object
            draw = ImageDraw.Draw(image_with_text)
            
            # Define the font and size for the text
            font = ImageFont.truetype("arial.ttf", 30)
            
            # Add the text to the image
            draw.text((x, y), text, fill=(255, 255, 255), font=font)
            
            # Display the image with the added text on the canvas
            canvas.image = ImageTk.PhotoImage(image_with_text)
            canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)
            
            # Update the edited image
            edited_image = image_with_text
        except:
            messagebox.showerror("Error", "Invalid position. Please enter a valid position.")

# Sepia filter
def sepia_filter(image):
    width, height = image.size
    sepia_image = Image.new("RGB", (width, height))

    pixels = image.load()
    sepia_pixels = sepia_image.load()

    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            sepia_pixels[i, j] = (tr, tg, tb)

    return sepia_image

# Create the main window
window = tk.Tk()
window.title("Bonafide Photo Editor")
window.configure(bg='grey30')

# Create a frame for the toolbar
toolbar_frame = tk.Frame(window, bg='grey20')
toolbar_frame.pack(fill=tk.X)

# Create the toolbar buttons
open_button = tk.Button(toolbar_frame, text="Open", command=open_image, font=(None, 12), bg='grey60')
open_button.pack(side=tk.LEFT, padx=5, pady=5)

save_button = tk.Button(toolbar_frame, text="Save", command=save_image, font=(None, 12), bg='grey60')
save_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame for the image canvas
canvas_frame = tk.Frame(window, highlightbackground="black", highlightthickness=1)
canvas_frame.pack()

# Create the canvas for displaying the image
canvas = tk.Canvas(canvas_frame, width=800, height=600, bg='LavenderBlush4')
canvas.pack()

# Create a frame for the settings
settings_frame = tk.Frame(window, bg='grey20', highlightbackground="black", highlightthickness=1)
settings_frame.pack(fill=tk.X)

# Blur settings
blur_label = tk.Label(settings_frame, text="Blur", bg='grey50')
blur_label.pack(side=tk.LEFT, padx=5, pady=5)

blur_slider = tk.Scale(settings_frame, from_=0, to=20, orient=tk.HORIZONTAL, bg='grey50', sliderlength=40, length=170)
blur_slider.pack(side=tk.LEFT, padx=5, pady=5)

# Contrast settings
contrast_label = tk.Label(settings_frame, text="Contrast", bg='grey50')
contrast_label.pack(side=tk.LEFT, padx=5, pady=5)

contrast_slider = tk.Scale(settings_frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, bg='grey50', sliderlength=40, length=170)
contrast_slider.pack(side=tk.LEFT, padx=5, pady=5)

# Brightness settings
brightness_label = tk.Label(settings_frame, text="Brightness", bg='grey50')
brightness_label.pack(side=tk.LEFT, padx=5, pady=5)

brightness_slider = tk.Scale(settings_frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, bg='grey50', sliderlength=40, length=170)
brightness_slider.pack(side=tk.LEFT, padx=5, pady=5)

# Sharpness settings
sharpness_label = tk.Label(settings_frame, text="Sharpness", bg='grey50')
sharpness_label.pack(side=tk.LEFT, padx=5, pady=5)

sharpness_slider = tk.Scale(settings_frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, bg='grey50', sliderlength=40, length=170)
sharpness_slider.pack(side=tk.LEFT, padx=5, pady=5)

# Saturation settings
saturation_label = tk.Label(settings_frame, text="Saturation", bg='grey50')
saturation_label.pack(side=tk.LEFT, padx=5, pady=5)

saturation_slider = tk.Scale(settings_frame, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, bg='grey50', sliderlength=40, length=170)
saturation_slider.pack(side=tk.LEFT, padx=5, pady=5)

# Filter settings
filter_label = tk.Label(settings_frame, text="Filter", bg='grey50')
filter_label.pack(side=tk.LEFT, padx=5, pady=5)

filter_var = tk.StringVar(settings_frame)
filter_var.set("None")

filter_dropdown = tk.OptionMenu(settings_frame, filter_var, "None", "Grayscale", "Sepia", "Invert")
filter_dropdown.config(bg="grey50", fg="black")
filter_dropdown["menu"].config(bg="grey50")
filter_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame for the buttons
buttons_frame = tk.Frame(window, bg='grey20', highlightbackground="black", highlightthickness=1)
buttons_frame.pack(fill=tk.X)

# Create the buttons
apply_button = tk.Button(buttons_frame, text="Apply Changes", command=apply_changes, bg='grey60', fg='black', font=(None, 15))
apply_button.pack(side=tk.LEFT, padx=5, pady=5)

reset_button = tk.Button(buttons_frame, text="Reset Changes", command=reset_changes, bg='grey60', fg='black', font=(None, 15))
reset_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create a frame for the crop buttons
crop_buttons_frame = tk.Frame(window, bg='grey20', highlightbackground="black", highlightthickness=1)
crop_buttons_frame.pack(fill=tk.X)

# Create the crop buttons
crop_label = tk.Label(crop_buttons_frame, text="Crop:", bg='grey50')
crop_label.pack(side=tk.LEFT, padx=5, pady=5)

crop_buttons = [
    ("1:1", 1),
    ("4:3", 4 / 3),
    ("3:4", 3 / 4),
    ("16:9", 16 / 9),
    ("9:16", 9 / 16),
    ("3:2", 3 / 2),
    ("2:3", 2 / 3)
]

for text, aspect_ratio in crop_buttons:
    button = tk.Button(crop_buttons_frame, text=text, command=lambda ar=aspect_ratio: crop_image(ar), bg='grey60', fg='black', font=(None, 12))
    button.pack(side=tk.LEFT, padx=5, pady=5)
    
circle_crop_button = tk.Button(crop_buttons_frame, text="Circle", command=circle_crop, font=(None, 12), bg='grey60')
circle_crop_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create the rotate buttons 
rotate_label = tk.Label(crop_buttons_frame, text="Rotate:", bg='grey50')
rotate_label.pack(side=tk.LEFT, padx=5, pady=5)

rotate_left_button = tk.Button(crop_buttons_frame, text="Rotate Left", command=rotate_left, font=(None, 12), bg='grey60')
rotate_left_button.pack(side=tk.LEFT, padx=5, pady=5)

rotate_right_button = tk.Button(crop_buttons_frame, text="Rotate Right", command=rotate_right, font=(None, 12), bg='grey60')
rotate_right_button.pack(side=tk.LEFT, padx=5, pady=5)

rotate_180_button = tk.Button(crop_buttons_frame, text="Rotate 180", command=rotate_180, font=(None, 12), bg='grey60')
rotate_180_button.pack(side=tk.LEFT, padx=5, pady=5)
# Create add text button
text_label = tk.Label(crop_buttons_frame, text="Text:", bg='grey50')
text_label.pack(side=tk.LEFT, padx=5, pady=5)

add_text_button = tk.Button(crop_buttons_frame, text="Add Text", command=add_text_on_image, font=(None, 12), bg='grey60')
add_text_button.pack(side=tk.LEFT, padx=5, pady=5)

# Run the main loop
window.mainloop()
