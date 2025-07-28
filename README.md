🖐️ HandTracking Volume Control 🎚️

Control your MacBook's volume using just your fingers, in real time!

🔥 What It Does

This project uses your webcam and hand gestures to control the system volume using computer vision and media pipe hand tracking.

When you bring your thumb and index finger closer or farther apart, the volume decreases or increases. Smooth, contactless control – ideal for accessibility, futuristic UI, or just fun!

https://github.com/roshan11-05/HandTrackingProject/assets/yourusername/demo-video.gif
<sub>(You can add a demo GIF/video later!)</sub>

💡 Features

🔍 Real-time hand tracking using MediaPipe
✌️ Detects finger distance for gesture input
🔊 Maps finger distance to system volume
⚡️ Fast performance with OpenCV
🖥️ Designed for MacBook (macOS) but extendable to Windows/Linux

📁 Project Structure
HandTrackingProject/
│
├── HandTrackingModule.py       
├── VolumeHandControl.py        # Main script for gesture → volume control
├── README.md
└── .idea/, .venv/             

🛠️ How to Run (MacBook)

🔗 1. Clone the Repository
git clone https://github.com/roshan11-05/HandTrackingProject.git
cd HandTrackingProject

📦 2. Install Requirements
pip install opencv-python mediapipe numpy

🚀 3. Run the App
python VolumeHandControl.py


📸 How It Works:

Camera captures video stream
MediaPipe detects hand landmarks
Distance between thumb & index finger is measured
That distance is mapped to system volume scale (e.g., 0–100)
OpenCV displays the live feed with gesture feedback and FPS

🤖 Technologies Used:
Python 🐍
OpenCV 🎥
MediaPipe 🤚
NumPy 🧮
macOS osascript for volume control

👨‍💻 Author

Roshan Gopinath
🔗 GitHub
📧 roshan.gopinath@example.com (use your real email)

⭐️ Show Some Love
If you liked this project, consider giving it a ⭐️ on GitHub and sharing it!
