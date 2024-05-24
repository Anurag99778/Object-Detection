# Object Detection Project

This project demonstrates object detection using TensorFlow and MySQL database interaction.

## Table of Contents

- [Introduction](#introduction)
- [Setup Environment](#setup-environment)
  - [Clone the Repository](#1-clone-the-repository)
  - [Install Dependencies](#2-install-dependencies)
  - [Download Pre-trained Model](#3-download-pre-trained-model)
  - [Database Setup](#4-database-setup)
- [Usage](#usage)
  - [Run the Main Script](#1-run-the-main-script)
  - [View Output](#2-view-output)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project utilizes TensorFlow for object detection tasks and integrates with a MySQL database for storing detection data.

## Setup Environment

### 1. Clone the Repository

```bash
git clone https://github.com/Anurag99778/Object-Detect.git
cd Object-Detect
# Setup Environment

```
### 2. Install Dependencies
Ensure you have Python (version 3.6 or higher) installed.
Install required packages using requirements.txt:

```bash
Copy code
pip install -r requirements.txt


```
### 3. Download Pre-trained Model
Download the pre-trained TensorFlow model (SSD MobileNet V2) from the TensorFlow Model Zoo and place it in the models/ directory.

### 4. Database Setup
Ensure MySQL server is installed and running.
Create a database named OBJECT_DETECTION.
Modify the database connection settings in database.py as needed.

## Usage
### 1. Run the Main Script
Execute the main.py script to perform object detection and interact with the database.
```bash
Copy code
python main.py
```
### 2. View Output
The processed video output will be saved in the specified output directory.
Detections will be saved to the MySQL database.


## Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
