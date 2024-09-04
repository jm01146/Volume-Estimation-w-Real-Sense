from PredictionData import Depth_Area_Data
from statistics import mean
import openpyxl as xl
import numpy as np

wb_1 = xl.load_workbook("Area_data.xlsx")
area_data = wb_1['sheet1']
wb_2 = xl.load_workbook("Depth_data.xlsx")
depth_data = wb_2['sheet1']

class ScalePxDimensions():
  def __init__(self):
    super().__init__()
    self.area_slope = None
    self.depth_slope = None
    self.area_intercept = None
    self.depth_intercept = None
    self.data_fitting_area()
    self.data_fitting_depth()

  def data_fitting_area(self):
    area_PX = []
    area_MM = []
    area_scale = []
    area_distance = []
    
    for pixel_measurement in area_data['A']:
      area_PX.append(pixel_measurement.value)
    for millimeters_measurement in area_data['B']:
      area_MM.append(millimeters_measurement.value)
    for distance_measurment in area_data['C']:
      area_distance.append(distance_measurement.value)

    for pixel, millimeters in zip(area_PX, area_MM)
      area_scale.append(pixel/millimeters)
      
    self.area_slope = (((mean(area_distance) * mean(area_scale)) - mean(area_distance * area_scale)) / ((mean(area_distance) * mean(area_distance)) - mean(area_distance * area_distance)))
    self.area_intercept = mean(area_scale) - self.area_slope * mean(area_distance)
    return self.area_slope, self.area_intercept

  def data_fitting_depth(self):
    depth_PX = []
    depth_MM = []
    depth_scale = []
    depth_distance = []
    
    for pixel_measurement in depth_data['A']:
      depth_PX.append(pixel_measurement.value)
    for millimeters_measurement in depth_data['B']:
      depth_MM.append(millimeters_measurement.value)
    for distance_measurment in depth_data['C']:
      depth_distance.append(distance_measurement.value)

    for pixel, millimeters in zip(depth_PX, depth_MM)
      depth_scale.append(pixel/millimeters)
      
    self.depth_slope = (((mean(depth_distance) * mean(depth_scale)) - mean(depth_distance * depth_scale)) / ((mean(depth_distance) * mean(depth_distance)) - mean(depth_distance * depth_distance)))
    self.depth_intercept = mean(depth_scale) - self.depth_slope * mean(depth_distance)
    return self.depth_slope, self.depth_intercept

  def get_scale_area(self, area):
    fitted_area = (self.area_slope * area) + self.area_intercept
    return fitted_area

  def get_scale_depth(self, depth):
    fitted_depth = (self.depth_slope * depth) + self.depth_intercept
    return fitted_depth
