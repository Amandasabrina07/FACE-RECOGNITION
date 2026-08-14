# GitHub Upload Guide

## Recommended Repository

Name:

```text
esp32cam-lbph-face-recognition
```

Description:

```text
Real-time face recognition with ESP32-CAM, OpenCV Haar Cascade, and LBPH in Python.
```

## Option 1: Git Command Line

From the extracted repository folder:

```bash
git init
git add .
git status
git commit -m "Initial public release"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Inspect `git status` before committing. Dataset images, trained models, personal label files, and Wi-Fi secrets should not appear.

## Option 2: GitHub Web Upload

1. Create a new empty repository on GitHub.
2. Do not ask GitHub to generate another README if you want to preserve this repository exactly.
3. Upload the contents of this folder.
4. Verify that ignored biometric files and secrets are not included.
5. Commit the uploaded files.

## Suggested Topics

```text
esp32-cam
opencv
python
face-recognition
lbph
computer-vision
iot
haar-cascade
```
