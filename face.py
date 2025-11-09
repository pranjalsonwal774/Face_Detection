import cv2
from tkinter import *
from PIL import Image, ImageTk

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize main window
root = Tk()
root.title("Real-Time Face Detection")
root.geometry("850x650")
root.configure(bg="#1e1e2e")

# Global variables
cap = None
running = False
camera_index = 0   # 0 = default cam, 1 = external/secondary

# Create video display label
video_label = Label(root, bg="#1e1e2e")
video_label.pack(pady=20)

# Status and face count labels
status_label = Label(root, text="Status: Camera not started", font=("Arial", 12), fg="white", bg="#1e1e2e")
status_label.pack()

face_count_label = Label(root, text="Detected Faces: 0", font=("Arial", 12, "bold"), fg="lightgreen", bg="#1e1e2e")
face_count_label.pack(pady=5)

# -----------------------------------------------------
# Function: Start Camera
# -----------------------------------------------------
def start_camera():
    global cap, running
    if running:
        return
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        status_label.config(text="Error: Could not open camera.", fg="red")
        return
    running = True
    status_label.config(text=f"Camera {camera_index} started...", fg="lightgreen")
    show_frame()

# -----------------------------------------------------
# Function: Show Frame (Detect Faces)
# -----------------------------------------------------
def show_frame():
    global cap, running
    if not running:
        return

    ret, frame = cap.read()
    if not ret:
        status_label.config(text="Failed to grab frame.", fg="red")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Update face count label
    face_count_label.config(text=f"Detected Faces: {len(faces)}")

    # Convert frame to ImageTk for display
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    video_label.after(10, show_frame)

# -----------------------------------------------------
# Function: Stop Camera
# -----------------------------------------------------
def stop_camera():
    global cap, running
    running = False
    if cap is not None:
        cap.release()
    video_label.config(image='')
    status_label.config(text="Camera stopped.", fg="yellow")
    face_count_label.config(text="Detected Faces: 0")


# Buttons
# -----------------------------------------------------
btn_frame = Frame(root, bg="#1e1e2e")
btn_frame.pack(pady=10)

start_btn = Button(btn_frame, text="Start Camera", font=("Arial", 12, "bold"),
                   bg="#4CAF50", fg="white", width=15, command=start_camera)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = Button(btn_frame, text="Stop Camera", font=("Arial", 12, "bold"),
                  bg="#F44336", fg="white", width=15, command=stop_camera)
stop_btn.grid(row=0, column=1, padx=10)



exit_btn = Button(btn_frame, text="Exit", font=("Arial", 12, "bold"),
                  bg="#607D8B", fg="white", width=15, command=root.destroy)
exit_btn.grid(row=0, column=3, padx=10)

# Run Tkinter loop
root.mainloop()
