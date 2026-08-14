# Project Report Summary

## Project Scope

The original project demonstrated real-time face recognition for three people in one camera frame using an ESP32-CAM, Arduino tooling, Python, OpenCV Haar Cascade, and an LBPH face recognizer.

The workflow consisted of three stages:

1. Capture face samples from the ESP32-CAM over Wi-Fi.
2. Train an LBPH recognizer from grayscale face images.
3. Retrieve new frames from the ESP32-CAM and classify detected faces.

## Original Dataset

The supplied project archive contained 91 face images across three numeric IDs. The original dataset and trained model are intentionally excluded from this public-ready repository because they contain or derive from identifiable biometric data.

## Reported Demonstration Results

The report compared two dataset conditions.

### Varied face angles

Displayed recognition values were reported around:

- 32 percent
- 47 percent
- 44 percent

The report observed weaker recognition when faces were rotated or viewed from larger angles.

### Mostly frontal faces

Displayed recognition values were reported around:

- 50 percent
- 54 percent
- 50 percent

The report observed more stable results when faces remained frontal.

## Methodological Clarification

The original program displayed a value calculated from the LBPH `confidence` output, effectively treating `100 - confidence` as a percentage-like score. OpenCV LBPH prediction output is a distance measure. It is not a validated classification accuracy percentage.

Therefore, this repository does not label the reported values as model accuracy.

A defensible performance evaluation would require:

1. Separate training and test data.
2. No test image leakage into training.
3. Ground-truth labels for every test sample.
4. Metrics such as accuracy, precision, recall, F1-score, and a confusion matrix.
5. Evaluation across lighting, pose, distance, and occlusion conditions.

## Technical Findings

The project still demonstrates a useful classical computer-vision principle. Haar Cascade and LBPH can work in controlled environments with frontal faces and consistent lighting, but they are sensitive to pose and image quality. The system is appropriate for learning and prototyping rather than security-critical authentication.

## Repository Cleanup Performed

For public GitHub use, this version removes or replaces:

- hard-coded Wi-Fi SSID and password
- hard-coded ESP32-CAM IP addresses
- personal face labels in source code
- raw face-image dataset
- trained LBPH model
- redundant external Haar Cascade XML because OpenCV already bundles the cascade path used by the scripts
- original report PDF because it contains identifiable faces, personal identifiers, and Wi-Fi credentials

The repository now uses CLI arguments, environment configuration, ignored secret files, an example label mapping, and privacy documentation.
