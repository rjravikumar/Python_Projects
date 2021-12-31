#!/usr/bin/env python

import numpy
import os
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# open SECH.png
shape = numpy.array(Image.open("Word_Cloud/img/SECH.png"))

dirname = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# open sech_name.txt that contains all my posts
text = open(path.join(dirname, "sech_name.txt"), "r", encoding="utf-8").read()

# external font
font_path = "Word_Cloud/font/Marcha.ttf"

# Define parameter for the wordCloud image
wordcloud = WordCloud(
    background_color="white",
    font_path=font_path,
    contour_width=5,
    mask=shape,
    contour_color="black",
).generate(text)

plt.imshow(wordcloud, interpolation="bilinear")

# store to file
wordcloud.to_file("Word_Cloud/img/SECH_mask.png")
plt.axis("off")
plt.show()
