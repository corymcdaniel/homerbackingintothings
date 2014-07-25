from PIL import Image
from PIL import ImageChops 
from images2gif import writeGif
import numpy
import math
import pyimgur
from config import *

def apply_mask(frame, bg, key_color, tolerance):

    # open files
    fg_img = frame.convert('YCbCr')
    bg_img = Image.open(bg).convert('RGB')
    img_size = 400, 300

    # resize image to fit homer.gif pixel size
    if bg_img.size != img_size:
        bg_img = bg_img.resize((img_size), Image.ANTIALIAS)
        bg_img = bg_img.crop((0, 0)+img_size)

    [Y_key, Cb_key, Cr_key] = key_color
    [tol_a, tol_b]= tolerance

    (x,y) = fg_img.size
    fg_data = numpy.array(fg_img.getdata())
    mask_vector = numpy.vectorize(color_close)

    alpha_mask = mask_vector(fg_data[:,1], fg_data[:,2], Cb_key, Cr_key, tol_a, tol_b)
    alpha_mask.shape = (y,x)
    img_mask = Image.fromarray(numpy.uint8(alpha_mask))
    invert_mask = Image.fromarray(numpy.uint8(255-255*(alpha_mask/255)))

    # create images for color mask
    color_mask = Image.new('RGB', (x,y), (0,0,0))
    all_green = Image.new('YCbCr', (x,y), key_color)

    color_mask.paste(all_green, invert_mask)
    fg_img = fg_img.convert('RGB')
    cleaned = ImageChops.subtract(fg_img, color_mask)
    bg_img.paste(cleaned, img_mask)

    return bg_img

def color_close(Cb_p, Cr_p, Cb_key, Cr_key, tol_a, tol_b):
    temp = math.sqrt((Cb_key-Cb_p)**2+(Cr_key-Cr_p)**2)
    if temp < tol_a:
        z = 0.0
    elif temp < tol_b:
        z = ((temp-tol_a)/(tol_b-tol_a))
    else:
        z = 1.0
    return 255.0*z

def to_ycc(r, g, b): 
    y = .299*r + .587*g + .114*b
    cb = 128 - .168736*r -.331364*g + .5*b
    cr = 128 + .5*r - .418688*g - .081312*b
    return int(y), int(cb), int(cr)

def extract_frames(gif, bg):
    img = Image.open(gif)

    rgb_green = [61, 139, 40]
    key_color = to_ycc(*rgb_green)
    tolerance = [15, 15]

    frames = []
    for i, frame in enumerate(iter_frames(img)):
        frames.append(apply_mask(frame, bg, key_color=key_color, tolerance=tolerance))

    bg_name, bg_extension = os.path.splitext(bg)
    writeGif(bg_name+'-homer-masked.gif', frames, duration=0.2)
    return bg_name+'-homer-masked.gif'
        
def iter_frames(im):
    try:
        i = 0
        while 1:
            im.seek(i)
            imframe = im.copy()
            if i == 0: 
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass

def imgur_upload(bg):
    im = pyimgur.Imgur(client_id)
    uploaded_image = im.upload_image(bg, title="Homerfied")
    return uploaded_image.link

def new(bg):
    finished_gif = extract_frames(homer_gif_path, bg)
    imgur_url = imgur_upload(finished_gif)

    # remove files to remain lightweight
    os.remove(bg)
    os.remove(finished_gif)
    return imgur_url
