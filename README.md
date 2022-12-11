# Knee Bend Exercise Counter

A pose-estimation rep counter for a knee-bend exercise. It tracks the hip, knee and ankle in a video, measures the knee angle every frame, and counts a rep only when the leg is held bent for the full 8 seconds, giving live feedback when the hold is broken early.

**Stack:** Python · MediaPipe Pose · OpenCV · NumPy

---

## Problem

Counting every bend is easy; counting only *correct* reps is the hard part. A rep here is valid only if the knee stays bent for 8 seconds, so the counter has to track state over time, not just detect a pose in a single frame. The source video also contains duplicate frames, which would distort any timing based on frame counts.

## Approach

1. **De-duplicate frames** (`remove_duplicates.py`). Each frame is hashed with Python's `hashlib`, and frames with matching hashes are dropped, so frame counts map cleanly to elapsed time.
2. **Estimate pose.** Each frame is converted from OpenCV's BGR to RGB, passed to MediaPipe Pose, and converted back for drawing the landmarks.
3. **Extract joints.** The hip, knee and ankle landmarks are pulled from the detected pose.
4. **Compute the knee angle.** `calculate_angle(hip, knee, ankle)` takes the difference of the two segment angles from `arctan2`, converts radians to degrees, and folds anything above 180° back into [0°, 180°].
5. **Track state and time.**
   - An angle below **140°** marks the leg as **bent**; above 140° marks it **relaxed**.
   - Hold time is measured in video time, not wall-clock time: frames spent in the bent stage divided by the video's FPS.
   - When the bent hold reaches **8 s**, the rep counter increments.
   - If the leg relaxes before 8 s, the overlay shows **"Keep your knee bent"**.

The overlay draws the landmarks, the live angle, the current stage, the hold timer and the rep count on every frame.

## Running it

```bash
pip install mediapipe opencv-python numpy
python remove_duplicates.py      # optional: clean the input video first
python main.py                   # processes KneeBendVideo.mp4
```

`KneeBendVideo.mp4` is the sample input and `Output.mp4` is the annotated result.

## Repository layout

```
main.py                 pose estimation, angle, stage machine, overlay
remove_duplicates.py    hash-based duplicate frame removal
KneeBendVideo.mp4       sample input video
Output.mp4              annotated output
```

## Known limitations

- The 140° threshold and 8 s hold are fixed; a different exercise or camera angle would need re-tuning.
- Only the left leg is tracked (MediaPipe's left hip, knee and ankle landmarks).
