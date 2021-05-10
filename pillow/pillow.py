import os, sys
import numpy as np
from numpy import array
from PIL import Image, ImageFilter, ImageEnhance, ImageSequence, ImageDraw, ImageFont   #Import Image, ImageFilter, ImageEnhance, ImageSequence, ImageDraw, ImageFont Class from library

#Read Concepts here: https://pillow.readthedocs.io/en/stable/handbook/concepts.html

im = Image.open('test.jpg')             #load image
print(im.format, im.size, im.mode)       
'''
format attribute identifies the source of an image, if image not read from file then set to NONE.
size attribute is a 2-tuple containing width and height (in pixels). 
mode attribute defines the number and names of the bands in the image, and also the pixel type and depth.
    L(Luminance) : Greyscale Images
    RGB : Color Images
    CMYK : Pre-press Images
    
If file not openable then OSError exception raised.'''

im.show()       #display image

'''Copying a subrectangle from an image'''
box = (100, 300, 600, 1050)          #(left, upper, right, lower)
#Python Imaging Library uses a coordinate system with (0, 0) in the upper left corner. 
cropped = im.crop(box)
cropped.show()
cropped.save('results/cropped.jpg')


'''Processing a subrectangle, and pasting it back'''
cropped = cropped.transpose(Image.ROTATE_180)
im.paste(cropped, box)


'''Splitting and merging bands'''
#for a single-band image, split() returns the image itself.
im = Image.open('test.jpg')
im = im.convert('RGB')              #To work with individual color bands, you may want to convert the image to “RGB” first.
r, g, b = im.split()            
out = Image.merge("RGB", (b, r, g))
out.show()
out = Image.merge('L', (b,))
out.show()
out = Image.merge('RGBA', (r, g, b, b))
out.show()

'''Rolling an Image'''
def roll(image, delta):
    """Roll an image sideways."""
    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0: return image

    #For Horizontal Roll
    part1 = image.crop((0, 0, delta, ysize))               #Use : part1 = image.crop((0, 0, xsize, delta))  For Vertical
    part2 = image.crop((delta, 0, xsize, ysize))           #Use : part2 = image.crop((0, delta, xsize, ysize)) For Vertical

    image.paste(part1, (xsize-delta, 0, xsize, ysize))      #Use : (0, ysize-delta, xsize, ysize) For Vertical
    image.paste(part2, (0, 0, xsize-delta, ysize))          #Use : (0, 0, xsize, ysize-delta) For Vertical
    print('Image Rolled!')
    return image

im = Image.open('test.jpg')
out = roll(im, 900)  #Calling the function, delta value should be within width for horizontal roll or height for vertical role.
out.save('results/Rolled.jpg')
'''
paste() method is used to paste cropped image/image to another image.
User needs to provide place where to paste the image with a tuple (left, upper, right, lower). Users can only provide (left, upper) as well for place and it'll work fine.
One can also use mask which can be used to make pasted images with transparency. The masked image will have values between (0, 255) with 0 values being totally transparent and 255 is opaque.
One can use this function to create a collage.'''


#For running python code 
#Use: python pillow filename.extension
#With this method several files can be loaded at once.
for infile in sys.argv[1:]:             
    '''Identify Image Files'''
    try:
        with Image.open(infile) as im:
            print('Image Identified!')
            print(infile, im.format, f"{im.size}x{im.mode}")
    except OSError:
        print('Image Not Identified!')
    
    '''Convert files to JPEG'''
    f, e = os.path.splitext(infile)
    outfile = f + ".jpg"
    if infile != outfile:
        try:
            with Image.open(infile) as im:
                im.save('results/converted_jpeg.jpg')
                print('Image Converted to JPEG!')
        except OSError:
            print("Cannot convert", infile)
    
    '''Create JPEG thumbnails'''
    size = (128, 128)

    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    if infile != outfile:
        try:
            with Image.open(infile) as im:
                im.thumbnail(size)
                im.save('results/thumbnail.jpg', "JPEG")           #second argument explicitly specifies file format.
                print('Thumbnail Created!')
        except OSError:
            print("Cannot create thumbnail for", infile)

'''Geometrical Transformation'''
im = Image.open('test.jpg')
out = im.resize((128, 128))
out.save('results/resize.jpg')
out = im.rotate(45) # degrees counter-clockwise from 0-360
out.save('results/rotate.jpg')

out = im.transpose(Image.FLIP_LEFT_RIGHT) #similarly Image.FLIP_TOP_BOTTOM, Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270
out.save('results/transpose.jpg')

'''To rotate the image in 90 degree steps, you can either use the rotate() method or the transpose() method. 
The latter can also be used to flip an image around its horizontal or vertical axis.'''

'''Color transforms'''
im = im.convert("L")
im.save('results/L_Conversion.jpg')
#convert() function is used to convert an image from one mode to another. Currently conversion only between images with mode types 'L', 'RGB' and 'CMYK'

'''Image enhancement'''
'''Filters'''
im = Image.open('test.jpg')
out = im.filter(ImageFilter.DETAIL)     
out.save('results/DETAIL.JPG')
out = im.filter(ImageFilter.BLUR)
out.save('results/BLUR.JPG')
out = im.filter(ImageFilter.MinFilter(3))   #MinFilter() used to create a minimum filter. It picks the lowest pixel value in a window with the given size. 
out.save('results/MinFilter.JPG')
out = im.filter(ImageFilter.CONTOUR)
out.save('results/CONTOUR.JPG')
out = im.filter(ImageFilter.EDGE_ENHANCE)
out.save('results/EDGE_ENHANCE.JPG')
out = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
out.save('results/EDGE_ENHANCE_MORE.JPG')
out = im.filter(ImageFilter.EMBOSS)
out.save('results/EMBOSS.JPG')
out = im.filter(ImageFilter.FIND_EDGES)
out.save('results/FIND_EDGES.JPG')
out = im.filter(ImageFilter.SMOOTH)
out.save('results/SMOOTH.JPG')
out = im.filter(ImageFilter.SMOOTH_MORE)
out.save('results/SMOOTH_MORE.JPG')
out = im.filter(ImageFilter.SHARPEN)
out.save('results/SHARPEN.JPG')

'''Point Operations'''
im = Image.open('test.jpg')    
# multiply each pixel by 3.5
out = im.point(lambda i: i * 3.5)       # point() method used to translate the pixel values of an image. 
out.save('results/Point.jpg')

'''Processing individual bands'''
im = Image.open('test.jpg')
# split the image into individual bands
source = im.split()
R, G, B = 0, 1, 2

# select regions where red is less than 100
mask = source[R].point(lambda i: i < 100 and 255)         #Syntax for making mask: imout = im.point(lambda i: expression and 255)

# process the green band
out = source[G].point(lambda i: i * 0.7)

# paste the processed band back, but only where red was < 100
source[G].paste(out, None, mask)

# build a new multiband image
out = Image.merge(im.mode, source)
out.save('results/bands.jpg')

'''Enhancing Images'''
im = Image.open('test.jpg')
enh = ImageEnhance.Contrast(im)     #An enhancement factor of 0.0 gives a solid grey image. A factor of 1.0 gives the original image.
enh.enhance(1.3).save("results/30%_more_contrast.JPG")      
enh = ImageEnhance.Color(im)        #An enhancement factor of 0.0 gives a black and white image. A factor of 1.0 gives the original image.
enh.enhance(0.5).save("results/50%_less_color.JPG")
enh = ImageEnhance.Brightness(im)      #An enhancement factor of 0.0 gives a black image. A factor of 1.0 gives the original image.
enh.enhance(0.7).save("results/30%_less_brighter.JPG") 
enh = ImageEnhance.Sharpness(im)        #An enhancement factor of 0.0 gives a blurred image, a factor of 1.0 gives the original image, and a factor of 2.0 gives a sharpened image.
enh.enhance(1.8).save("results/80%_more_sharper.JPG") 

'''Image Sequence'''
# Supported sequence formats include FLI/FLC, GIF, and a few experimental formats. TIFF files can also contain more than one frame.
'''Reading Sequences'''
with Image.open("animation.gif") as im:
    im.seek(1) #skip to the second frame

    try:
        while 1:
            im.seek(im.tell()+1)
            index = 1
            for frame in ImageSequence.Iterator(im):
                frame.save(f"frames/frame{index}.png")
                index += 1

                im.getdata()
                #im.show()
    except EOFError:
        pass # end of sequence

'''Merging/Collage of Images'''
#Read the two images
image1 = Image.open('marvel.jpg')
image2 = Image.open('cap.jpg')

#resize image
image1 = image1.resize((1920, 1080))
image2 = image2.resize((1920, 1080))

image1_size = image1.size
image2_size = image2.size
new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))

new_image.paste(image1,(0,0))
new_image.paste(image2,(image1_size[0],0))
new_image.save("results/merged_image.jpg","JPEG")

'''Writing Text on Image'''
im = Image.open('test.jpg')
d1 = ImageDraw.Draw(im)
myFont = ImageFont.truetype('arial.ttf', 40)
d1.text((28, 36), "Hello, I am learning Pillow!",font = myFont, fill=(255, 0, 0))
im.save("results/image_text.jpg")

'''Creating Image from Numpy Array'''
'''Creating an RGB image using PIL and save it as a jpg file. In the following example we will −
Create a 150 by 250-pixel array.
Fill left half of the array with orange.
Fill right half of the array with blue.'''

arr = np.zeros([150, 250, 3], dtype=np.uint8)
arr[:,:100] = [255, 128, 0]
arr[:,100:] = [0, 0, 255]
img = Image.fromarray(arr)
img.save("results/RGB_image.jpg")

'''Creating greyscale images'''
arr = np.zeros([150,300], dtype=np.uint8)

#Set grey value to black or white depending on x position
for x in range(300):
    for y in range(150):
        if (x % 16) // 8 == (y % 16)//8:
            arr[y, x] = 0
        else:
            arr[y, x] = 255
img = Image.fromarray(arr)

img.save('results/greyscale.jpg')

'''Creating numpy array from an Image'''
im = Image.open('test.jpg')
#Convert an image to numpy array
img2arr = array(im)

#Print the array
print(img2arr)

#Convert numpy array back to image
arr2im = Image.fromarray(img2arr)

#Save the image generated from an array
arr2im.save("results/array2Image.jpg")

'''Creating a WaterMark'''
im = Image.open('test.jpg')   
width, height = im.size

draw = ImageDraw.Draw(im)
text = "Marvel Entertainment"

font = ImageFont.truetype('arial.ttf', 36)
textwidth, textheight = draw.textsize(text, font)

# calculate the x,y coordinates of the text
margin = 10
x = width - textwidth - margin
y = height - textheight - margin

# draw watermark in the bottom right corner
draw.text((x, y), text, font=font)

#Save watermarked image
im.save('results/watermark.jpg')

'''Explore ImageDraw Module'''
# Docs : https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
# Tutorial : https://www.tutorialspoint.com/python_pillow/python_pillow_imagedraw_module.htm