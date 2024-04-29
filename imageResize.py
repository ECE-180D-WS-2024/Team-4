from PIL import Image
import os

# Open an image file
with Image.open(os.path.join('img', 'box.png')) as img:
    # Resize the image
    img = img.resize((32, 32), Image.ANTIALIAS)
    img = img.convert('RGB')
    # Save the resized image
    img.save('resized_image.jpg')
