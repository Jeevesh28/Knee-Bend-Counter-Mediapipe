import cv2
import numpy as np
import mediapipe as mp

# Pose recognition, it will detect all our landmarks, using which the angle is found
mp_pose = mp.solutions.pose

# Drawing all landmarks
mp_drawing = mp.solutions.drawing_utils

# Calculate angle
def calculate_angle(a, b, c):
    a = np.array(a) # Start
    b = np.array(b) # Middle
    c = np.array(c) # End
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle    
    return angle 

# Video input
cap = cv2.VideoCapture('KneeBendVideo.mp4')

# Video Characteristics
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Counter and State Variables
relax_counter = 0 
bent_counter = 0
counter = 0
stage = None
feedback = None
images_array=[]

# Mediapipe Instance
with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract Landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates of interested landmarks (23, 25, and 27)
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            
            # Calculating Angle
            angle = calculate_angle(hip, knee, ankle)

            # Render Detections
            a0 = int(ankle[0] * width)
            a1 = int(ankle[1] * height)

            k0 = int(knee[0] * width)
            k1 = int(knee[1] * height)

            h0 = int(hip[0] * width)
            h1 = int(hip[1] * height)

            cv2.line(image, (h0, h1), (k0, k1), (255, 255, 0), 2)
            cv2.line(image, (k0, k1), (a0, a1), (255, 255, 0), 2)
            cv2.circle(image, (h0, h1), 5, (0, 0, 0), cv2.FILLED)
            cv2.circle(image, (k0, k1), 5, (0, 0, 0), cv2.FILLED)
            cv2.circle(image, (a0, a1), 5, (0, 0, 0), cv2.FILLED)       
            
            # Visualizing Angle
            cv2.putText(image, str(round(angle,4)), tuple(np.multiply(shoulder, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            relax_time = (1 / fps) * relax_counter
            bent_time = (1 / fps) * bent_counter

            #Counter Logic
            if angle > 140:
                relax_counter += 1
                bent_counter = 0
                stage = "Relaxed"
                feedback = ""
            
            if angle < 140:
                relax_counter = 0
                bent_counter += 1
                stage = "Bent"
                feedback = ""
            
            # Sucessful rep
            if bent_time == 8:
                counter += 1
                feedback = 'Rep completed'
                
            elif bent_time < 8 and stage == 'Bent':
                feedback = 'Keep Your Knee Bent'
            
            else:
                feedback = ""
                
        except:
            pass
                
        # Setup status box
        cv2.rectangle(image, (0,0), (int(width), 60), (255,255,0), -1)
        
        # Rep data
        cv2.putText(image, 'REPS', (10,15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.putText(image, str(counter), 
                    (10,50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'STAGE', (105,15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (105,50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # Feedback
        cv2.putText(image, 'FEEDBACK', (315,15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.putText(image, feedback, 
                    (315,50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # Bent Time
        cv2.putText(image, 'BENT TIME', (725,15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.putText(image, str(round(bent_time,2)), 
                    (725,50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)  

        images_array.append(image) 
        
        cv2.imshow('Knee Bend Excercise', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Generate output video
out = cv2.VideoWriter('Output.mp4', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in range(len(images_array)):
    out.write(images_array[i])
out.release()