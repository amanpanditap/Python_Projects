# Pillow
Jupyter Notebook for better Readibility, Use python code for running.
Check out the code for detailed explaination and go through the results.

- Command to run : `python pillow.py test.jpg`

The output after running the code is here:

### Starting Image

<img src="pillow/test.jpg" height = 400 width = 800>

### Copying a subrectangle from an image

<img src="pillow/results/cropped.jpg" height = 400 width = 800>

### Splitting and merging bands

- RGB : <img src="pillow/results/RGB.png" height = 400 width = 800>

- L : <img src="pillow/results/L.png" height = 400 width = 800>

- RGBA : <img src="pillow/results/RGBA.png" height = 400 width = 800>

### Rolling an Image

<img src="pillow/results/Rolled.jpg" height = 400 width = 800>

### Identify Image Files, Convert files to JPEG, Create JPEG thumbnails

- Command Line output for Identify Image Files
<img src="pillow/results/IJT.png" height = 400 width = 800>

- Converting to JPEG
As the image is itself in JPEG no need for conversion.

- Thumbnail
<img src="pillow/results/thumbnail.jpg" height = 128 width = 128>

### Geometrical Transformation

<img src="pillow/results/resize.jpg" height = 400 width = 800>

<img src="pillow/results/rotate.jpg" height = 400 width = 800>

<img src="pillow/results/transpose.jpg" height = 400 width = 800>

### Color Transforms

<img src="pillow/results/L_Conversion.jpg" height = 400 width = 800>

### Image Enhancement

#### Filters
- DETAIL
<img src="pillow/results/DETAIL.JPG" height = 400 width = 800>

- BLUR
<img src="pillow/results/BLUR.JPG" height = 400 width = 800>

- MinFilter
<img src="pillow/results/MinFilter.JPG" height = 400 width = 800>

- CONTOUR
<img src="pillow/results/CONTOUR.JPG" height = 400 width = 800>

- EDGE_ENHANCE
<img src="pillow/results/EDGE_ENHANCE.JPG" height = 400 width = 800>

- EDGE_ENHANCE_MORE
<img src="pillow/results/EDGE_ENHANCE.JPG" height = 400 width = 800>

- EMBOSS
<img src="pillow/results/EMBOSS.JPG" height = 400 width = 800>

- FIND_EDGES
<img src="pillow/results/FIND_EDGES.JPG" height = 400 width = 800>

- SMOOTH
<img src="pillow/results/SMOOTH.JPG" height = 400 width = 800>

- SMOOTH_MORE
<img src="pillow/results/SMOOTH_MORE.JPG" height = 400 width = 800>

- SHARPEN
<img src="pillow/results/SHARPEN.JPG height = 400 width = 800>

#### Point Operations
<img src="pillow/results/Point.jpg" height = 400 width = 800>

#### Processing Individual Bands
<img src="pillow/results/bands.jpg" height = 400 width = 800>

#### Enhancing Images
- 30% More Contrast
<img src="pillow/results/30% more contrast.JPG" height = 400 width = 800>

- 50% Less Colour
<img src="pillow/results/50% less colour.JPG" height = 400 width = 800>

- 30% Less Brighter
<img src="pillow/results/30% less brighter.JPG" height = 400 width = 800>

- 80% More Sharper
<img src="pillow/results/80% more sharper.JPG" height = 400 width = 800>

### Image Sequences
Check out the frames folder for the captured images saved from the animated GIF.

### Merging/Collage of Images
<img src="pillow/results/merged_image.jpg" height = 400 width = 800>

### Writing Text on Image
<img src="pillow/results/image_text.jpg" height = 400 width = 800>

### Creating Image from Numpy Array
<img src="pillow/results/RGB_image.jpg" height = 400 width = 800>

### Creating greyscale images
<img src="pillow/results/greyscale.jpg" height = 400 width = 800>

### Creating numpy array from an Image
- Array 
[[[173 186 205]
  [108 123 144]
  [111 127 152]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 [[173 186 205]
  [108 123 144]
  [111 127 152]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 [[173 186 205]
  [108 123 144]
  [111 127 152]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 ...

 [[  0   0   0]
  [  0   0   0]
  [  0   0   0]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 [[  0   0   0]
  [  0   0   0]
  [  0   0   0]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]

 [[  0   0   0]
  [  0   0   0]
  [  0   0   0]
  ...
  [  0   0   0]
  [  0   0   0]
  [  0   0   0]]]

- Image
<img src="pillow/results/array2Image.jpg" height = 400 width = 800>

### Creating a WaterMark
<img src="pillow/results/watermark.jpg" height = 400 width = 800>
