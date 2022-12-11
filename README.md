# Knee Bend Exercise Counter

## STEPS:
* Remove duplicate frames 
* Configuring the Media Pipe
* Estimating poses
* Extracting joint coordinates
* Calculating angles between joints
* Inserting timer, stage (bent or relaxed), rep counter, and feedback

## 0. Remove duplicate frames:
* Extract the individual frames of the video using a video processing library like OpenCV.
* Once the frames are extracted, Python's built-in **hashlib** module is to compute a hash value for each frame, and then compare the hash values to identify duplicate frames.

## 1. Configuring the Media Pipe:
* Install and import [Mediapipe](https://google.github.io/mediapipe/solutions/pose), it is a cross-platform library developed by Google that provides amazing, ready-to-use ML solutions for computer vision tasks.
* Along with Mediapipe, install and import some other dependencies such as **OpenCV** and **NumPy**.

## 2. Estimating poses:
* In this step, we will be estimating all the different joints and parts within our body.
* Capture the video feed from the [video file](https://github.com/Jeevesh28/Knee-Bend-Counter-Mediapipe/blob/main/KneeBendVideo.mp4) provided.
* Recolor our image because when we pass the image to mediapipe it should be in RGB format, which is the default BGR when we read it.
* Use the Pose estimation model to detect the pose.
* Recolor the image back to the default BGR format.
* Perform detections, i.e., draw **landmarks** from the video feed (e.g., nose, eyes, ears, shoulders, elbows, wrists).

## 3. Extraction of Joint Coordinates:
* Use the pose estimation model to extract landmarks using detected pose estimation, as we did in the previous step.
* Extract the landmarks for the main 3 joints that we need to calculate the rep count for knee-bending exercises which are **hip**, **knee**, and **ankle**.

## 4. Calculating angles between joints:
* Calculate the **angle** between the hip, knee, and ankle to identify whether the leg is straight or bent.
* For calculate the angle, we are going to calculate the radians with the help of three parameters passed to the function **calculate_angle()**, which are hip, knee, and ankle, by using a trigonometric function and then converting radian to angle.

## 5. Inserting timer, stage (bent or relaxed), rep counter, and feedback:
* If the calculated angle is less than or equal to **140&deg;**, then the stage of the leg will be **bent**, and else if the calculated angle is greater than 140&deg; and the stage is bent, then the stage will be **relaxed**.
* A timeholder is used to measure the start time in starting when the stage changes from relaxed to bent stage, and the end time is measured when the stages changes from bent to relaxed stage, duration is calculated by subtracting the end time from the start time. 
* If a user can hold the leg in the bent stage for the duration of **8** or more than 8 seconds, then the rep count is incremented. 
* Otherwise if the user is unable to stay in the bent stage for more than 8 seconds, the feedback will print **keep your knee bent**.

## Input Video:

https://user-images.githubusercontent.com/58467403/206901158-8dfc2f56-a776-4438-881c-12ba9533b526.mp4

## Output Video:

https://user-images.githubusercontent.com/58467403/206901533-ca2acdb6-59b7-4af8-b6fa-3e3228c475ed.mp4
