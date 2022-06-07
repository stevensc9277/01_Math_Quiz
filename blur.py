#Import required Image library
from PIL import Image, ImageFilter

#Open existing image
OriImage = Image.open('vivillion.gif')
OriImage.show()

#Applying GaussianBlur filter
gaussImage = OriImage.filter(ImageFilter.GaussianBlur(2))
gaussImage.show()

#Save Gaussian Blur Image
gaussImage.save('gaussian_blur.gif')