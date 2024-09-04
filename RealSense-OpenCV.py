from PredictScales import ScalePxDimensions
import pyrealsense2 as rs
import numpy as np
import cv2

ctx = rs.context()
rs_device = []
for reItems in ctx.devices:
  rs_device.append(rsItems.get_info(rs.camera_info.serial_number))

cam_1 = rs.pipeline()
config_1 = rs.config()
config_1.enable_device(rs_device[0])
config_1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config_1.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

cam_2 = rs.pipeline()
config_2 = rs.config()
config_2.enable_device(rs_device[1])
config_2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config_2.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

cam_1.start(config_1)
cam_2.start(config_2)

# Green color detection limits
green_lower = np.array([50, 50, 50], dtype=np.uint8)
green_upper = np.array([90, 255, 255], dtype=np.uint8)

# filter resolution
kernel = np.ones((25, 25), np.uint8)

predictScales = ScalePxDimension()

# Accesses camera and finds the targeted color and displays it
while True:
  ret, frame = cam_1.wait_for_frames()
  color_frame = frame.get_color_frame()
  color_image = np.asanarray(color_frame.get_data())
  depth_frame = frame.get_depth_frame()
  depth_image = np.asanarray(depth_frame.get_data())
  
  hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, green_lower, green_upper)
  mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
  mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
  
  mask_contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  results = frame.copy()
  results = cv2.drawContours(results, mask_contours, -1, (0, 0, 255), 3)

    # crates a box around the targeted color
  if len(mask_contours) != 0:
      for mask_contour in mask_contours:
          if cv2.contourArea(mask_contour) > 1500:
            M = cv2.moments(mask_contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(color_image, (cX, cY), 7, (255, 255, 255), -1)
            x, y, w, h = cv2.boundingRect(mask_contour)
            cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 0, 255), 3)
            depth_calibration = depth_image.get_distance(cX, cY)
            depth = predictScales.get_scale_depth(depth_calibration)
            area = predictScale.get_scale_area(mask_contour)
            volume = depth * area
            print(f"\rVolume:{volume}", end="")

# This shows the photo with the box, the mask, and what the computer will see before putting a box this is for debugging
# purposes
    cv2.imshow('Frame', frame)
    cv2.imshow('HSV', hsv)
    cv2.imshow('Mask', mask)
    cv2.imshow('Results', results)

# Waits for the user to hit the q button to close program #
    if cv2.waitKey(1) == ord('q'):
        break

# Allows to release the picture to free used system resources #
cap.release()
cv2.destroyAllWindows()
cam_1.stop()
cam_2.stop()
