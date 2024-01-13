#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float64MultiArray
from Arm_Lib import Arm_Device
import numpy as np
import time
import json


Arm = Arm_Device()
msg = Float64MultiArray()
package_path = "/home/jetson/sanket_ws/src/verify"
database_path = package_path+"/database/"

class Movements:
    def user(self,user_array,dt):    
        Arm.Arm_serial_servo_write6(user_array[0], user_array[1], user_array[2], user_array[3], 90.0, 180.0, dt)
        time.sleep(round((dt/1000),1))

    def go_home(self,dt):
        self.user([90,90,90,90],dt)

    def go_to_target(self,dt):
        self.user([0,90,0,0],dt)
        pass
    
    
    # def move_to_cap_target():
    #     user([0,90,90,90],1000)
    #     time.sleep(1)
    #     user([0,120,30,-30],1000)
    #     time.sleep(1)
    #     user([0,90,30,-30],500)
    #     time.sleep(0.5)
    #     user([0,90,0,0],500)
    #     time.sleep(0.5)
        
        
    def go_to_puzzle(self,dt):
        self.user([90,98,55,-47],dt)



class ImageSubscriber:
    def __init__(self, topic_name):
        self.bridge = CvBridge()
        self.image = None

        # Subscribe to the specified topic
        self.image_sub = rospy.Subscriber(topic_name, Image, self.image_callback)

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV format
            self.image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

        except CvBridgeError as e:
            rospy.logerr("Error converting ROS Image to OpenCV format: %s", str(e))

    def get_image(self):
        # Return the latest image
        return self.image
   
   
    
class Pattern:
    def find_puzzle_pattern(self,image):
        image = self.perspective_crop(image)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        color_ranges = {
            'R': ([100, 120, 100], [190, 205, 255]),
            'G': ([40, 40, 40], [80, 255, 255]),
            'B': ([100, 100, 100], [140, 255, 255]),
            'Y': ([20, 60, 150], [40, 155, 255]),
            'W': ([0, 0, 200], [180, 30, 255]),
            'O': ([0, 100, 200], [25, 255, 255]),
            '0': ([100, 0, 0],[200, 100, 100])
        }
        
        i = 0
        color_pattern = np.empty((5, 5), dtype=object)
        for row in range(5):
            for col in range(5):
                # Crop the region of interest for each face
                x_start, y_start = col * (image.shape[1] // 5), row * (image.shape[0] // 5)
                # x_start, y_start = x_start+20, y_start+20
                x_end, y_end = (col + 1) * (image.shape[1] // 5), (row + 1) * (image.shape[0] // 5)
                # x_end,y_end = x_end-20, y_end-20
                # print([x_start,y_start],[x_end,y_end])
                cv2.rectangle(image, (x_start,y_start), (x_end,y_end), (0,255,255), 2)
                face_roi = hsv[y_start:y_end, x_start:x_end, :]
                nm = str(i)
                # cv2.imshow(nm,face_roi)
                i+=1
                color_counts = {}
                
                for color, (lower, upper) in color_ranges.items():
                    mask = cv2.inRange(face_roi, np.array(lower), np.array(upper))
                    color_counts[color] = cv2.countNonZero(mask)
                # print()
                # print(i, 'color_counts', color_counts)
                
                dominant_color = max(color_counts, key=color_counts.get)
                color_pattern[row, col] = dominant_color
                
                # cv2.putText(hsv, str(dominant_color,str(color_counts[dominant_color])), (x_start+5, y_start+2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
                cv2.putText(hsv, str(color_counts[dominant_color]), (x_start+5, y_end-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        print("Puzzle_pattern")
        print(color_pattern)
        
        # cv2.imshow("img", image)
        # cv2.imshow("hsv", hsv)
        # cv2.waitKey(2000)
        # cv2.destroyAllWindows()
        
        return color_pattern


    def perspective_crop(self,image):
        # Define the size of the output image
        width, height = 480, 480

        pts_original = np.array([[70, 8], [590, 0], [640, 480], [40, 480]], dtype=np.float32)
        # Define the coordinates of the four corners of the desired output
        # pts_output = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)
        pts_output = np.array([[0, 0], [width - 1, 0], [width - 30, height - 1], [0, height - 1]], dtype=np.float32)

        # Calculate the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(pts_original, pts_output)

        # Apply the perspective transform to the image
        result = cv2.warpPerspective(image, matrix, (width, height))

        # Display the result
        # cv2.imshow('Perspective Crop', result)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return result

    
    def find_tartet_pattern(self,image):
        x, y, x1, y1 = 166, 81, 477, 382  

        # Crop the region of interest from the original image
        image = image[y:y1, x:x1]
        # image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
        # image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)
        image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # color_ranges = {
        #     'R': ([150, 120, 100], [190, 205, 255]),
        #     'G': ([40, 40, 40], [80, 255, 255]),
        #     'B': ([100, 100, 100], [140, 255, 255]),
        #     'Y': ([20, 100, 100], [40, 255, 255]),
        #     'W': ([0, 0, 200], [180, 30, 255]),
        #     'O': ([0, 100, 100], [10, 255, 255])
        # }
        
            # 'R': ([150, 80, 170], [190, 205, 255]),
            
        color_ranges = {
            'R': ([100, 100, 100], [180, 255, 255]),
            'G': ([40, 40, 40], [80, 255, 255]),
            'B': ([100, 130, 80], [135, 255, 250]),
            'Y': ([20, 100, 100], [40, 255, 255]),
            'W': ([0, 0, 150], [100, 30, 255]),
            'O': ([0, 100, 100], [10, 255, 255])
        }
        
        i = 0
        color_pattern = np.empty((3, 3), dtype=object)
        for row in range(3):
            for col in range(3):
                # Crop the region of interest for each face
                x_start, y_start = col * (image.shape[1] // 3), row * (image.shape[0] // 3)
                x_end, y_end = (col + 1) * (image.shape[1] // 3), (row + 1) * (image.shape[0] // 3)
                # face_roi = hsv[y_start:y_end, x_start:x_end, :]
                # print([x_start,y_start],[x_end,y_end])
                cv2.rectangle(image, (x_start,y_start), (x_end,y_end), (0,255,255), 2)
                
                face_roi = hsv[y_start:y_end, x_start:x_end, :]
                nm = str(i)
                # cv2.imshow(nm,face_roi)
                i+=1
                color_counts = {}
                
                for color, (lower, upper) in color_ranges.items():
                    mask = cv2.inRange(face_roi, np.array(lower), np.array(upper))
                    color_counts[color] = cv2.countNonZero(mask)
                # print()
                # print(i, 'color_counts', color_counts)
                
                dominant_color = max(color_counts, key=color_counts.get)
                color_pattern[row, col] = dominant_color
                cv2.putText(hsv, str(color_counts[dominant_color]), (x_start+5, y_end-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        print("/n Tanget pattern")
        print(color_pattern)
        # cv2.imshow("img", image)
        # cv2.imshow("hsv", hsv)
        # cv2.waitKey(2000)
        # cv2.destroyAllWindows()
        
        return color_pattern
 



 

def get_image_from_topic(topic_name):
    # Initialize ROS node
    rospy.init_node('image_subscriber', anonymous=True)

    # Create an ImageSubscriber instance for the specified topic
    image_subscriber = ImageSubscriber(topic_name)

    # Wait for the first image to be received
    while image_subscriber.get_image() is None and not rospy.is_shutdown():
        rospy.sleep(0.1)

    # Return the retrieved image
    return image_subscriber.get_image()


def save_img(img, img_name):
    img_path = database_path+img_name
    
    if img is not None:     
        cv2.imwrite(img_path,img)
        # cv2.imshow("Retrieved Image", img)     
        # cv2.waitKey(0)
    else:
        rospy.logerr("Failed to retrieve image from the specified topic.")
   
   
class verify_patten:
    
    def loop(self,RC,color,pattern):
        current_color_count = 0
        for i in range(RC):
            for j in range(RC):
                if pattern[i][j] == color:
                    current_color_count +=1
        return current_color_count
    
    def check_puzzle(self,puzzle_pattern):
        puzzle_ok = True
        colors = ['R', 'G', 'B', 'Y','W','O']
        for color in colors:
            current_color_count = self.loop(5,color,puzzle_pattern)            
            if current_color_count > 4:
                puzzle_ok = False
                print("Failed to capture, capturing again")
                return puzzle_ok
        blank = self.loop(5,'0',puzzle_pattern)
        if blank > 1:
            puzzle_ok = False
            print("Failed to capture, capturing again")
            return puzzle_ok
        return puzzle_ok
    
    def check_target(self,target_pattern):
        target_ok = True    
        colors = ['R', 'G', 'B', 'Y','W','O']
        for color in colors:
            current_color_count = self.loop(3,color,target_pattern)            
            if current_color_count > 4:
                target_ok = False
                print("color : ",color," -> count",current_color_count)
                print("shuffle_again")
                return target_ok
        return target_ok
        
    # puzzle_ok = check_puzzle(puzzle_pattern)
    # target_ok = check_target(target_pattern)
    
    # return puzzle_ok,target_ok


VP = verify_patten()
  
def main_reading_sequence():
    '''
    move to home
    move to target
    capture and save target
    move to puzzle
    capture and save puzzle
    '''
    move = Movements()
    pattern = Pattern()
    move.go_home(2000)
    
    # Read and save puzzle_pattern
    def cap_puzzle():
        move.go_to_puzzle(2000)
        time.sleep(2)
        retrieved_image = get_image_from_topic('/camera_image')
        save_img(retrieved_image,'puzzle.jpg')
        puzzle_pattern = pattern.find_puzzle_pattern(retrieved_image)
        # print("Puzzle_pattern")
        # print(puzzle_pattern)
        puzzle_pattern = puzzle_pattern.tolist()
        puzzle = VP.check_puzzle(puzzle_pattern)
        if puzzle == True:
            return puzzle_pattern
        else:
            time.sleep(1)
            cap_puzzle()
    
    # Read and save target pattern
    def cap_target():
        move.go_to_target(1000)
        time.sleep(2)
        retrieved_image = get_image_from_topic('/camera_image')
        save_img(retrieved_image,'target.jpg')
        target_pattern = pattern.find_tartet_pattern(retrieved_image)
        # print("/n Tanget pattern")
        # print(target_pattern)
        target_pattern = target_pattern.tolist()
        target = VP.check_target(target_pattern)
        if target == True:
            return target_pattern
        else:
            time.sleep(1)
            cap_target()
    
    
    def save(puzzle_pattern,target_pattern):
        data = {
                "puzzle_pattern": puzzle_pattern,  
                "target_pattern": target_pattern
            }
        json_file_name = 'patterns.json'
        json_file_path = database_path+json_file_name
        with open(json_file_path,'w') as json_file:
            json.dump(data,json_file,indent=4)
        rospy.loginfo("patterns.json saved")
    
    puzzle_pattern = cap_puzzle()
    target_pattern = cap_target()
    save(puzzle_pattern,target_pattern)
    move.go_to_puzzle(2000)
    

if __name__ == '__main__':
    try:
        main_reading_sequence()
                
        rospy.loginfo("capture and save successful")
    except:
        rospy.loginfo("Capture Failed")
        pass