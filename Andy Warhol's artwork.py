#-------------------------------------------------------------------------------
# Name:        Andy Warhol Marilyn Diptych
# Purpose:     Automatically create Andy Warhol's Marilyn Diptych artwork
#              with any image
#
# Author:      Oazin
#
# Created:     02/02/2021
# Copyright:   (c) Oazin 2021
# Version:     Python 3.4
#-------------------------------------------------------------------------------
from PIL import Image
from random import randint
from math import sqrt

lighting_color = [(121, 248, 248),(0,255,0),(255,255,255),(255,255,0),(0,255,255),(255,0,255),(192,192,192),(220,20,60),(255,99,71),(255,127,80),(240,128,128),(250,128,114),(255,160,122),(255,165,0),(255,215,0),(238,232,170),(240,230,140),(154,205,50),(124,252,0),(127,255,0),(173,255,47),(50,205,50),(144,238,144),(152,251,152),(0,250,154),(0,255,127),(32,178,170),(0,255,255),(224,255,255),(64,224,208),(72,209,204),(175,238,238),(127,255,212),(176,224,230),(0,191,255),(100,149,237),(173,216,230),(135,206,235),(135,206,250),(138,43,226),(147,112,219),(216,191,216),(221,160,221),(238,130,238),(255,0,255),(255,20,147),(255,182,193),(255,192,203),(250,235,215),(245,245,220),(255,228,196),(255,235,205),(255,248,220),(255,250,205),(250,250,210),(255,255,224),(255,222,173),(240,255,255),(248,248,255),(253,245,230),(240,255,240),(255,250,250),(245,255,250)]
dark_color = [(0,0,0),(0, 0, 255),(128,0,0),(255,0,0),(0,128,0),(128,128,128),(128,128,0),(0,128,128),(0,128,0),(128,0,128),(0,0,128),(128,0,0),(139,0,0),(139,0,0),(178,34,34),(205,92,92),(233,150,122),(255,69,0),(255,140,0),(184,134,11),(218,165,32),(189,183,107),(85,107,47),(107,142,35),(0,100,0),(34,139,34),(143,188,143),(46,139,87),(102,205,170),(60,179,113),(47,79,79),(0,128,128),(0,139,139),(0,206,209),(95,158,160),(70,130,180),(0,191,255),(25,25,112),(0,0,128),(0,0,139),(0,0,205),(65,105,225),(75,0,130),(72,61,139),(106,90,205),(139,0,139),(148,0,211),(153,50,204),(128,0,128),(199,21,133),(139,69,19),(160,82,45),(210,105,30),(205,133,63),(244,164,96),(112,128,144),(119,136,153),(105,105,105),(169,169,169)]

def average_pixel(image):
    """This function that detects the brightest pixel and the darkest pixel to average the colors"""
    (xmax,ymax) = image.size
    min_pixel, max_pixel = (115, 115, 115),(115, 115, 115)
    for x in range(xmax):
        for y in range(ymax):
            px = image.getpixel((x,y))
            if min_pixel > px:
                min_pixel = px
            elif max_pixel < px:
                max_pixel = px
    average = int((min_pixel[0] + min_pixel[1] + min_pixel[2] + max_pixel[0] + max_pixel[1] + max_pixel[2])/6)
    return average


def black_white(image):
    """This function transforms an image into an image containing only white and black"""
    (xmax, ymax) = image.size
    average_image = average_pixel(image)
    for x in range(xmax):
        for y in range(ymax):
            px = image.getpixel((x, y))
            (r, g, b) = px
            average = int((r+g+b)/3)
            if average > average_image :
                px2 = (255, 255, 255)
            else:
                px2 = (0, 0, 0)
            image.putpixel((x, y), px2)

def face_detection(image):
    """This function detects the "face" part that is colored with another color (any, it will not be the final color)"""
    (xmax,ymax) = image.size
    image.putpixel((0,ymax-1),(0,255,0))
    start_x, start_y = 0, ymax-1
    end_x, end_y = xmax, -1
    pas_x, pas_y = 1,-1
    cnt = 0
    while cnt < 4:
        for x in range(start_x,end_x,pas_x):
            for y in range(start_y, end_y, pas_y):
                if y > 0 and image.getpixel((x, y-1)) == (0, 255, 0) and image.getpixel((x, y)) == (255, 255, 255):
                    image.putpixel((x,y),(0, 255, 0))
                if y < ymax-1 and image.getpixel((x, y+1)) == (0, 255, 0) and image.getpixel((x, y)) == (255, 255, 255):
                    image.putpixel((x,y),(0, 255, 0))
                if x > 0 and image.getpixel((x-1, y)) == (0, 255, 0) and image.getpixel((x, y)) == (255, 255, 255):
                    image.putpixel((x,y),(0, 255, 0))
                if x < xmax-1 and image.getpixel((x+1, y)) == (0, 255, 0) and image.getpixel((x, y)) == (255, 255, 255):
                    image.putpixel((x,y),(0, 255, 0))
        cnt += 1
        if cnt == 1:
            start_x = xmax-1
            end_x = -1
            pas_x = -1
        if cnt == 2:
            start_x, start_y = 0, 0
            end_x, end_y = xmax, ymax
            pas_x, pas_y = 1,1
        if cnt == 3:
            start_x = xmax-1
            end_x = -1
            pas_x = -1

def coloring(image):
    """Function that colors the background, outline and face with three different suitable colors"""
    (xmax, ymax) = image.size
    c1 = dark_color[randint(1,len(dark_color)-1)]
    c2 = lighting_color[randint(1,len(lighting_color)-1)]
    c3 = lighting_color[randint(1,len(lighting_color)-1)]
    for x in range(xmax):
        for y in range(ymax):
            (r, g, b) = image.getpixel((x, y))
            if (r, g, b) == (0, 0, 0):
                image.putpixel((x, y), c1)
            if (r, g, b) == (255, 255, 255):
                image.putpixel((x, y), c2)
            if (r, g, b) == (0, 255, 0):
                image.putpixel((x, y), c3)

def assembly(image):
    """Function which assembles 9 images to obtain the final rendering"""
    (xmax, ymax) = image.size
    n = 9
    new_image = Image.new('RGB', (int(sqrt(n))*xmax, int(sqrt(n))*ymax))
    i,j = 0,0
    max_i, max_j = xmax-2, ymax-2
    start_x, start_y = 0, 0
    end_x, end_y = xmax, ymax
    im = image.copy()
    cnt = 0
    k = 1
    while cnt < n:
        coloring(im)
        for x in range(start_x,end_x):
            for y in range(start_y,end_y):
                px = im.getpixel((i,j))
                new_image.putpixel((x, y),px)
                if j > max_j:
                    j = 0
                else:
                    j += 1
            if i > max_i:
                i = 0
            else:
                i += 1
        cnt += 1
        if k > 2:
            k = 0
        if cnt < sqrt(n):
            start_y, end_y = ymax*k, ymax*(k+1)
            im = image.copy()
        elif cnt < sqrt(n)*2:
            start_x, end_x = xmax, xmax*2
            start_y, end_y = ymax*k, ymax*(k+1)
            im = image.copy()
        elif cnt < sqrt(n)*3:
            start_x, end_x = xmax*2, xmax*3
            start_y, end_y = ymax*k, ymax*(k+1)
            im = image.copy()
        k +=1
    return new_image

def main():
    image = Image.open("che_guevara.bmp")
    black_white(image)
    face_detection(image)
    new_image = assembly(image)
    new_image.show()

if '__name__' == main():
    main()