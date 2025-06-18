import cv2
import numpy as np
from jetbot import Robot, Camera
import ipywidgets.widgets as widgets
from IPython.display import display
import traitlets
from jetbot import bgr8_to_jpeg
import time

robot = Robot()

image_widget = widgets.Image(format='jpeg', width=300, height=300)
display(image_widget)

camera = Camera.instance()

def find_black_object_center(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            return (cx, cy), thresh
    return None, thresh

def find_green_square(img, black_line_center):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 100, 25])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        contour_area = cv2.contourArea(largest_contour)

        min_area = 0
        if contour_area > min_area:
            box_center = x + w / 2
            if box_center < black_line_center - 10:
                print("Box center is", box_center)
                print("Black line center is", black_line_center)
                return 'left', mask
            elif box_center > black_line_center + 14:
                return 'right', mask
            else:
                return 'uturn', mask

    return None, mask

process_images = True
cooldown_time = 3
last_turn_time = 0.0

def update(change):
    global process_images, last_turn_time
    image = change['new']

    if not process_images:
        return

    height, width = image.shape[:2]
    crop_size = 150
    crop_box = ((width - crop_size) // 2, (height - crop_size) // 2, (width + crop_size) // 2, (height + crop_size) // 2)
    cropped_image = image[crop_box[1]:crop_box[3], crop_box[0]:crop_box[2]]

    center, processed_image = find_black_object_center(cropped_image)

    if center is not None:
        cx, cy = center
        green_direction, green_mask = find_green_square(cropped_image, cx)
        processed_image = cv2.bitwise_or(processed_image, green_mask)
        image_widget.value = cv2.imencode('.jpg', processed_image)[1].tobytes()

        if green_direction == 'left' or green_direction == 'right':
            print(green_direction)
            turn_duration = 0.3
            left_motor_speed = 0.2 if green_direction == 'left' else 0.5
            right_motor_speed = 0.3 if green_direction == 'left' else 0.2

            process_images = False
            time_interval = 0.01
            num_iterations = int(turn_duration / time_interval)

            try:
                if time.time() - last_turn_time > cooldown_time:
                    for i in range(num_iterations):
                        progress = i / num_iterations
                        current_left_speed = left_motor_speed * (1 - progress)
                        current_right_speed = right_motor_speed * (1 - progress)
                        robot.set_motors(current_left_speed, current_right_speed)
                        time.sleep(time_interval)
                    last_turn_time = time.time()
            finally:
                robot.stop()
                process_images = True

        elif green_direction == 'uturn':
            print(green_direction)
            turn_duration = 0.4
            left_motor_speed = 0.8
            right_motor_speed = 0.1

            process_images = False
            time_interval = 0.01
            num_iterations = int(turn_duration / time_interval)

            try:
                if time.time() - last_turn_time > cooldown_time:
                    for i in range(num_iterations):
                        progress = i / num_iterations
                        current_left_speed = left_motor_speed * (1 - progress)
                        current_right_speed = right_motor_speed * (1 - progress)
                        robot.set_motors(current_left_speed, current_right_speed)
                        time.sleep(time_interval)
                    last_turn_time = time.time()
            finally:
                robot.stop()
                process_images = True

        else:
            if cx < int(crop_size * 0.2):
                robot.left(0.16)
            elif cx > int(crop_size * 0.6):
                robot.right(0.16)
            else:
                robot.forward(0.18)
    else:
        robot.forward(0.1)

camera_link = traitlets.dlink((camera, 'value'), (image_widget, 'value'), transform=bgr8_to_jpeg)
camera.observe(update, names='value')

time.sleep(0.01)
