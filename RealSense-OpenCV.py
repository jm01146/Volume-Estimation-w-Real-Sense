import PredictScales import ScalePxDimensions
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

