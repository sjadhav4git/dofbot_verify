#!/usr/bin/env python

import json
import numpy as np
from tqdm import tqdm
import math
import rospy
'''
# Read final_path_dofbot
# Generate detail final path --> detailed_final_path.json
# generate joint variables --> joint_var.json
'''

package_path = "/home/jetson/sanket_ws/src/verify"
database_path = package_path+"/database/"


class convert:
    def detailed_path_generate(self,z_touch,z_safe,dist):
        """
        This function generate all 3d points in sequence and store it in detaild_final_path.json
        """
        # Read final_path_dofbot.json
        path_list = self.read_final_path()
        
        p_list = []
        all_points = self.tot_point_list_generate(self.pt_list(path_list,z_touch,z_safe),dist)
        progress_bar = tqdm(total=len(all_points), desc=("Detailed path genrating with resolution {} mm".format(dist)))
        for pl in all_points:
            p_list.append([round(pt,2) for pt in pl])
            progress_bar.update(1)
        progress_bar.close()
        
        self.write_detaild_final_path_json(p_list)

        
    def read_final_path(self):
        json_path = database_path+"final_path_dofbot.json"
        with open(json_path,'r') as json_file:
            data = json.load(json_file)
        path_list = data["final_path_dofbot"]
        return path_list
    
    
    def write_detaild_final_path_json(self,p_list):
        data ={
            "final_path":p_list
        }

        json_data = json.dumps(data,indent=4)
        json_path = database_path+"detailed_final_path.json"
        with open(json_path,"w") as json_file:
            # print("\nFrom : src/dofbot_controller_original_copy/detailed_final_path_gerator.py")
            print("writing_data to detailed_final path")
            json_file.write(json_data)
            print("detailed_final_path (all 3d locations) ready.\nTotal_point: ",len(p_list))
    
    
    def tot_point_list_generate(self, end_point_list,d):
        tot_pt_list = []
        for i in range(len(end_point_list)-1):
            pt1 = end_point_list[i]
            pt2 = end_point_list[i+1]
            # pt_list = (lp.line_points(pt1,pt2,d))
            pt_list = (self.line_points(pt1,pt2,d))
            
            tot_pt_list.append(list(pt_list))
            if i != len(end_point_list)-2:
                tot_pt_list[i].pop(-1)
        flat_list = []
        for sublist in tot_pt_list:
            for element in sublist:
                element = list(element)
                # element = list(round(element,2))
                flat_list.append(element)
                # flat_list.append(round(element,2))
        return (flat_list)
   
    
    def line_points(self, point1,point2,d):
        ponit1 = np.array(point1)
        point2 = np.array(point2)
        distance = np.sqrt(np.sum((point2-ponit1)**2))
        # print('Distance :', distance)
        if distance >2:
            if int(distance)%2 == 0:
                n = int(distance/d) + 1
            else:
                n = int(distance/d) + 2
        elif distance <=2:
            n = 2

        t = np.linspace(0,1, num=n)
        line_points = (ponit1 + t[:,np.newaxis]*(point2 - ponit1))
        return (line_points)


    def pt_list(self, path_list,touch_z,safe_z):
        touch_list = self.p_list(touch_z)
        safe_height_list = self.p_list(safe_z)

        # path_list = [[2,1],[6,2],[10,6],[11,10],[7,11],[6,7],[5,6]]

        final_path_pt_list = []
        for path in path_list:
            final_path_pt_list.append(safe_height_list[path[0]-1])
            final_path_pt_list.append(touch_list[path[0]-1])
            final_path_pt_list.append(touch_list[path[1]-1])
            final_path_pt_list.append(safe_height_list[path[1]-1])
            ##############################
            
        return final_path_pt_list
    
    
    def p_list(self, z):
        x_cords = [Int for Int in range(-65,61,30)]
        y_cords = [Int for Int in range(240,119,-30)]

        all_locations = []
        z -= 4
        
        for y in y_cords:
            for x in x_cords:
                all_locations.append([x,y,z])
            z+=1
        return all_locations
    

class ik:
    def main_ik(self):
        """
        Run this function to save all joint variables to joint_var.json file in database
        """
        print("\nSolving inverse kinematics\nwait...")
        
        
        # with open("src/database/dofbot_details.json","r") as json_read:
        #     data = json.load(json_read)
        data = self.read_dofbot_details()
        l1,l2,l3,l4,finger_len,circum_points = data['l1'],data['l2'],data['l3'],data['l4'],data['finger_len'],data['circum_points']

        l4 += finger_len
        
        # with open("src/database/detailed_final_path.json","r") as json_read:
        #     data = json.load(json_read)

        # final_path_co_ords = data["final_path"]
        
        final_path_co_ords = self.read_detail_path()
        # total = len(final_path_co_ords)
        i = 1
        joint_var_angles = []
        joint_var_locations = []
        # print("count:\n")
        total_itr = len(final_path_co_ords)
        progress_bar = tqdm(total=total_itr, desc="Solving Inverse Kinematics: ")
        
        for pt in final_path_co_ords:
            # print(i,'/',total,end="")
            # sys.stdout.flush()
            th_1,th_2,th_3,th_4,J1_pt,J2_pt,J3_pt,J4_pt = self.joint_variables(pt,l1,l2,l3,l4,circum_points)
            joint_var_angles.append((th_1,th_2,th_3,th_4))
            joint_var_locations.append((J1_pt,J2_pt,J3_pt,J4_pt))
            progress_bar.update(1)
            # print("\r")
        progress_bar.close()
        # data = {
        #     "joint_var_angles" : joint_var_angles,
        #     "joint_var_locations" : joint_var_locations
        # }

        # with open("src/database/joint_var.json","w") as json_write:
        #     json.dump(data,json_write,indent=4)
        self.write_json_var(joint_var_angles,joint_var_locations)


    def read_dofbot_details(self):
        json_path = database_path+"dofbot_details.json"
        with open(json_path,"r") as json_read:
            data = json.load(json_read)        
        return data


    def read_detail_path(self):
        json_path = database_path+"detailed_final_path.json"
        with open(json_path,"r") as json_read:
            data = json.load(json_read)

        final_path_co_ords = data["final_path"]
        return final_path_co_ords


    def write_json_var(self, joint_var_angles, joint_var_locations):
        data = {
            "joint_var_angles" : joint_var_angles,
            "joint_var_locations" : joint_var_locations
        }
        json_path = database_path+"joint_var.json"
        with open(json_path,"w") as json_write:
            json.dump(data,json_write,indent=4)



    def joint_variables(self,P,l1,l2,l3,l4,tot_circum_points):
        """
        input : P [x,y,z]
                dofbot details = l1, l2, l3, l4
                total_circum_points : default = 1999, high number result in high accuracy and high computation.
        Output:
                Joint Variables = th1, th2, th3, th4
                Joint variable location 2d = J1_pt, J2_pt, J3_pt, J4_pt
        """
        th_1 = round(self.th_1(P),2)
        p = self.new_2d_cords(P)
        th_2,th_3,th_4,J3_pt,J4_pt = self.pts_on_circum(p,tot_circum_points,l1,l2,l3,l4)   
        J1_pt = (0,l1)
        J2_pt = self.J2_pt(l2,th_2,J1_pt)
        
        #convet_2d to 3d points
        J1_pt = self.convert_2d_to_3d(J1_pt,th_1)
        J2_pt = self.convert_2d_to_3d(J2_pt,th_1)
        J3_pt = self.convert_2d_to_3d(J3_pt,th_1)
        J4_pt = self.convert_2d_to_3d(J4_pt,th_1)
        
        # return round(th_1,2),round(th_2,2),round(th_3,2),round(th_4,2),round(J1_pt,2),round(J2_pt,2),round(J3_pt,2),round(J4_pt,2)
        return th_1,th_2,th_3,th_4,J1_pt,J2_pt,J3_pt,J4_pt

        
    def th_1(self,P):
        """
        Input: P = (x,y,z)
        Output: th_1
        """
        x,y,z = P[0], P[1], P[2]
        if x != 0:
            theta_1 = np.arctan(y/x)
        else:
            theta_1 = np.deg2rad(90)
        theta_1 = np.rad2deg(theta_1)
        if(theta_1 < 0):
                theta_1 = round(180 + theta_1,2)
        return theta_1


    def new_2d_cords(self,P):
        X,Y,Z = P[0],P[1],P[2]
        x = np.sqrt(X**2 + Y**2)
        y = Z
        p = (round(x,2),round(y,2))
        return p


    def pts_on_circum(self, p,num_points,l1,l2,l3,l4):
        center_x = p[0]
        center_y = p[1]
        alpha = 360/num_points
        points = []
        J2 = [0,l1]
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = center_x + l4 * math.cos(angle)
            y = center_y + l4 * math.sin(angle)
            dist_from_J2 = np.sqrt(((x-J2[0])**2)+((y-J2[1])**2))
            if dist_from_J2<(l2+l3) and dist_from_J2>(np.sqrt(2)*(l2)) and x >= 0 and y>=0:
                
                #===========================================
                J1_pt = [0,l1]
                J3_pt = (round(x,2),round(y,2))
                D = dist_from_J2
                J4_pt = p
                
                th_2,th_3  = self.thetas(J1_pt,J3_pt,l2,D)
                lamda = abs(np.rad2deg(np.arctan2((J4_pt[1]-J3_pt[1]),(J4_pt[0]-J3_pt[0]))))
                th_4 = 90 - (lamda+(th_3+th_2-90))
                theta = th_3+th_2-90
                theta_lamda = theta+lamda
                th_4 = round(90 - theta_lamda,2)
                
                #===========================================
                if th_4>=0 and th_2>=0 and th_3>=0:
                    points.append([x, y])
                    break
        return th_2,th_3,th_4,J3_pt,J4_pt


    def thetas(self, J1_pt,J3_pt,l2,D):
        beta = np.rad2deg(np.arctan2((J3_pt[1] - J1_pt[1]),(J3_pt[0] - J1_pt[0])))
        alpha = np.rad2deg(np.arccos((D/2)/l2))
        th_2 = round((beta + alpha),2)
        phi = 180-(2*alpha)
        th_3 = round(phi - 90,2)
        return th_2,th_3


    def J2_pt(self, l2,th_2,J1_pt):
        x = (l2 * np.cos(np.deg2rad(th_2)))+J1_pt[0]
        y = (l2 * np.sin(np.deg2rad(th_2)))+J1_pt[1]
        J2_point = (round(x,2),round(y,2))
        return J2_point


    def convert_2d_to_3d(self,pt,th1):
        x,y = pt
        Z = y
        Y = round(np.sin(np.deg2rad(th1))*x,2)
        X = round(np.cos(np.deg2rad(th1))*x,2)
        return(X,Y,Z)


if __name__ == '__main__':
    rospy.init_node("convertor",anonymous=True)    
    CONV = convert()
    IK = ik()
    CONV.detailed_path_generate(-6,40,5)
    IK.main_ik()