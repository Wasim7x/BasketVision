# 🏀 BasketVision – Basketball Video Analysis System

BasketVision is an end-to-end **basketball video analysis** project that automatically detects and tracks players and the ball, assigns teams, analyzes possession and passes, and generates a fully annotated output video.

The project integrates **YOLO-based object detection**, **tracking**, and **custom basketball-specific logic** to convert raw match footage into meaningful visual insights. It is designed to be modular, reproducible, and easy to extend for research or production use.

---

## 📌 Table of Contents

1. [Features](#-features)
2. [Demo / Sample Output](#-demo--sample-output)
3. [Prerequisites](#-prerequisites)
4. [Installation](#-installation)
5. [Model Training](#-model-training)
6. [Usage](#-usage)
7. [Project Structure](#-project-structure)
8. [Future Enhancements](#-future-enhancements)
9. [Contributing](#-contributing)
10. [License](#-license)

---

## ✨ Features

- 🎯 **Player & Ball Detection** using YOLO-based deep learning models
- 🔄 **Multi-object Tracking** across video frames
- 👕 **Team Assignment** based on jersey color classification
- 🏀 **Ball Possession Detection** (which player controls the ball)
- 🔁 **Pass & Interception Detection**
- 🏟️ **Court Keypoint Detection** for tactical visualization
- 🎨 **Frame Annotation Utilities** (bounding boxes, labels, court lines)
- ⚡ **Stub-based Caching** to avoid recomputation and speed up experiments
- 📹 **End-to-End Video Pipeline** from raw input to annotated output

---

## 🎮 Demo / Sample Output

> 📍 Place your **sample output video or GIF** here

```text
output_videos/
└── sample_output.mp4
```

You can also attach a YouTube demo:

```
[![Demo Video](thumbnail_link)](youtube_video_link)
```

---

## 🔧 Prerequisites

- Python **3.8+**
- pip / virtualenv / conda
- (Optional) **Docker** for containerized execution
- GPU recommended for real-time or faster inference

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/BasketVision.git
cd BasketVision
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\\Scripts\\activate    # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🎓 Model Training

This project supports both **pretrained weights** and **custom-trained models**.

### Option 1: Use Pretrained Models

Place all `.pt` files inside the `models/` directory:

```text
models/
├── player_detector.pt
├── ball_detector.pt
└── court_keypoint_detector.pt
```

### Option 2: Train Your Own Models

Training notebooks are provided for:

- 🏀 Basketball Ball Detection
- 🧍 Player Detection
- 🏟️ Court Keypoint Detection

You can train using **Roboflow + Ultralytics YOLO** and export weights to the `models/` folder.

---

## 🚀 Usage

### Run Analysis Pipeline

```bash
python main.py path_to_input_video.mp4 --output_video output_videos/result.avi
```

### Optional Arguments

- `--stub_path` : Path to cached detection results
- `--disable_stubs` : Force fresh inference

### Docker (Optional)

```bash
docker build -t basketvision .

docker run \
  -v $(pwd)/videos:/app/videos \
  -v $(pwd)/output_videos:/app/output_videos \
  basketvision \
  python main.py videos/input.mp4 --output_video output_videos/output.avi
```

---

## 🏗️ Project Structure

```text
BasketVision/
├── main.py                     # Main entry point
├── models/                      # Trained model weights (.pt files)
├── trackers/                    # Player & ball tracking logic
├── drawers/                     # Visualization & annotation utilities
├── utils/                       # Helper utilities (bbox, video, stubs)
├── team_assigner/               # Jersey-color based team classification
├── ball_acquisition/            # Ball possession logic
├── pass_and_interception_detector/ # Pass & interception detection
├── court_keypoint_detector/     # Court line & keypoint detection
├── configs/                     # Config files and paths
├── training_notebooks/          # Model training notebooks
├── videos/                      # Input videos
├── output_videos/               # Annotated output videos
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## 🔮 Future Enhancements

- 🤸 **Pose Estimation** for detecting violations (travel, double dribble)
- 📊 **Advanced Analytics Dashboard** (possession %, heatmaps)
- 🧠 **Action Recognition** (shots, rebounds, fouls)
- ⚡ **Real-time Inference Support**

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request with clear details

---

## 📜 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more details.

---

## 💬 Contact

For questions, suggestions, or collaboration opportunities, feel free to open an issue or reach out.

Happy analyzing! 🏀📊

