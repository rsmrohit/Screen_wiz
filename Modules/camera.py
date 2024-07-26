import cv2
import mediapipe as mp
import multiprocessing
import logging
import math

mp_hands = mp.solutions.hands

# Load in model
hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3,
    max_num_hands=4)


class Camera(multiprocessing.Process):

    def __init__(self, ldm):
        multiprocessing.Process.__init__(self)
        self.ldm = ldm
        self.exit = multiprocessing.Event()
        self.cap = None

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while not self.exit.is_set():

            if not self.cap.isOpened():
                print("Can not open camera")
                continue

            success, image = self.cap.read()

            if not success:
                print("Can not read image")
                break

            image.flags.writeable = False
            image = cv2.flip(image, 1)

            results = hands.process(image)
            chosen_hand, long_len = None, 0
            if results.multi_hand_landmarks:
                for hand in results.multi_hand_landmarks:
                    tip1 = hand.landmark[8]
                    tip2 = hand.landmark[6]

                    if not tip1 or not tip2:
                        break

                    dist = math.dist((tip1.x, tip1.y), (tip2.x, tip2.y))
                    if long_len < dist:
                        chosen_hand = hand.landmark
                        long_len = dist

            if chosen_hand:
                for i in range(21):
                    self.ldm[i] = [chosen_hand[i].x, chosen_hand[i].y]
            else:
                for i in range(21):
                    self.ldm[i] = []
            # GET THE LANDMARKS OF THE CLOSER HAND

            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            cv2.imshow("Window", image)
            key = cv2.waitKey(5) & 0xFF
            if key == 27:
                break

            pass

        for i in range(21):
            self.ldm[i] = []
        self.cap.release()

    def shutdown(self):
        self.exit.set()
