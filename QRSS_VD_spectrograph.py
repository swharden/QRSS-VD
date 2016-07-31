#!/usr/bin/env python
# QRSS_VD.py
 
"""QRSS VD - high resolution spectrum analyzer by Scott Harden, AJ4VD."""

"""
   Written by: Scott Harden, AJ4VD (SWHarden@gmail.com)
      Website: http://www.SWHarden.com

Note: I'm not a programmer.  I'm a molecular biologist, and a dental student.
I code when I'm bored, and often I'm bored when I code, so this is a total mess.
If it works, it works, right?
"""

version = 1.05


from PIL import JpegImagePlugin
from PIL import TgaImagePlugin
from PIL import PngImagePlugin
from PIL import GifImagePlugin
from PIL import PcxImagePlugin
from PIL import PpmImagePlugin
from PIL import BmpImagePlugin
from PIL import FliImagePlugin
from PIL import EpsImagePlugin
from PIL import DcxImagePlugin
from PIL import FpxImagePlugin
from PIL import ArgImagePlugin
from PIL import CurImagePlugin
from PIL import GbrImagePlugin
from PIL import IcoImagePlugin
from PIL import ImImagePlugin
from PIL import ImtImagePlugin
from PIL import IptcImagePlugin
from PIL import McIdasImagePlugin
from PIL import MicImagePlugin
from PIL import MspImagePlugin
from PIL import PcdImagePlugin
from PIL import PdfImagePlugin
from PIL import PixarImagePlugin
from PIL import PsdImagePlugin
from PIL import SgiImagePlugin
from PIL import SunImagePlugin
from PIL import TgaImagePlugin
from PIL import TiffImagePlugin
from PIL import WmfImagePlugin
from PIL import XVThumbImagePlugin
from PIL import XbmImagePlugin
from PIL import XpmImagePlugin

import os
import pyaudio
import scipy
from scipy import stats
import struct
import scipy.fftpack
from Tkinter import *
import threading
import time, datetime
import math
#import Image
from PIL import ImageTk
from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
from PIL import ImageDraw
from PIL import ImageFilter
import random
import webbrowser
import tkMessageBox
import tkSimpleDialog
import string
#import colors
#colormap=colors.colormap_blue

#_icon = wx.EmptyIcon()
#_icon.CopyFromBitmap(wx.Bitmap("icon.ico", wx.BITMAP_TYPE_ANY))
#self.SetIcon(_icon)

colormap_blue=[(255, 247, 251), (254, 246, 250), (253, 245, 250), (252, 244, 249), (252, 244, 249), (252, 244, 249), (250, 243, 249), (250, 242, 248), (249, 242, 248), (249, 241, 248), (249, 241, 248), (247, 240, 247), (247, 240, 247), (246, 239, 247), (246, 239, 246), (246, 239, 246), (244, 238, 246), (244, 237, 245), (243, 237, 245), (243, 236, 245), (242, 236, 245), (241, 235, 244), (241, 235, 244), (240, 234, 244), (240, 234, 243), (239, 233, 243), (238, 233, 243), (238, 232, 243), (237, 232, 242), (237, 231, 242), (236, 231, 242), (235, 230, 241), (235, 230, 241), (234, 229, 241), (233, 228, 240), (232, 228, 240), (231, 227, 240), (230, 226, 239), (229, 226, 239), (228, 225, 238), (227, 224, 238), (227, 224, 238), (226, 223, 237), (225, 222, 237), (224, 221, 237), (223, 221, 236), (222, 220, 236), (221, 219, 235), (220, 219, 235), (220, 218, 235), (219, 217, 234), (218, 217, 234), (217, 216, 234), (216, 215, 233), (215, 215, 233), (214, 214, 232), (213, 213, 232), (213, 212, 232), (212, 212, 231), (211, 211, 231), (210, 210, 231), (209, 210, 230), (208, 209, 230), (207, 208, 229), (206, 208, 229), (205, 207, 229), (204, 206, 228), (202, 206, 228), (201, 205, 228), (199, 205, 227), (198, 204, 227), (197, 203, 227), (196, 203, 226), (194, 202, 226), (193, 201, 226), (191, 201, 225), (190, 200, 225), (189, 200, 225), (187, 199, 224), (186, 198, 224), (185, 198, 224), (184, 197, 223), (182, 196, 223), (181, 196, 223), (180, 195, 222), (178, 195, 222), (177, 194, 221), (176, 193, 221), (174, 193, 221), (173, 192, 220), (172, 191, 220), (170, 191, 220), (169, 190, 219), (168, 190, 219), (166, 189, 219), (165, 188, 218), (163, 188, 218), (162, 187, 218), (160, 186, 217), (159, 186, 217), (157, 185, 216), (156, 185, 216), (154, 184, 216), (152, 183, 215), (151, 183, 215), (149, 182, 215), (148, 181, 214), (146, 181, 214), (145, 180, 213), (143, 179, 213), (141, 179, 213), (140, 178, 212), (138, 178, 212), (137, 177, 212), (135, 176, 211), (134, 176, 211), (132, 175, 210), (130, 174, 210), (129, 174, 210), (127, 173, 209), (126, 173, 209), (124, 172, 209), (123, 171, 208), (121, 171, 208), (119, 170, 207), (118, 169, 207), (116, 169, 207), (115, 168, 206), (113, 167, 206), (111, 167, 205), (109, 166, 205), (107, 165, 204), (105, 164, 204), (103, 163, 203), (101, 163, 203), (99, 162, 203), (97, 161, 202), (95, 160, 202), (93, 159, 201), (91, 159, 201), (89, 158, 200), (87, 157, 200), (85, 156, 199), (83, 156, 199), (81, 155, 198), (80, 154, 198), (78, 153, 197), (76, 152, 197), (74, 152, 196), (72, 151, 196), (70, 150, 195), (68, 149, 195), (66, 149, 195), (64, 148, 194), (62, 147, 194), (60, 146, 193), (58, 145, 193), (56, 145, 192), (54, 144, 192), (53, 143, 191), (51, 142, 191), (49, 141, 190), (48, 140, 190), (46, 139, 189), (45, 138, 189), (43, 137, 188), (42, 136, 188), (40, 135, 187), (39, 134, 187), (37, 133, 186), (36, 132, 186), (34, 131, 185), (33, 130, 185), (31, 129, 184), (29, 128, 184), (28, 127, 183), (26, 126, 183), (25, 125, 182), (23, 124, 182), (22, 123, 181), (20, 122, 181), (19, 121, 180), (17, 120, 180), (16, 119, 179), (14, 118, 179), (13, 117, 178), (11, 116, 178), (9, 115, 177), (8, 114, 177), (6, 113, 176), (5, 112, 176), (4, 111, 175), (4, 110, 174), (4, 110, 172), (4, 109, 171), (4, 108, 170), (4, 108, 169), (4, 107, 168), (4, 106, 167), (4, 105, 166), (4, 105, 165), (4, 104, 164), (4, 103, 163), (4, 103, 161), (4, 102, 160), (4, 101, 159), (4, 101, 158), (4, 100, 157), (4, 99, 156), (4, 99, 155), (4, 98, 154), (4, 97, 153), (4, 96, 152), (4, 96, 150), (4, 95, 149), (4, 94, 148), (4, 94, 147), (4, 93, 146), (4, 92, 145), (4, 92, 144), (4, 91, 143), (4, 90, 142), (4, 90, 140), (3, 89, 138), (3, 87, 137), (3, 86, 135), (3, 85, 133), (3, 84, 132), (3, 83, 130), (3, 82, 128), (3, 81, 127), (3, 80, 125), (3, 79, 123), (3, 78, 122), (3, 77, 120), (3, 76, 118), (3, 75, 117), (3, 74, 115), (3, 73, 113), (2, 71, 112), (2, 70, 110), (2, 69, 108), (2, 68, 107), (2, 67, 105), (2, 66, 103), (2, 65, 102), (2, 64, 100), (2, 63, 98), (2, 62, 97), (2, 61, 95), (2, 60, 93), (2, 59, 92), (2, 58, 90), (2, 57, 89), (2, 58, 90), (2, 57, 89)]
colormap_blue.reverse()
colormap_green=[(255, 255, 228), (254, 254, 227), (254, 254, 225), (253, 254, 223), (253, 254, 222), (253, 254, 221), (253, 254, 219), (252, 254, 218), (252, 254, 216), (252, 254, 215), (252, 253, 214), (251, 253, 212), (251, 253, 211), (251, 253, 210), (251, 253, 208), (250, 253, 207), (250, 253, 205), (250, 253, 204), (250, 253, 203), (249, 253, 201), (249, 253, 200), (249, 252, 199), (249, 252, 197), (248, 252, 196), (248, 252, 194), (248, 252, 193), (248, 252, 192), (247, 252, 190), (247, 252, 189), (247, 252, 187), (247, 252, 186), (246, 251, 185), (245, 251, 184), (245, 251, 183), (244, 250, 182), (243, 250, 182), (242, 250, 181), (241, 249, 180), (240, 249, 180), (239, 248, 179), (238, 248, 178), (237, 248, 178), (236, 247, 177), (235, 247, 176), (234, 247, 175), (233, 246, 175), (232, 246, 174), (231, 245, 173), (230, 245, 173), (229, 245, 172), (229, 244, 171), (228, 244, 171), (227, 244, 170), (226, 243, 169), (225, 243, 169), (224, 242, 168), (223, 242, 167), (222, 242, 166), (221, 241, 166), (220, 241, 165), (219, 241, 164), (218, 240, 164), (217, 240, 163), (216, 239, 162), (215, 239, 162), (213, 238, 161), (212, 238, 160), (211, 237, 160), (210, 236, 159), (208, 236, 158), (206, 235, 158), (205, 235, 157), (204, 234, 156), (202, 233, 156), (201, 233, 155), (200, 232, 154), (199, 232, 154), (197, 231, 153), (195, 230, 152), (194, 230, 152), (193, 229, 151), (192, 229, 150), (190, 228, 150), (189, 227, 149), (187, 227, 149), (186, 226, 148), (184, 226, 147), (183, 225, 147), (182, 224, 146), (180, 224, 145), (179, 223, 145), (178, 223, 144), (176, 222, 143), (175, 221, 143), (173, 221, 142), (172, 220, 141), (170, 220, 141), (169, 219, 140), (167, 218, 139), (165, 217, 139), (164, 217, 138), (162, 216, 137), (160, 215, 137), (159, 214, 136), (157, 214, 135), (155, 213, 135), (154, 212, 134), (152, 212, 133), (150, 211, 133), (149, 210, 132), (147, 209, 131), (145, 209, 131), (144, 208, 130), (142, 207, 129), (140, 207, 129), (139, 206, 128), (137, 205, 127), (135, 204, 127), (134, 204, 126), (132, 203, 125), (130, 202, 125), (129, 201, 124), (127, 201, 123), (125, 200, 123), (124, 199, 122), (122, 199, 121), (120, 198, 121), (119, 197, 120), (117, 196, 119), (115, 195, 118), (113, 195, 117), (112, 194, 117), (110, 193, 116), (108, 192, 115), (107, 191, 114), (105, 190, 113), (103, 189, 112), (101, 189, 111), (100, 188, 110), (98, 187, 110), (96, 186, 109), (94, 185, 108), (93, 184, 107), (91, 184, 106), (89, 183, 105), (88, 182, 104), (86, 181, 103), (84, 180, 102), (82, 179, 102), (81, 178, 101), (79, 178, 100), (77, 177, 99), (76, 176, 98), (74, 175, 97), (72, 174, 96), (70, 173, 95), (69, 173, 95), (67, 172, 94), (65, 171, 93), (64, 170, 92), (63, 169, 91), (62, 167, 90), (61, 166, 90), (60, 165, 89), (59, 164, 88), (58, 162, 87), (57, 161, 86), (56, 160, 85), (55, 159, 85), (55, 158, 84), (54, 156, 83), (53, 155, 82), (52, 154, 81), (51, 153, 81), (50, 151, 80), (49, 150, 79), (48, 149, 78), (47, 148, 77), (46, 146, 76), (45, 145, 76), (44, 144, 75), (43, 143, 74), (42, 142, 73), (41, 140, 72), (40, 139, 72), (39, 138, 71), (39, 137, 70), (38, 135, 69), (37, 134, 68), (36, 133, 68), (35, 132, 67), (34, 131, 66), (33, 130, 66), (31, 129, 65), (30, 128, 65), (29, 127, 65), (28, 126, 64), (27, 126, 64), (26, 125, 64), (25, 124, 63), (24, 123, 63), (23, 122, 62), (22, 121, 62), (21, 120, 62), (19, 119, 61), (18, 119, 61), (17, 118, 61), (16, 117, 60), (15, 116, 60), (14, 115, 59), (13, 114, 59), (12, 113, 59), (11, 112, 58), (9, 112, 58), (8, 111, 58), (7, 110, 57), (6, 109, 57), (5, 108, 56), (4, 107, 56), (3, 106, 56), (2, 105, 55), (1, 104, 55), (0, 104, 55), (0, 102, 54), (0, 101, 54), (0, 100, 53), (0, 99, 53), (0, 98, 52), (0, 97, 52), (0, 96, 51), (0, 95, 51), (0, 94, 51), (0, 93, 50), (0, 91, 50), (0, 90, 49), (0, 89, 49), (0, 88, 48), (0, 87, 48), (0, 86, 48), (0, 85, 47), (0, 84, 47), (0, 83, 46), (0, 82, 46), (0, 80, 45), (0, 79, 45), (0, 78, 44), (0, 77, 44), (0, 76, 44), (0, 75, 43), (0, 74, 43), (0, 73, 42), (0, 72, 42), (0, 71, 41), (0, 70, 41), (0, 71, 41), (0, 70, 41)]
colormap_green.reverse()
colormap_logo=[(0, 0, 129), (0, 0, 134), (0, 0, 139), (0, 0, 143), (0, 0, 148), (0, 0, 152), (0, 0, 157), (0, 0, 161), (0, 0, 166), (0, 0, 170), (0, 0, 175), (0, 0, 180), (0, 0, 184), (0, 0, 189), (0, 0, 193), (0, 0, 198), (0, 0, 202), (0, 0, 207), (0, 0, 211), (0, 0, 216), (0, 0, 220), (0, 0, 225), (0, 0, 230), (0, 0, 234), (0, 0, 239), (0, 0, 243), (0, 0, 248), (0, 0, 252), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 0, 255), (0, 2, 255), (0, 7, 255), (0, 11, 255), (0, 14, 255), (0, 18, 255), (0, 23, 255), (0, 27, 255), (0, 31, 255), (0, 34, 255), (0, 39, 255), (0, 43, 255), (0, 47, 255), (0, 51, 255), (0, 54, 255), (0, 59, 255), (0, 63, 255), (0, 67, 255), (0, 71, 255), (0, 75, 255), (0, 79, 255), (0, 83, 255), (0, 87, 255), (0, 91, 255), (0, 95, 255), (0, 99, 255), (0, 103, 255), (0, 107, 255), (0, 111, 255), (0, 115, 255), (0, 119, 255), (0, 123, 255), (0, 127, 255), (0, 131, 255), (0, 135, 255), (0, 139, 255), (0, 143, 255), (0, 147, 255), (0, 151, 255), (0, 155, 255), (0, 159, 255), (0, 163, 255), (0, 167, 255), (0, 171, 255), (0, 175, 255), (0, 179, 255), (0, 183, 255), (0, 187, 255), (0, 191, 255), (0, 195, 255), (0, 199, 255), (0, 203, 255), (0, 207, 255), (0, 211, 255), (0, 215, 255), (0, 219, 254), (0, 223, 251), (0, 227, 248), (2, 231, 245), (5, 235, 241), (7, 239, 238), (11, 243, 235), (14, 247, 232), (18, 251, 228), (21, 255, 225), (23, 255, 222), (27, 255, 219), (31, 255, 215), (34, 255, 212), (37, 255, 208), (40, 255, 205), (44, 255, 203), (47, 255, 199), (50, 255, 195), (54, 255, 192), (57, 255, 189), (60, 255, 186), (63, 255, 183), (66, 255, 179), (70, 255, 176), (73, 255, 173), (76, 255, 170), (79, 255, 166), (83, 255, 163), (86, 255, 160), (89, 255, 157), (92, 255, 154), (95, 255, 150), (99, 255, 147), (102, 255, 144), (105, 255, 141), (108, 255, 137), (112, 255, 134), (115, 255, 131), (118, 255, 128), (121, 255, 125), (124, 255, 121), (128, 255, 118), (131, 255, 115), (134, 255, 112), (137, 255, 108), (141, 255, 105), (144, 255, 102), (147, 255, 99), (150, 255, 95), (154, 255, 92), (157, 255, 89), (160, 255, 86), (163, 255, 83), (166, 255, 79), (170, 255, 76), (173, 255, 73), (176, 255, 70), (179, 255, 66), (183, 255, 63), (186, 255, 60), (189, 255, 57), (192, 255, 54), (195, 255, 50), (199, 255, 47), (202, 255, 44), (205, 255, 41), (208, 255, 37), (212, 255, 34), (215, 255, 31), (218, 255, 28), (221, 255, 24), (224, 255, 21), (228, 255, 18), (231, 255, 15), (234, 255, 12), (238, 255, 8), (241, 252, 5), (244, 248, 2), (247, 244, 0), (250, 240, 0), (254, 236, 0), (255, 233, 0), (255, 229, 0), (255, 226, 0), (255, 221, 0), (255, 218, 0), (255, 215, 0), (255, 211, 0), (255, 207, 0), (255, 203, 0), (255, 199, 0), (255, 196, 0), (255, 192, 0), (255, 188, 0), (255, 184, 0), (255, 180, 0), (255, 177, 0), (255, 173, 0), (255, 169, 0), (255, 165, 0), (255, 162, 0), (255, 159, 0), (255, 155, 0), (255, 151, 0), (255, 147, 0), (255, 143, 0), (255, 140, 0), (255, 136, 0), (255, 132, 0), (255, 128, 0), (255, 125, 0), (255, 121, 0), (255, 117, 0), (255, 114, 0), (255, 110, 0), (255, 106, 0), (255, 102, 0), (255, 99, 0), (255, 95, 0), (255, 91, 0), (255, 88, 0), (255, 84, 0), (255, 80, 0), (255, 76, 0), (255, 73, 0), (255, 69, 0), (255, 65, 0), (255, 62, 0), (255, 58, 0), (255, 54, 0), (255, 51, 0), (255, 47, 0), (255, 43, 0), (255, 39, 0), (255, 36, 0), (255, 32, 0), (255, 28, 0), (255, 25, 0), (255, 21, 0), (253, 17, 0), (248, 14, 0), (244, 10, 0), (240, 6, 0), (235, 2, 0), (230, 0, 0), (225, 0, 0), (221, 0, 0), (217, 0, 0), (212, 0, 0), (207, 0, 0), (203, 0, 0), (198, 0, 0), (194, 0, 0), (189, 0, 0), (185, 0, 0), (180, 0, 0), (175, 0, 0), (171, 0, 0), (166, 0, 0), (162, 0, 0), (157, 0, 0), (152, 0, 0), (148, 0, 0), (144, 0, 0), (139, 0, 0), (134, 0, 0), (130, 0, 0), (134, 0, 0), (130, 0, 0)]

#for i in range(50):
#	r,g,b=colormap_blue[i]
#	r=r*(i+50)/100.0
#	g=g*(i+50)/100.0
#	b=b*(i+50)/100.0
#	colormap_blue[i]=(r,g,b)

# DEFAULT CONFIG - VALUES ARE ONLY A STARTING POINT TO GET THINGS ROLLING
# THIS THING GETS BIG FAST!

config={
	# YOU CAN CHANGE THESE ###################
	"power":13,			#! 2^x for buffersize, adjust for vertical FFT res (I like 13)
	"sampleRate":5500,	#! increases max frequency (if buf4rate=False)
						#    reduce if your pc cant keep up
	"buf4rate":False, 	#! recommended True to force rate=bufSize
	"overlap":4,		#! higher makes graph faster/smoother (keep small powers of 2!)
	"gain":7,			#! I don't want to explain. I like 7, but screw with it.
	"gainType":"auto",#! set to False to use the maxGain
	"manGain":1700,		#! to prevent ANY intensity modification but allow cutoff
	"width":500,		#! Width of the spectrograph window
	"upsideDown":True,	#! True = freq increases from bottom to top
	"dropData":True,	#! Drop data if falling behind
	"saveImgs":True,	#! Automatically save
	"imgType":"BMP",	#! capture format
	"prefix":"capt_",	#! filename prefix
	"timestamp":True,	#! add timestamp to image file name?
	"resize":False,		#! resize output?
	"resizeX":20,		#! resize width
	"resizeY":800,		#! resize height
	"pause":True,		#! holds the recorder still
	"RFT":False,		#! use real FT? bad idea!
	"printLog":False,	#! print devel info to console
	"logAll":False,		#! good for debugging but slower
	"bandpass":True,	#! limit calcs between a ragen
	"bandlow":500,		#!	^^^ low in Hz
	"bandhigh":900,		#!  ^^^ high in Hz
	"offset":10140000,	#!  Displayed Hz = Hz + offset
	"smoothing":0,		#! if enabled it uses time-domain averaging
	"soundcard":0,		#! soundcard ID (usually low integers)
	
	# THESE ARE AUTOMATICALLY UPDATED ########
	"version":version, 	# version, obviously
	"bufSize":None, 	# number of audio samples per calculation
						#    changes speed and resolution
	"fftxs":None,		# frequency units
	"maxFreq":None,		# maximum frequency current settings are capable of
	"vertSize":None,	# vertical size of graph in pixles (assume max Freq)
	"vertRes":None,		# vertical resolution in Hz/pixel
	"horizRes":None,	# horizontal resolution in seconds/pixel
	"horizTime":None,	# horizontal timespan in seconds
	"dieNOW":False,		# set this to True to kill recorder thread
	"updateNow":False,	# set to true if window needs to be redrawn
	"colormap":"greens",# to set colormap remotely
	"exit":False,		# set to True to prevent restart, but lead to a quit
	"imgSuffix":".bmp",	# to append to the image captures
	"ilow":None,		# fftx[i] of upper limit
	"ihigh":None,		# fftx[i] of upper limit
	"lowFreq":None,
	"highFreq":None,
	"fldr":"./output/",
	"absmax":None		# absolute maximum bandpass frequency
	
	
	
	}

	
logdata=[]
logstat=[]
def log(junk,stats=False):
	global logdata
	addwhat="[%.02f] %s"%(time.clock(),str(junk))
	if stats==True:
		logstat.append(addwhat)
		if len(logstat)>5:
			logstat.pop(0)
	else:
		logdata.append(addwhat)
		if len(logdata)>5:
			logdata.pop(0)
	if config["printLog"]==True:
		print addwhat
	return

def readlog(stats=False):
	logtxt=""
	global logdata
	if stats==True:
		for i in range(len(logstat)):
			logtxt=logtxt+logstat[i]+"\n"
		logtxt+="NUMBER OF IMAGE CAPTURES:\t%d\n"%savedCaptures
		logtxt+="TIMESTAMP OF LAST CAPTURE:\t%d\n"%lastCaptureTime
		secSinceLast=int(time.time()-lastCaptureTime)
		timeleft=config["horizTime"]-secSinceLast
		minLeft=int(timeleft/60)
		secLeft=int(timeleft-minLeft*60)
		logtxt+="TIME UNTIL NEXT CAPTURE:\t%02d:%02d\n"%(minLeft,secLeft)
		logtxt+="CAPTURES PER HOUR:\t%.02f\n"%((60*60)/config["horizTime"])
		logtxt+="CAPTURES PER DAY:\t%.02f\n"%((24*60*60)/config["horizTime"])
		logtxt+="\n--- BEFORE NORMALIZATION ---\n"
		logtxt+="min:\t"+str(before_min)+"\n"
		logtxt+="max:\t"+str(before_max)+"\n"
		logtxt+="avg:\t"+str(before_average)+"\n"
		logtxt+="\n--- AFTER NORMALIZATION ---\n"
		logtxt+="min:\t"+str(after_min)+"\n"
		logtxt+="max:\t"+str(after_max)+"\n"
		logtxt+="avg:\t"+str(after_average)+"\n"
	else:
		for i in range(len(logdata)):
			logtxt=logtxt+logdata[i]+"\n"
	return logtxt
	
def config_show(loud=False):
	"""display all values from config in the console."""
	logOneLine="\n\n\n##### CONFIGURATION VALUES #####\n"
	for key in config.keys():
		snippit=str(config[key])
		if len(snippit)>7:
			#snippit="TOO BIG TO SHOW"
			snippit=snippit[:6]+"..."
		line="%s=%s"%(key,snippit)
		if loud: 
			print line
		logOneLine+=line+"\t"
	log(logOneLine+"\n\n\n")
			
def recalculateEverything():	
	"""update all values in config."""
	global config
	log("RECALCULATING CONFIGURATION")
	d = os.path.dirname(config["fldr"])
	if not os.path.exists(d):
		log("I don't see "+str(d)+" so I'll make it")
		os.makedirs(d)
	config["bufSize"]=2**config["power"]
	if config["buf4rate"]:
		config["sampleRate"]=config["bufSize"]/2
	if config["RFT"]==True:
		config["fftxs"]=scipy.fftpack.rfftfreq(config["bufSize"]*2, 1.0/(config["sampleRate"]/2))
	else:
		config["fftxs"]=scipy.fftpack.fftfreq(config["bufSize"]*2, 1.0/(config["sampleRate"]))
		config["fftxs"]=config["fftxs"][:len(config["fftxs"])/2]
	config["absmax"]=config["fftxs"][-1]
	config["ilow"]=0
	config["ihigh"]=len(config["fftxs"]-1)
	if config["bandpass"]==True:
		if config["bandlow"]<0: 
			config["bandlow"]=0
		if config["bandhigh"]>config["fftxs"][-1]: 
			config["bandlow"]=config["fftxs"][-1]
		for i in range(len(config["fftxs"])):
			if config["fftxs"][i]<config["bandlow"]:
				config["ilow"]=i
			i=len(config["fftxs"])-1-i
			if config["fftxs"][i]>config["bandhigh"]:
				config["ihigh"]=i
	
	#print "BANDPASS FILTERS:"
	#print config["ilow"],config["fftxs"][config["ilow"]]
	#print config["ihigh"],config["fftxs"][config["ihigh"]]
	config["fftxs"]=config["fftxs"][config["ilow"]:config["ihigh"]]
	config["lowFreq"]=config["fftxs"][1]
	config["highFreq"]=config["fftxs"][-1]
	
	#raw_input("WAITING")
	config["vertSize"]=(len(config["fftxs"]))
	#if config["RFT"]==True: 
	config["vertRes"]=(config["highFreq"]-config["lowFreq"])/float(config["vertSize"])
	config["horizRes"]=config["bufSize"]/float(config["sampleRate"])/config["overlap"]
	config["horizTime"]=config["horizRes"]*config["width"]
	global fftmins,fftmaxs
	fftmins,fftmaxs=[],[]
	global colormap
	if config["colormap"]=="blues": colormap=colormap_blue
	elif config["colormap"]=="greens": colormap=colormap_green
	elif config["colormap"]=="logo": colormap=colormap_logo
	config_show()

	#raw_input("WAITING")
	
recalculateEverything()

# INITIALIZE TEMPORARY RUNTIME VARIABLES #
chunks=[] #segments of audio stored in memory, should be ~3
currentRow=0 #how many pixles have been processed so far
fftmins,fftmaxs=[],[]
	
def config_load(fname="qrss_vd.cfg"):
	"""load config settings from file."""
	global config
	fname=config["fldr"]+fname
	log("loading config file %s"%(fname))
	if os.path.exists(fname)==False:
		config_save()
	f=open(fname)
	raw=f.read()
	raw=raw.replace("\n","")
	raw=raw.replace("\t","")
	f.close()
	try:
		ctest=eval(raw)
		if not ctest["version"]==config["version"]:
			msg="You are running QRSS VD version "+config["version"]+"\n"
			msg+="Your default config file is for version "+config["version"]+"\n\n"
			msg+="If load it, right-click and select 'set as default' immediately after!\n"
			msg+="Do you want to load it anyway? "
			if tkMessageBox.askokcancel("Load old config?", msg)==False: return
		gui_shutdown()
		for key in ctest.keys():
			config[key]=ctest[key]
		recalculateEverything()
	except:
		#tkMessageBox.showinfo("RESET","The program needs to be restarted to restore factory defaults")
		config_save()
	return

def config_save(fname="qrss_vd.cfg"):
	"""save config settings to file."""
	#print "SAVING"
	fname=config["fldr"]+fname
	msg="saving config file (%d values) to %s"%(len(config),fname)
	log(msg)
	f=open(fname,'w')
	config["fftxs"]=None
	out=""
	out+=str(config)
	out=out.replace(",",",\n\t")
	f.write(out)
	f.close()
	return

def config_get(key):
	"""retrieve a value from the config variable."""
	global config
	return config[key]

def recorder_shutdown():
	global config
	config["dieNOW"]=True
	while len(threading.enumerate())>1:
		time.sleep(.1)
	return
	
def recorder_pause():
	config_set("pause",True)
	return
	
def recorder_resume():
	config_set("pause",False)
	return
	
def recorder_startup():
	global t_rec, config
	config["dieNOW"]=False
	t_rec=threading.Thread(target=record) 
	t_rec.daemon=True # daemon mode forces thread to quit with program
	t_rec.start()
	return

def gui_shutdown(killProg=False):
	global config
	recorder_shutdown()
	if killProg==True: 
		config["exit"]=True
	
def config_set(key,value):
	"""set a value in the config variable set."""
	global config
	log("setting "+str(key)+" to "+str(value))
	requireResets=["power","RFT","offset"]
	if key in requireResets:
		#print "SHUTTING DOWN"
		#recorder_shutdown()
		gui_shutdown()
		config[key]=value
		#recorder_startup()
	elif key == "soundcard":
		recorder_shutdown()
		config[key]=value
		recorder_startup()
		
	else:
		config[key]=value
	recalculateEverything()
	return

def getSoundCards():
	p = pyaudio.PyAudio() 
	msg="These are the sound cards I found:\n\n"
	cards=[]
	for i in range(p.get_default_host_api_info()["deviceCount"]):
		if p.get_device_info_by_index(i)["maxInputChannels"]>0:
			cardName = p.get_device_info_by_index(i)["name"]
			cardIndex = p.get_device_info_by_index(i)["index"]
			cards.append(cardIndex)
			msg+="[%d] %s\n"%(cardIndex,cardName)
	p.terminate()
	msg+="\nEnter the number of the card to use:"
	ans=tkSimpleDialog.askinteger("Select Sound Card", msg, initialvalue=cards[0])
	if not ans==None: 
		config_set("soundcard",ans)
	return #ans
	
def record(returnPcm=False):
	"""continuously record from the sound card."""
	"""This should be run as a thread, and it will continuously
	poll the sound card and tell the rest of the script to update
	the imagry when it's ready. If image/fft calculations get slow,
	the recording doesn't stop! This is good and bad. Good b/c you don't
	lose a second of audio, but bad because the farther it gets behind
	the harder it is to catch up."""
	global config
	global chunks
	print "USING SOUNDCARD:",config["soundcard"]
	p = pyaudio.PyAudio() 
	qual=pyaudio.paInt16 #this matches the fromstring() below, increase if ur crazy
	inStream = p.open(format=qual,channels=1,rate=config["sampleRate"],\
						input=True,frames_per_buffer=config["bufSize"],\
						input_device_index=config["soundcard"])
	while config["dieNOW"]==False:
		while config["pause"]==True:
			if config["dieNOW"]==True:
				return
			time.sleep(.1)
			#I've got a good idea! Let's actch up!
			if len(chunks)>3:config["updateNow"]=True
			else:config["updateNow"]=False
		wavdata=inStream.read(config["bufSize"])
		pcm=scipy.fromstring(wavdata, 'Int16')
		#DOWNSAMPLE HERE?
		if returnPcm==True:
			return pcm
		chunks.append(pcm)
		config["updateNow"]=True
		#slp=float(config["bufSize"])/config["sampleRate"]
		#print "SLEEPING",slp
		#time.sleep(slp+.3)#FOR SLOW PC

def graphSoundClip(): #FOR PCM DEBUGGING ONLY!
	import pylab
	vals=record(True,False)
	pylab.plot(vals)
	pylab.show()
	quit()
#graphSoundClip()

def commaize( valstr ) :
	ilist = list( valstr )
	ilist.reverse()
	olist = []
	for i in range( len( ilist )) :
		if i % 3 == 0 and i > 2 :
			olist.append( "," )
		olist.append( ilist[i] )
	olist.reverse()
	return string.join(olist, "")

def textIntro():
	"""cool ascii logo."""
	daText="66964111111884111111166741111118864111111978899784116677411941111111957784112266113611226711641122661194112266117998893711977361137112286115663711790911371188071139116702243811660224779867391199636113711980811576361197391138111111143681111118397111111768886836911949114381166391158939118836113611229611602222891190222297116787677098119114836117939115663911411911381186091164118707116411770711869887990891114663911993911598388111111438116836113871111114399111111476867998807814766391111111456960222261113224973224902222224670222222479868977666024879632222222485668976880224"
	daText=daText.replace("0","\\")
	daText=daText.replace("1","#")
	daText=daText.replace("2","_")
	daText=daText.replace("3","|")
	daText=daText.replace("4","/")
	daText=daText.replace("5","\n")			
	daText=daText.replace("6","8")			
	daText=daText.replace("7","8")			
	daText=daText.replace("8","9")			
	daText=daText.replace("9"," ")			
	print "\n"*20+daText+"by Scott Harden, AJ4VD"," "*19,"version",
	print str(config["version"])
	print "\n"*5
	
def downSample(fftx,ffty,degree=10): #USED FOR TESTING OF GRAPHING AND DEBUGGING
	"""Use averaging to make a list of x points x/degree points."""
	x,y=[],[]
	for i in range(len(ffty)/degree-1):
			x.append(fftx[i*degree+degree/2])
			y.append(sum(ffty[i*degree:(i+1)*degree])/degree)
	return [x,y]

def smoothWindow(fftx,ffty,degree=10): #USED FOR TESTING OF GRAPHING AND DEBUGGING
	"""moving window averager."""
	lx,ly=fftx[degree:-degree],[]
	for i in range(degree,len(ffty)-degree):
			ly.append(sum(ffty[i-degree:i+degree]))
	return [lx,ly]

def detrend(ffty,degree=10): #USED FOR TESTING OF GRAPHING AND DEBUGGING
	"""subtracts the moving window average from the list."""
	i=0
	m=len(ffty)
	list=scipy.zeros(m)
	while i<len(list):
		if i<=degree:
			list[i]=ffty[degree]
		elif i>=m-degree:
			list[i]=ffty[-degree]
		else:
			list[i]=ffty[i]-scipy.average(ffty[i-degree:i+degree])/2
		i+=1
	return list

def reduceHalf(ffty):
	new=[]
	for i in range(len(ffty)/2):
		new.append(scipy.average(ffty[2*i:2*(i+1)]))
	return scipy.array(new)
	
def smooth(ffty,degree=5): #USED FOR TESTING OF GRAPHING AND DEBUGGING
	"""subtracts the moving window average from the list."""
	i=0
	m=len(ffty)
	list=scipy.zeros(m)
	while i<len(list):
		if i<=degree:
			list[i]=ffty[degree]
		elif i>=m-degree:
			list[i]=ffty[-degree]
		else:
			list[i]=scipy.average(ffty[i-degree:i+degree])/2
		i+=1
	return list

lastffty=[]
def constPhase(ffty,degree=10): #USED FOR TESTING OF GRAPHING AND DEBUGGING
	"""subtracts the moving window average from the list."""
	global lastffty
	if len(lastffty)==0:
		lastffty=ffty
		return ffty*0
	else:
		newffty=ffty
		for i in range(len(newffty)):
			if newffty[i]<0:newffty[i]=0
		lastffty=ffty
		return newffty
	
def triangleShape(list):
	"""change the volume of a wav to make a triangle."""
	"""I like to do this in conjunction with overlap to emphasize the
	current data points while also including surrounding points.
	I wonder if a Gaussian (or similar) curve would be better?"""
	t = scipy.arange((len(list)+1)/2)
	t = scipy.append(t,t[::-1])
	if len(t)>len(list):
		t = scipy.delete(t,len(list)/2)
	return (list*t)/float(max(t))

mFFT=scipy.array([])
def memoryFFT(fft,times=5):
	if times==0: return fft
	global mFFT
	if len(mFFT)==0 or len(mFFT[0])<>len(fft):
		mFFT=scipy.array([fft]) #start a new memory array
	else:
		mFFT=scipy.vstack((mFFT,fft)) #build it up first
	while len(mFFT)>times:
		mFFT=mFFT[1:]
	if len(mFFT)==times:
		fft=mFFT.mean(0)
	return fft

before_min,before_max,before_average=0,0,0	
def normalize(ffty): #COULD USE TECHNIQUE WORK TO IMPROVE WEAKSIGNALS!!!!
	"""Eats crazy large values and poops-out values 0 to 255."""
	"""This represents an area which could use GUI improvement.
	This function does everything to the FFT from the moment its created
	until it's given 8-bit pixel values. By adjusting how this works
	you can either hide accentuate weak signals. experiment!!!"""
	global before_min,before_max,before_average	
	#print "max ffty before:",ffty.max()
	#if True:
	ffty=memoryFFT(ffty,config["smoothing"])
	#print "max ffty after:",ffty.max()
	#ffty=detrend(ffty)
	#ffty=smooth(ffty)
	#ffty=constPhase(ffty)
	
	global fftmins,fftmaxs
	#fft=scipy.log(ffty+10)#log magnifies small peaks (weak signals)
	fftmin=ffty.min()
	fftmin=0
	
	if currentRow%25==0:
		before_min=fftmin
		before_max=max(ffty)
		before_average=scipy.average(ffty)
	
	if config["logAll"]==True:
		log("---BERORE NORMALIZATION---")
		log("min: "+str(fftmin))
		log("max: "+str(max(ffty)))
		log("average: "+str(scipy.average(ffty)))
		#log("mean: "+str(scipy.mean(ffty)))
	if config["gainType"]=="auto":
		fftmax=scipy.median(ffty) #this is a brain twist. it works much better!!
		fftmax=(fftmax-fftmin)*config["gain"]+fftmin #INCREASE THIS NUMBER TO DECREASE GAIN
		ffty=255.0*(ffty-fftmin)/(fftmax-fftmin)
		return ffty
		#fftmins.append(fftmin)
		#fftmaxs.append(fftmax)
		#fftmin=scipy.average(fftmins) # add the current max/min to the rest
		#fftmax=scipy.average(fftmaxs)
		#while len(fftmins)>50:
		#	 fftmins.pop(0) # delete theoldest max/min from the rest
		#	 fftmaxs.pop(0)
	if config["gainType"]=="simple":
		fftmax=ffty.max()
		ffty=255.0*(ffty-fftmin)/(fftmax-fftmin)
		return ffty
	if config["gainType"]=="manual":
		fftmax=config["manGain"]
		ffty=255.0*(ffty-fftmin)/(fftmax-fftmin)
		return ffty


def graph():
	"""Combine 3 recordings and do a moving window FFT with overlap."""
	global chunks
	if len(chunks)<3:return #we need 3 chunks before we can begin
	soundsize=len(chunks[0]) #we'll do a FFT on twice the length of a chunk
	# ^^^ this also causes are vertical FFT resolution to double (score!)
	sound=scipy.concatenate((chunks[0],chunks[1],chunks[2])) #make a 3-chunk sound
	for i in range(config["overlap"]): #moving window FFT using int(overlap) windows
		start=soundsize*i/config["overlap"] #subselection size
		workwith = sound[start:start+soundsize*2] # create subselection
		workwith = triangleShape(workwith) #shape the audio (silence edges)
		doTheWork(workwith) #update chunks[] with FFT data from this selection
		# ^^^ note that doTheWork() leads to the image being updated, perhaps we 
		#     want to only update the image after all the work has been done?
	chunks.pop(0) #remove oldest chunk

	if len(chunks)>20:
		log("falling behind... "+str(len(chunks)))
		if config["dropData"]==True:		
			pass
			#print "I SHOULD KNOW WHAT TO DO I BUT I DONT"	
		if len(chunks)>500:
			print "I JUST AM NOT KEEPING UP!"
			print "YOU'RE BEHIND:",len(chunks)
		#I don't know what to do about this if it happens
		#reduce config["power"] or CPU load or something

savedCaptures=0
lastCaptureTime=time.time()
def captureNow(im):
	global savedCaptures,lastCaptureTime
	savedCaptures+=1
	lastCaptureTime=time.time()
	config_set("saveNow",False)
	fname=config["fldr"]+config["prefix"]
	if config["timestamp"]==True:
		fname=fname+str(time.time())
	fname=fname+config["imgSuffix"]
	if config["resize"]==True:
		im=im.resize((config["resizeX"],config["resizeY"]),Image.ANTIALIAS)
	#print "SAVING IMAGE:",fname
	log("SAVING IMAGE: "+fname)
	im.save(fname,config["imgType"])
	f=open(config["fldr"]+"scale_info.txt",'w')
	s=[config["vertRes"],config["lowFreq"],config["horizRes"],config["offset"]]
	#print "STRING:",str(s)
	f.write(str(s))
	f.close()

after_min,after_max,after_average=0,0,0	
def doTheWork(data):
	"""read WAV data, FFT, filter, update spectrograph, maybe save."""
	global config
	global after_min,after_max,after_average
	if config["RFT"]==True:
		ffty=scipy.fftpack.rfft(data) #convert WAV to FFT
		ffty=abs(ffty[0:len(ffty)/2])/1000
	else:
		ffty=scipy.fftpack.fft(data) #convert WAV to FFT
		#ffty=ffty.real #.real or .imag for phase separation
		ffty=abs(ffty[0:len(ffty)/2])/1000 #FFT is mirror-imaged, grab half	
		#ffty1=ffty[:len(ffty)/2] #FFT is mirrorish still, split in 2
		#ffty2=ffty[len(ffty)/2::]
		#ffty2=ffty2[::-1] #reverse the second split
		#ffty=ffty1+ffty2 #combine them (average)
		
	#print "FFTY:",len(ffty),ffty[0:4]
	ffty=ffty[config["ilow"]:config["ihigh"]]
	
	if config["upsideDown"]==True:
		ffty=ffty[::-1]
		
	#print "FFT SIZE 1:",len(ffty)
	ffty=normalize(ffty) #convert crazy-large values to 0-255
	#print "FFT SIZE 2:",len(ffty)
	
	if currentRow%25==0:
		after_min=min(ffty)
		after_max=max(ffty)
		after_average=scipy.average(ffty)
	
	if config["logAll"]==True:
		log("---AFTER NORMALIZATION---")
		log("min: "+str(min(ffty)))
		log("max: "+str(max(ffty)))
		log("average: "+str(scipy.average(ffty)))
	updatePic(ffty) #load new pixel data onto spectrograph
	config["updateNow"]=True
	return
			
def updatePic(data):
	"""take fft data, make it a row of pixles, and add it to the image."""
	global im
	global currentRow
	strip=Image.new("L",(1,config["vertSize"]))
	#print "FFT SIZE 3:",config["vertSize"]
	if len(data)>config["vertSize"]: #maybe do this differently for bandpassing
		 data=data[:config["vertSize"]-1]
	strip.putdata(data)
	strip=colorize(strip)
	im=ImageChops.offset(im,-1,0) #WHY DID I HAVE
	im.paste(strip,(config["width"]-1,0)) #THESE REVERSED???
	currentRow+=1
	if currentRow==config["width"] and config["saveImgs"]==True:
		#LETS SAVE THIS THING
		captureNow(im)
		currentRow=0

def setThisImage(imt):
	"""use this only when you want to set the global image manally."""
	global im
	im=imt


def drawVertScale():
	"""draws a scale given height and vertRes in hz/pixel."""
	#ONLY KNOWS UPSIDE DOWN RIGHT NOW
	height=config["vertSize"]
	vertres=config["vertRes"]
	freqLow=config["lowFreq"]
	freqHigh=vertres*height+freqLow
	im=Image.new("L",(100,height),255)
	draw = ImageDraw.Draw(im)
	freq=freqLow #config["lowFreq"])
	txtwidth=0

	if vertres>2:
		tickevery=10
		labelEvery=100
	elif vertres>.5:
		tickevery=5
		labelEvery=25
	else:
		tickevery=1
		labelEvery=10

	freqs=scipy.arange(freqLow,freqHigh,vertres)
	lasthz=int(freqLow+height*vertres)/tickevery
	lastlab=int(freqLow+height*vertres)/labelEvery

	for y in range(height):
		freq=freqs[-(y+1)]
		if int(freq)/tickevery <> lasthz:
			draw.line([(0, y),(5, y)],150)
			lasthz=int(freq)/tickevery
		if int(freq)/labelEvery <> lastlab:
			draw.line([(0, y),(10, y)],0)
			lab=commaize(str(int(config["offset"]+labelEvery+int(freq)/labelEvery*labelEvery)))+" Hz"
			labwidth,labheight=draw.textsize(lab)
			if labwidth>txtwidth:
				txtwidth=labwidth
			draw.text((12, y-labheight/2),lab)
			lastlab=int(freq)/labelEvery
	im=im.crop((0,0,12+txtwidth+2,height))
	del draw
	#im.save("scale_vert.bmp","BMP")	
	return im

def drawHorizScale(width,horizres):
	"""returns a horizontal scale given width and resolution."""
	im=Image.new("L",(width,100),255)
	draw = ImageDraw.Draw(im)
	maxsec=int(width*horizres)
	for sec in range(maxsec):
		x=int(float(sec)/horizres)
		if horizres<.3:
			draw.line([(width-x, 0),(width-x, 5)],200)
		if sec%10==0:
			if horizres<.3:
				draw.line([(width-x, 0),(width-x, 10)],0)
				lab=str(int(sec/10)*10)+"s"
				labw=draw.textsize(lab)[0]
				if sec>0:
					draw.text((width-x-labw/2, 12),lab)
			else:
				draw.line([(width-x, 0),(width-x, 10)],200)
		if sec%60==0:
			if horizres>.3:
				draw.line([(width-x, 0),(width-x, 10)],0)
				lab=str(int(sec/60))+"m"
				labw=draw.textsize(lab)[0]
				if sec>0:
					draw.text((width-x-labw/2, 12),lab)
	txtheight=draw.textsize(lab)[1]
	im=im.crop((0,0,width,12+txtheight+2))
	del draw
	#im.save("scale_horiz.bmp","BMP")
	return im

	
def cornerLogo(width,height):
	imq=ImageOps.invert(genLogo(1,0))
	x,y=imq.size
	im=Image.new("L",(width,height),255)
	im.paste(imq,(width/2-x/2,height/2-y/2))
	#im.save("scale_corner.bmp","BMP")
	return im
	
def genLogo(scaleby=15,rotate=40):
	"""create QRSS VD text as an image."""
	if rotate>0: rotate+=random.randint(0,50)
	b="1111011110111101111000100101110210010100101000010000001001010012"
	b+="1001011110111101111000100101001210110101000001000010001010010012"
	b+="1111010110111101111000010001110"
	b=b.split("2")
	im=Image.new("L",(33,7))
	data=im.load()
	for y in range(len(b)):
		for x in range(len(b[y])):
			data[x+1,y+1]=int(b[y][x])*255
	im=im.resize((im.size[0]*scaleby,im.size[1]*scaleby))
	data=im.load()
	def drawSin(width,height,vertoffset,horizoffset,thickness,darkness):
		for x in range(im.size[0]):
			y=scipy.sin((x-horizoffset)/float(width))*height+vertoffset
			for i in range(thickness):
				if 0<=y+i<im.size[1] and 0<=x<im.size[0]:
					data[x,y+i]=data[x,y+i]+darkness
	if rotate>0:
		canv=Image.new("L",(1000,1000))
		canv.paste(im,(400,450))
		im=canv.rotate(rotate)
		im=im.crop(im.getbbox())
	return im
	
def sinit(width,height):
	"""draw sine waves on top of an image."""
	im=Image.new("L",(width,height))
	draw = ImageDraw.Draw(im)
	for sinNum in range(10):
		sinwidth=random.randint(5,100)
		sinheight=sinwidth*(random.random()+.1)
		horizoffset=random.randint(1,width)
		vertoffset=250+random.randint(-150,150)
		thickness=None
		darkness=random.randint(10,200)
		lastx,lasty=None,None
		for x in range(1,width):
			y=scipy.sin((x-horizoffset)/float(sinwidth))*sinheight+vertoffset
			if 1<=y<height and 1<=x<=width:
				if not lastx==None:
					draw.line((lastx,lasty,x,y),fill=darkness)
					draw.line((lastx,lasty+1,x,y+1),fill=darkness)
					draw.line((lastx,lasty+2,x,y+2),fill=darkness)
				lastx,lasty=x,y
	for i in range(5):
		im=im.filter(ImageFilter.SMOOTH_MORE)
	del draw
	return im

def delete_file(fname="qrss_vd.cfg"):
	if tkMessageBox.askyesno("DELETE",\
		"I've been told to delete:\n%s\n\nIs this what you want to do?"%fname):
		os.remove(config["fldr"]+fname)
		tkMessageBox.showinfo("PLEASE CLOSE PROGRAM","The program needs to be restarted to restore factory defaults")

def launchFldr1():
	fldr=os.getcwd()
	#os.system('explorer '+fldr)
	os.startfile(fldr)
	
def launchFldr2():
	fldr=os.getcwd()+config["fldr"]#.replace('.','').replace('/','\\')
	#os.system('explorer '+fldr)
	os.startfile(fldr)

		
def colorize(im):
	"""go from 8-bit grayscale to colormapped RGB image."""
	global colormap
	def red(val):
		return colormap[val][0]
	def green(val):
		return colormap[val][1]
	def blue(val):
		return colormap[val][2]
	r=Image.eval(im,red)
	g=Image.eval(im,green)
	b=Image.eval(im,blue)
	im=Image.merge("RGB",(r,g,b))
	return im
	
def credits():
	master = Tk()
	master.title("QRSS VD - Credits")
	master.config(padx=5, pady=5)
	author = LabelFrame(master, text="Author", padx=5, pady=5)
	author.grid(row=1,column=1,sticky=E+W)
	msg="QRSS VD version "+str(version)
	msg+="""
QRSS VD was written by
Scott Harden, AJ4VD
wesite: www.SWHarden.com
email: SWHarden@gmail.com"""
	Label(author,text=msg, wraplength=150,justify=CENTER, anchor=E).grid(row=1,column=1,sticky=E+W)
	Button(master,text="[SITE]",relief=FLAT,command=lambda: webbrowser.open("http://www.SWHarden.com")).grid(row=1,column=2,sticky=N+S+E+W)
	Button(master,text="[SITE]",relief=FLAT,command=lambda: webbrowser.open("http://www.GatorRadio.org")).grid(row=2,column=2,sticky=N+S+E+W)
	affiliation = LabelFrame(master, text="Affiliation", padx=5, pady=5)
	affiliation.grid(row=2,column=1)
	msg="I'm a member of GARC, the University of Florida Gator Amateur Radio Club! QRSS VD was "
	msg+="written specifically to be run as a QRSS grabber at the W4DFU club station in "
	msg+="Gainesville, Florida.\n\nhttp://www.GatorRadio.org"
	Label(affiliation,text=msg, wraplength=150,justify=LEFT).grid(row=1,column=1)
	thanks = LabelFrame(master, text="Special Thanks", padx=5, pady=5)
	thanks.grid(row=3,column=1,sticky=E+W,columnspan=2)
	msg="""SOFTWARE TESTING:
Kyle Walker
    kyleswalker.wordpress.com
Fred Eckert
    kj4lfj.dyndns.org

HARDWARE:
Dr. Jay Garlitz
University of FL Amateur Radio Club"""
	Label(thanks,text=msg, wraplength=150,justify=LEFT).grid(row=1,column=1)
	mainloop()

	
def genSplash(width,height):
	"""create the splash image."""
	global colormap
	imLogo=genLogo()
	imLogo=ImageOps.expand(imLogo, border=50, fill=0)
	for i in range(5):
		imLogo=imLogo.filter(ImageFilter.SMOOTH_MORE)
	lw,lh=imLogo.size
	im2=Image.new("L",(width,height))
	im2=ImageOps.expand(im2, border=20, fill=0)
	draw = ImageDraw.Draw(im2)
	#MAKE SOME STATIC
	#for x in range(width/2+10):
	#	for y in range(height/2+10):
	#		v=random.randint(0,30)
	#		draw.rectangle((x*2,y*2,x*2+1,y*2+1),fill=v)
	del draw
	for i in range(10):
		im2=im2.filter(ImageFilter.SMOOTH_MORE)
	imSin=sinit(im2.size[0],im2.size[1])
	im2.paste(255, (0,0), imSin)
	im2.paste(255, (width-lw-40,0), imLogo)
	#im2=im2.crop((10,10,width,height))
	txt=Image.new("L",(1000,500))
	draw=ImageDraw.Draw(txt)
	darkness=100
	draw.text((10, 10),"QRSS VD version %s"%config["version"],fill=darkness)
	draw.text((10,20),"by Scott Harden, A J 4 V D",fill=darkness)
	#draw.text((10,30),"www.SWHarden.com",fill=darkness)
	del draw
	x1,y1,x2,y2 = txt.getbbox()
	txt=txt.crop((x1-3,y1-3,x2+3,y2+3))
	scaleby=2
	txt=txt.resize((txt.size[0]*scaleby,txt.size[1]*scaleby),Image.BICUBIC)
	im2.paste(255, (50,0), txt)
	tmp=colormap
	colormap=colormap_logo
	im2=colorize(im2)
	colormap=tmp #set it back to the default
	return im2

class frame_spectrograph(Frame):
	"""the GUI = scary, messy code."""
	

	
	
	global config,openwindows
				
	def quitIt(self,event=None):
		"""quit the entire program."""
		if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
			self.master.quit()
		else:
			print "attempt to quit thwarted"

	def window_stats(self,event=None):
		"""window for stats."""		
		def kill():
			wCon.destroy()
		def updateBox():
				StatsLabelData.config(text=readlog(True))
				StatsLabelData.after(1000,updateBox)
		wCon=Toplevel()
		wCon.protocol("WM_DELETE_WINDOW", kill)
		wCon.title("QRSS VD - STATISTICS")
		frameStats=Frame(wCon, bg="#003366")
		frameStats.grid(row=1,column=1,sticky=W)
		conjunk=StringVar()
		StatsLabelTop=Label(frameStats,text="##### STATISTICS #####",\
			fg="yellow",bg="#003366").grid(row=1,column=1)
		StatsLabelData=Label(frameStats,text="loading...",\
			fg="white",bg="#003366",justify=LEFT,\
			wraplength=500)
		StatsLabelData.grid(row=2,column=1,sticky=N+S+E+W)
		#threading.Thread(target=updateBox, args=conjunk).start()
		StatsLabelData.after(1000,updateBox)
		
	def window_console(self,event=None):
		"""window for developer console."""		
		def kill():
			wCon.destroy()
		
		def updateBox():
				StatsLabelData.config(text=readlog())
				StatsLabelData.after(100,updateBox)
		
		wCon=Toplevel()
		wCon.protocol("WM_DELETE_WINDOW", kill)
		wCon.title("QRSS VD - CONSOLE")
		frameStats=Frame(wCon, bg="black")
		frameStats.grid(row=1,column=1,sticky=W)
		conjunk=StringVar()
		StatsLabelTop=Label(frameStats,text="##### DEVELOPERS CONSOLE #####",\
			fg="white",bg="black").grid(row=1,column=1)
		StatsLabelData=Label(frameStats,text="you think you're cool?",\
			fg="green",bg="black",justify=LEFT,\
			wraplength=500)
		StatsLabelData.grid(row=2,column=1,sticky=N+S+E+W)
		#threading.Thread(target=updateBox, args=conjunk).start()
		StatsLabelData.after(1000,updateBox)


			
		
	def window_settings(self,event=None):
		"""window for general settings."""
		
		
		def kill():
		
			wLog.destroy()
		wLog=Toplevel(padx=5,pady=5)
		wLog.protocol("WM_DELETE_WINDOW", kill)
		wLog.title("QRSS VD - Settings")

		# FRAME: RATES
		fRates=Frame(wLog,padx=5,pady=5,bd=2,relief=GROOVE)
		fRates.grid(row=1,column=1, sticky=N+S+E+W)
		Label(fRates,text="Bitrate = 2^x (10-15): ",justify=RIGHT).grid(row=0,column=1,sticky=E)
		#Label(fRates,text="Buffer Size (2^X): ",justify=RIGHT).grid(row=1,column=1,sticky=E)
		#Label(fRates,text="Bitrate (Hz): ",justify=RIGHT).grid(row=2,column=1,sticky=E)
		ePower=Entry(fRates);ePower.grid(row=0,column=2);ePower.insert(0,str(config_get("power")))
		#eBS=Entry(fRates);eBS.grid(row=1,column=2);eBS.insert(0,"14")
		#eBR=Entry(fRates);eBR.grid(row=2,column=2);eBR.insert(0,"5500")	
		
		Label(fRates,text="Window width (px): ",justify=RIGHT).grid(row=1,column=1,sticky=E)
		eWid=Entry(fRates)
		eWid.grid(row=1,column=2)
		eWid.insert(0,str(config_get("width")))	
		
		Label(fRates,text="Bandpass Low: ",justify=RIGHT).grid(row=2,column=1,sticky=E)
		elow=Entry(fRates)
		elow.grid(row=2,column=2)
		elow.insert(0,str(config_get("bandlow")))	
		
		Label(fRates,text="Bandpass High: ",justify=RIGHT).grid(row=3,column=1,sticky=E)
		ehigh=Entry(fRates)
		ehigh.grid(row=3,column=2)
		ehigh.insert(0,str(config_get("bandhigh")))	
		
		#calcText=StringVar()
		#Label(fRates,text="",anchor=W,justify=LEFT,fg="#666666",\
		#	relief=SUNKEN,textvariable=calcText).grid(row=3,column=1,sticky=E+W,columnspan=2)		
		
		def calculate():
			bufSize=2**int(ePower.get())
			sampleRate=config["sampleRate"]
			#fftxs=scipy.fftpack.rfftfreq(bufSize*2, 1.0/(sampleRate/2))
			if config["RFT"]==True:
				fftxs=scipy.fftpack.rfftfreq(bufSize, 1.0/(config["sampleRate"]/2))
			else:
				fftxs=scipy.fftpack.fftfreq(bufSize*2, 1.0/(config["sampleRate"]/2))
			width=int(eWid.get())
			vertsize=len(fftxs)/4
			maxfreq=fftxs[-1]
			vertres=1.0*maxfreq/vertsize
			horizres=bufSize/float(sampleRate)
			txt="PREDICTED PROPERTIES:\n"
			txt+="vertical size (px): %d\n"%vertsize
			txt+="vertical resolution (Hz/px): %.02f\n"%vertres
			txt+="vertical resolution (px/Hz): %.02f\n"%(1.0/vertres)
			txt+="maximum frequency (Hz): %d\n"%maxfreq
			txt+="horizontal resolution (sec/px): %.02f\n"%horizres
			txt+="current window span (px): %d\n"%width
			txt+="spectrograph width (sec): %.02f\n"%(float(horizres)*width)
			txt+="spectrograph width (min): %.02f"%(float(horizres)*width/60.0)
			calcText.set(txt)
		#calculate()
		
		#Button(fRates,text="CALCULATE",command=calculate).grid(row=4,column=1)
		def applyCalcs():
			log("APPLYING CALCULATIONS")
			config_set("power",int(ePower.get()))
			config_set("width",int(eWid.get()))
			config_set("bandlow",int(elow.get()))
			bandhigh=int(ehigh.get())
			if bandhigh>config["absmax"]:
				bandhigh=config["absmax"]
			config_set("bandhigh",bandhigh)
			
			
		Button(fRates,text="APPLY VALUES",command=applyCalcs).grid(row=4,column=1,columnspan=2)

		#SPACER
		Frame(wLog,height=5).grid(row=4,column=1)
		
		# FRAME: RATEINFO ########################
		fImage=Frame(wLog,padx=5,pady=5,bd=2,relief=GROOVE)
		fImage.grid(row=5,column=1, sticky=N+S+E+W)
		
		Label(fImage,text="Colormap: ",justify=RIGHT).grid(row=1,column=1,sticky=E+W)
		colMapName = StringVar(fImage)
		colMapName.set(config["colormap"]) # default value
		OptionMenu(fImage, colMapName, "blues","greens","colors").grid(row=1,column=2,sticky=E+W)
		def set_cmap():
			if colMapName.get() =="blues": config_set("colormap","blues")
			elif colMapName.get() =="greens": config_set("colormap","greens")
			elif colMapName.get() =="colors": config_set("colormap","logo")
		Button(fImage,text="SET",command=set_cmap).grid(row=1,column=3) #COLORMAP


		def set_gaintype():
			if "Auto" in gainType.get():
				config_set("gainType","auto")
			if "Simple" in gainType.get():
				config_set("gainType","simple")
			if "Manual" in gainType.get():
				config_set("gainType","manual")
		gainType = StringVar(fImage)
		if config_get("gainType")=="auto":gainType.set("Automatic (mode*x)")
		elif config_get("gainType")=="simple":gainType.set("Simple (max max)")
		elif config_get("gainType")=="manual":gainType.set("Manual (set max)")
		OptionMenu(fImage, gainType, "Automatic (mode*x)",\
			"Simple (max max)","Manual (set max)").grid(row=2,column=2,sticky=E+W)
		Label(fImage,text="Gain Type: ",justify=RIGHT).grid(row=2,column=1,sticky=E+W)
		Button(fImage,text="SET",command=set_gaintype).grid(row=2,column=3)
		
		def set_autogain():
			config_set("gain",float(eAutoGain.get()))
		Label(fImage,text="Auto Gain: ",justify=RIGHT).grid(row=3,column=1,sticky=E+W)
		eAutoGain=Entry(fImage)
		eAutoGain.grid(row=3,column=2,sticky=E+W)
		eAutoGain.insert(0,str(config_get("gain")))
		Button(fImage,text="SET",command=set_autogain).grid(row=3,column=3)
		
		def set_mangain():
			config_set("manGain",float(eManGain.get()))
		Label(fImage,text="Manual Max: ",justify=RIGHT).grid(row=4,column=1,sticky=E+W)
		eManGain=Entry(fImage)
		eManGain.grid(row=4,column=2,sticky=E+W)
		eManGain.insert(0,str(config_get("manGain")))
		Button(fImage,text="SET",command=set_mangain).grid(row=4,column=3)
		
		#SPACER
		Frame(wLog,height=5).grid(row=6,column=1)
		
		# FRAME: FFT STUFF ########################
		fFft=Frame(wLog,padx=5,pady=5,bd=2,relief=GROOVE)
		fFft.grid(row=7,column=1, sticky=N+S+E+W)
		
		Label(fFft,text="Transformation: ",justify=RIGHT).grid(row=1,column=1,sticky=E+W)
		transType= StringVar(fFft)
		if config["RFT"]==True: transType.set("Real FFT")
		else: transType.set("Fast Fourier (best)")
		OptionMenu(fFft, transType, "Real FFT","Fast Fourier (best)").grid(row=1,column=2,sticky=E+W)
		def set_transtype():
			if transType.get() =="Real FFT": config_set("RFT",True)
			elif transType.get() =="Fast Fourier (best)": config_set("RFT",False)
		Button(fFft,text="SET",command=set_transtype).grid(row=1,column=3)
		Label(fFft,text="Time-domain smoothing: ",justify=RIGHT).grid(row=2,column=1,sticky=E+W)
		eSmth=Entry(fFft)
		eSmth.grid(row=2,column=2,sticky=E+W)
		eSmth.insert(0,str(config_get("smoothing")))
		Button(fFft,text="SET",command=lambda:config_set("smoothing",int(eSmth.get()))).grid(row=2,column=3)
		
	def window_offset(self,event=None):
                offset=tkSimpleDialog.askstring("OFFSET","""
The offset you enter will be ADDED to the existing displayed frequency.

You can enter large numbers (i.e., 10140000 for 10.14mhz) for band representation,
or small numbers (5, -1.3, -8, 1.3, etc) to fine-tune the calibration.

If you don't want an offset, you must enter 0

What offset (in Hz) do you want?""",\
initialvalue=str(config["offset"]))                
                try:
					offset=float(offset)
					config_set("offset",offset)
                except ValueError, err:	
					msg="yeah that's not a legitimate number, so I'm forgetting about this..."
					tkMessageBox.showinfo("wha...?",msg)

	def crashDoWhat(self,event=None):
		msg="""
QRSS VD was written by a 24 year old dental student, not a professional programmer.
I, Scott Harden (AJ4VD) fully intend for there to be some quirks with this program,
some of which may induce a full crash (where the program disappears completely), but
I'm confident that I can fix ALL issues, and correct ALL crashing problems in future
releaces if I have enough information about the problem.
||
If you found something that makes QRSS VD crash, please be a good pal and let me know
about it! Post a message on the QRSS VD Google Group along with a description of
the crash and the last several lines of the crash log file.
||
Crash log files end in ".exe.log" and are in the same folder as the program that crashed.
||
PS: I know sometimes QRSS VD crashes when it exists.  I'm not worried about it.  I'm
just a clumsy programmer.  Think of exiting as a controlled crash.

			Thanks and 73! --Scott, AJ4VD""".replace('\n','').replace('|','\n')
		tkMessageBox.showinfo("WHAT TO DO WHEN QRSS VD ACTS UP",msg)
		site="http://groups.google.com/group/qrss-vd"
		webbrowser.open(site)
		
	def window_autosave(self,event=None):
		"""window for autosave options."""
		
		
		def kill():
		
			wSave.destroy()
		wSave=Toplevel(padx=5,pady=5)
		wSave.protocol("WM_DELETE_WINDOW", kill)
		wSave.title("QRSS VD - AutoSave Options")

		# FRAME: RATES
		fCapt=Frame(wSave,padx=5,pady=5,bd=2,relief=GROOVE)
		fCapt.grid(row=1,column=1, sticky=N+S+E+W)
		
		def updateSample():
			t=str(time.time())
			if config_get("timestamp")==False:
				t=""
			sample=config_get("prefix")+t+config_get("imgSuffix")
			exampleFname.set(sample)
			
		def saveImCap():
			if "Auto" in eCapt.get():
				config_set("saveImgs",True)
			elif "Manual" in eCapt.get():
				config_set("saveImgs",False)
			config_set("imgType",eType.get())
			config_set("prefix",eprefix.get())
			if "BMP" in eType.get(): 
				config_set("imgSuffix",".bmp")
			if "TIFF" in eType.get(): 
				config_set("imgSuffix",".tif")
			if "JPEG" in eType.get(): 
				config_set("imgSuffix",".jpg")
			if "PNG" in eType.get(): 
				config_set("imgSuffix",".png")
			if "Enabled" in eSec.get():config_set("timestamp",True)
			else:config_set("timestamp",False)
			if "Enabled" in eRes.get():config_set("resize",True)
			else:config_set("resize",False)
			config_set("resizeX",int(eWidth.get()))
			config_set("resizeY",int(eHeight.get()))
			updateSample()
			
		Label(fCapt,text="Image capture: ",justify=RIGHT).grid(row=1,column=1,sticky=E)
		eCapt = StringVar(fCapt)
		if config_get("saveImgs"): eCapt.set("Automatic")
		else: eCapt.set("Manual")
		OptionMenu(fCapt, eCapt, "Automatic","Manual").grid(row=1,column=2,sticky=E+W)
		
		Label(fCapt,text="File type: ",justify=RIGHT).grid(row=2,column=1,sticky=E)
		eType = StringVar(fCapt)
		eType.set(config_get("imgType")) # default value
		OptionMenu(fCapt, eType, "JPEG","PNG","BMP").grid(row=2,column=2,sticky=E+W)
		
		Label(fCapt,text="Filename prefix: ",justify=RIGHT).grid(row=3,column=1,sticky=E)
		eprefix=Entry(fCapt)
		eprefix.grid(row=3,column=2,sticky=E+W)
		eprefix.insert(0,config_get("prefix"))
		
		Label(fCapt,text="Timestamp: ",justify=RIGHT).grid(row=4,column=1,sticky=E)
		eSec = StringVar(fCapt)
		if config_get("timestamp"): eSec.set("Enabled")
		else: eSec.set("Disabled")
		OptionMenu(fCapt, eSec, "Enabled","Disabled").grid(row=4,column=2,sticky=E+W)

		Label(fCapt,text="EXAMPLE: ",justify=RIGHT).grid(row=5,column=1,sticky=E)
		exampleFname=StringVar()
		Label(fCapt,textvariable=exampleFname,justify=LEFT).grid(row=5,column=2,sticky=E+W)
		updateSample()
		
		Label(fCapt,text="Resize Output: ",justify=RIGHT).grid(row=6,column=1,sticky=E)
		eRes = StringVar(fCapt)
		if config_get("resize"): eRes.set("Enabled")
		else: eRes.set("Disabled")
		OptionMenu(fCapt, eRes, "Enabled","Disabled").grid(row=6,column=2,sticky=E+W)
		
		Label(fCapt,text="Image Width: ",justify=RIGHT).grid(row=7,column=1,sticky=E)
		eWidth=Entry(fCapt)
		eWidth.grid(row=7,column=2,sticky=E+W)
		eWidth.insert(0,config_get("resizeX"))
		
		Label(fCapt,text="Image Height: ",justify=RIGHT).grid(row=8,column=1,sticky=E)
		eHeight=Entry(fCapt)
		eHeight.grid(row=8,column=2,sticky=E+W)
		eHeight.insert(0,config_get("resizeY"))
		
		Label(fCapt,text="ONLY STORED IF YOU:",justify=RIGHT).grid(row=9,column=1,sticky=E)
		Button(fCapt,text="CLICK TO APPLY ALL",command=saveImCap).grid(row=9,column=2,sticky=E+W)
		
	##########################################
	##########################################
	# ########################################
	##########################################
	##########################################
	
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		global config
		def dieNOW():
			log("EXITING as soon as the recorder is done...")
			gui_shutdown(True)
			self.master.destroy()
		self.master.protocol("WM_DELETE_WINDOW", dieNOW)
		if config["pause"]==True: state="[PAUSED] - right-click to resume!"
		else: state=""
		#self.master.title("LOADING!!!")
		#self.master.geometry("300x100")
		self.master.title("LOADING...")
		self.master.update()
		#loading=Label(self.master,text="LOADING...")
		#loading.grid(row=1,column=1)
		self.pack(expand=YES, fill=BOTH)
		self.canv = Canvas(self, relief=SUNKEN)
		
		def hitSite(event=None):
			site="http://www.SWHarden.com/QRSS_VD/"
			webbrowser.open(site)
		def hitSiteDocs(event=None):
			site="http://www.swharden.com/QRSS_VD/#documentation"
			webbrowser.open(site)
		def hitSiteSource(event=None):
			site="http://www.swharden.com/QRSS_VD/#download"
			webbrowser.open(site)
		def hitSiteScott(event=None):
			site="http://www.swharden.com/blog/?page_id=344"
			webbrowser.open(site)
		def hitSiteSuggest(event=None):
			msg="So you have an idea to make QRSS VD better?  Awesome!  Chances are "
			msg+="someone else wants the same feature you do.  Tell me about it and "
			msg+="I'll try to include your idea in the next version of QRSS VD! \n\n"
			#msg+="EMAIL: "+"swharden"+"@"+"gmail"+"."+"c"+"om"
			tkMessageBox.showinfo("SUGGEST A FEATURE",msg)
			#webbrowser.open("http://www.swharden.com/QRSS_VD/#gg")
			webbrowser.open("http://groups.google.com/group/qrss-vd")

		
		def doPause(event=None):
			self.master.title("QRSS VD - Spectrograph Monitor [PAUSED]")
			recorder_pause()
		def doResume(event=None):
			self.master.title("QRSS VD - Spectrograph Monitor")
			recorder_resume()
		
		
		def do_rightClickMenu(event):
			try:popup.tk_popup(event.x_root, event.y_root, 0)
			finally:popup.grab_release()
		def capnw():
			captureNow(im)
			

		
		# RIGHT CLICK MENU#####################
		popup = Menu(self.canv, tearoff=0)
		popup.add_command(label="Return")
		popup.add_command(label="Launch Viewer",command=lambda:os.startfile("QRSS_VD_viewer.exe"))
		popup.add_separator()
		popup.add_command(label="  ||  Pause",command=doPause)
		popup.add_command(label=" >> Resume",command=doResume)
		popup.add_command(label="  ()  Capture Now",command=capnw)
		popup.add_separator()
		popup.add_command(label="Set Sound Card",command=getSoundCards)
		popup.add_command(label="General Settings",command=self.window_settings)
		popup.add_command(label="Autosave Options",command=self.window_autosave)
		popup.add_command(label="Set Base Frequency",command=self.window_offset)		
		popup.add_separator()
		popup.add_command(label="Set as Default",command=config_save)
		popup.add_command(label="Reload From Default",command=config_load)
		popup.add_command(label="Factory Reset",command=delete_file)
		popup.add_separator()
		popup.add_command(label="Program Statistics",command=self.window_stats)
		popup.add_command(label="Developer Console",command=self.window_console)
		popup.add_separator()
		popup.add_command(label="Open Program Folder",command=launchFldr1)
		popup.add_command(label="Open Output Folder",command=launchFldr2)
		popup.add_separator()
		popup.add_command(label="QRSS VD Google Group",command=lambda: webbrowser.open("http://groups.google.com/group/qrss-vd"))
		popup.add_command(label="Does QRSS VD crash?!",command=self.crashDoWhat)
		popup.add_command(label="Suggest a Feature",command=hitSiteSuggest)
		popup.add_separator()
		popup.add_command(label="QRSS VD Website",command=hitSite)
		popup.add_command(label="QRSS VD Documentation",command=hitSiteDocs)
		popup.add_command(label="QRSS VD Source Code",command=hitSiteSource)
		popup.add_command(label="About AJ4VD",command=hitSiteScott)
		popup.add_command(label="Credits",command=credits)
		self.canv.bind("<Button-3>", do_rightClickMenu)
		# ############################################
		
		
		self.canv.config(highlightthickness=0)
		sbarV = Scrollbar(self, orient=VERTICAL)
		sbarH = Scrollbar(self, orient=HORIZONTAL)
		sbarV.config(command=self.canv.yview)
		sbarH.config(command=self.canv.xview)
		self.canv.config(yscrollcommand=sbarV.set)
		self.canv.config(xscrollcommand=sbarH.set)
		sbarV.pack(side=RIGHT, fill=Y)
		sbarH.pack(side=BOTTOM, fill=X)
		self.canv.pack(side=LEFT, expand=YES, fill=BOTH)
		self.im=Image.new("RGB",(config["width"], config["vertSize"]),(0,0,0))
		self.imSplash=genSplash(config["width"], config["vertSize"])
		self.im.paste(self.imSplash,(0,0))
		del self.imSplash
		setThisImage(self.im)
		self.width,self.height=self.im.size
		
		self.vertim=drawVertScale()
		self.vertimp = ImageTk.PhotoImage(self.vertim)
		self.vertlab = self.canv.create_image(self.width,0,anchor="nw",image=self.vertimp)
		
		self.horizim=drawHorizScale(config["width"],config["horizRes"])
		self.horizimp = ImageTk.PhotoImage(self.horizim)
		self.horizlab = self.canv.create_image(0,config["vertSize"],anchor="nw",image=self.horizimp)
		
		self.cornerim=cornerLogo(self.vertim.size[0],self.horizim.size[1])
		self.cornerimp = ImageTk.PhotoImage(self.cornerim)
		self.cornerlab = self.canv.create_image(self.width,self.height,anchor="nw",image=self.cornerimp)
		self.master.title("QRSS VD - Spectrograph Monitor %s"%state)
		
		
		self.canv.config(scrollregion=(0,0,\
			self.width+self.vertim.size[0],\
			self.height+self.horizim.size[1]))
		#goodWidth=config[goodWidth]
		#goodHeight=config[goodWidth]
		self.canv.config(width=self.width+self.vertim.size[0], height=600)
		#self.master.resizable(width=FALSE, height=TRUE) 
		
		def forceSize(event):
			curx,cury=self.master.geometry().split("x")
			cury=cury.split("+")[0]
			wantx=self.width+self.vertim.size[0]+16
			wanty=self.height+self.horizim.size[1]+16
			if int(curx)>wantx:
				self.master.geometry(str(wantx)+"x"+cury)
			if int(cury)>wanty:
				self.master.geometry(curx+"x"+str(wanty))

		#
		#MENU ITEMS ####################################
		self.canv.bind("<Configure>", forceSize)
		# ##############################################
		#
		self.i = ImageTk.PhotoImage(im)
		self.lab = self.canv.create_image(0,0,anchor="nw",image=self.i)
		# THIS THREAD WILL KEEP THE AUDIO RECORDER CONTINUOUSLY RUNNING
		#raw_input("PAUSED")
		recorder_startup()
		#self.doneLoading()
		def updateOrDie():
			if config["dieNOW"]==True: 
				#self.master.destroy()
				return True
			else:
				self.master.update()
				return False
		
		while True:
			while config["updateNow"]==False:
					if updateOrDie()==True: break
			graph()
			while len(chunks)>3:
				if updateOrDie()==True: break
				graph()
			if updateOrDie()==True: break
			try:
				self.i = ImageTk.PhotoImage(im)
			except Exception, err:
				print "got an error, I'll log it..."
				print "CONTENTS:"
				print err
				print "##############"
				break
			self.lab = self.canv.create_image(0,0,\
							anchor="nw",image=self.i)
			config["updateNow"]=False
		time.sleep(1)
		try:
			self.master.destroy()
		except:
			pass

textIntro()			
#raw_input("\n\npress ENTER to begin...")
config_load()
while config["exit"]==False:
	log("LAUNCHING GUI")
	x=frame_spectrograph().mainloop()
	del x
log("EXITING!")
