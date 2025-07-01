# Smart ID Photo Generator System
#### Video Demo:  https://www.youtube.com/watch?v=zVMAxNwJCWk
#### Description:

# Smart ID Photo Generator System
## Overview
The Smart ID Photo Generator System is a web-based application that allows users to upload photos and automatically generate professional ID photos with various standard sizes and background colors. The system features face detection, background replacement, intelligent cropping, and an optional anime-style conversion.

## Key Features
- **Face Detection & Landmark Localization**: Uses Dlib's 68-point face model
- **Background Replacement**: Powered by U²-Net for precise segmentation
- **Smart Cropping**: Supports standard sizes (1-inch, 2-inch, passport, visa, etc.)
- **Anime Style Conversion**: Optional fun feature to convert photos to anime style
- **User Authentication**: Secure login and registration system
- **Responsive UI**: Clean interface built with HTML and Bootstrap

## System Architecture

### Frontend
- **Templates**:
  - `layout.html`: Base template with header/footer
  - `index.html`: Main application page
  - `login.html`: User login
  - `register.html`: User registration
  - `about.html`: About page
  - `help.html`: Help documentation

### Backend
- **Core Modules**:
  - `face_marks.py`: Face detection and landmark localization
  - `ai_crop.py`: Intelligent image cropping and resizing
  - `web_main.py`: Main Flask application with routes and processing logic
  - `utils.py`: Helper functions for image processing

### AI Models
- **Face Detection**: Dlib's 68-point model
- **Background Segmentation**: U²-Net (ONNX format)
- **Inference Engine**: ONNX Runtime

## Development Environment

### Requirements
- **OS**: Windows 10/11
- **Python**: 3.11
- **Web Framework**: Flask
- **Frontend**: HTML + Bootstrap
- **Key Libraries**:
  - Dlib (face detection)
  - OpenCV, NumPy (image processing)
  - ONNX Runtime (model inference)
  - Werkzeug (security)

### Directory Structure
```
project/
├── static/              # Static resources (CSS, JS, images)
├── templates/           # HTML templates
│   ├── index.html       # Main page
│   ├── about.html       # About page
│   ├── help.html        # Help page
│   ├── layout.html      # Base template
│   ├── login.html       # Login page
│   └── register.html    # Registration page
├── models/              # Model files (e.g., u2net.onnx)
├── img/                 # User uploads and processed images
├── database.db          # SQLite user database
├── face_marks.py        # Face detection
├── ai_crop.py           # Image cropping
├── web_main.py          # Main application
├── utils.py             # Utility functions
└── requirements.txt     # Dependency list
```

## Installation & Usage

### Quick Start
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python web_main.py
   ```
4. Access the system at: `http://localhost:5000`

### Usage Flow
1. Register/Login to the system
2. Upload your photo
3. System automatically processes:
   - Face detection
   - Background segmentation
   - Image cropping
4. Choose between standard ID photo or anime-style conversion
5. Preview and download the result

## Technical Details

### Core Algorithms
- **Face Detection**: Uses Dlib's 68-point model to locate facial features
- **Background Segmentation**: U²-Net generates alpha masks for precise background removal
- **Image Cropping**: Intelligent sizing based on standard photo dimensions (configured in SIZE_MAP)
- **Color Processing**: Handles RGB/BGR conversions and normalization for model input

### Current Limitations
- Processes only the first detected face in multi-person photos
- May have imperfect edges with curly hair
- Possible artifacts with complex backgrounds

### Future Improvements
- Smarter face selection (e.g., largest or most centered face)
- Specialized hair segmentation models (e.g., MODNet)
- Edge expansion to prevent background filling issues
- Enhanced error handling for edge cases

## Support
For assistance, please:
1. Check the Help page in the application
2. Contact our support team through the About page

## License
This project is for demonstration purposes. All model weights (U²-Net) should be used according to their original licenses.
