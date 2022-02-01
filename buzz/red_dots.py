import numpy as np

from common_file import labelMe_class
from common_file.return_class import RetClass
from common_file.common_function import *

def pattern_overlay(image, pattern, x_pos, y_pos):
	result = image.copy()

	alpha = pattern[..., 3] / 255
	cutout = result[y_pos:y_pos + pattern.shape[0], x_pos:x_pos + pattern.shape[1]]
	for i in range(3):
		cutout[..., i] = (cutout[..., i] * (1 - alpha)) + (pattern[..., i] * alpha)

	return result

def rot_image(image, angle):
	height, width, dim = image.shape
	hypotenuse = int(np.sqrt(height**2 + width**2) + 1)
	border_h = hypotenuse - height
	border_w = hypotenuse - width
	big_image = np.zeros(shape = (height + border_h, width + border_w, dim), dtype = np.uint8)
	big_image[border_h//2:border_h//2 + height, border_w//2:border_w//2 + width] = image

	height, width = big_image.shape[:2]
	center = (width // 2, height // 2)
	rotate_matrix = cv2.getRotationMatrix2D(center = center, angle = angle, scale = 1)
	rotated_image = cv2.warpAffine(src = big_image, M = rotate_matrix, dsize = (width, height))

	return rotated_image

def red_dots(image, label, need_BGR2RGB_4_pat = True):
	"""
	need_BGR2RGB_4_pat: bool = True
		Opencv uses the BGR color scheme by default. But, if the color of
		the anomalies does not correspond to the correct one, then it
		is worth changing the parameter to the opposite value.
	"""

	#load pattern
	pattern = cv2.imread('red_dots/Red_dot.png', flags = cv2.IMREAD_UNCHANGED)
	if need_BGR2RGB_4_pat == True:
		pattern = cv2.cvtColor(pattern, cv2.COLOR_BGRA2RGBA)

	#anomaly generation
	num_anomalies = np.random.randint(2, 10)
	markup = []

	for i in range(num_anomalies):
		#rotation
		angle = np.random.randint(0, 359)
		rot_pattern = rot_image(pattern, angle)

		#resize
		min_side = np.min(image.shape[:2])
		scale_percent = ((4.2 - 2.8) * np.random.random_sample() + 4.2) / 100
		scale = int(min_side * scale_percent)
		min_side_pattern = np.min(rot_pattern.shape[:2])
		scale /= min_side_pattern
		rot_pattern = cv2.resize(rot_pattern, None, fx = scale, fy = scale, interpolation = cv2.INTER_LINEAR)

		#draw
		pos_x = np.random.randint(0, image.shape[1] - rot_pattern.shape[1])
		pos_y = np.random.randint(0, image.shape[0] - rot_pattern.shape[1])
		image = pattern_overlay(image, rot_pattern, pos_x, pos_y)

		#markup
		layout = [[pos_x,                        pos_y],
				  [pos_x,                        pos_y + rot_pattern.shape[1]],
				  [pos_x + rot_pattern.shape[0], pos_y + rot_pattern.shape[1]],
				  [pos_x + rot_pattern.shape[0], pos_y]]
		markup.append(labelMe_class.Shapes(label, layout, None, "polygon", {}))

	return RetClass(image, markup)