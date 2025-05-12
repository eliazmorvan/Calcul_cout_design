import streamlit as st
from PIL import Image
import numpy as np

def rgb_to_cmyk(r, g, b):
    r_, g_, b_ = r / 255.0, g / 255.0, b / 255.0
    k = 1 - max(r_, g_, b_)
    if k == 1:
        return 0, 0, 0, 1
    c = (1 - r_ - k) / (1 - k)
    m = (1 - g_ - k) / (1 - k)
    y = (1 - b_ - k) / (1 - k)
    return c, m, y, k

def pourcentage_cmjn(image_path):
    image = Image.open(image_path).convert("RGB")
    pixels = np.array(image)
    h, w, _ = pixels.shape

    total_pixels = h * w
    somme_cmyk = np.zeros(4)

    for row in pixels:
        for r, g, b in row:
            c, m, y, k = rgb_to_cmyk(r, g, b)
            somme_cmyk += np.array([c, m, y, k])

    moyenne_cmyk = somme_cmyk / total_pixels
    return dict(
        Cyan=f"{moyenne_cmyk[0]*100:.2f}%",
        Magenta=f"{moyenne_cmyk[1]*100:.2f}%",
        Jaune=f"{moyenne_cmyk[2]*100:.2f}%",
        Noir=f"{moyenne_cmyk[3]*100:.2f}%"
    )


def main_generatecost():

    st.title("Calculateur de taux d'encrage")

    
    img_up=st.file_uploader('Uploadez votre image avec design')

    if img_up is not None:
        res=pourcentage_cmjn(img_up)

        if st.button("Lancer le calcul"):
            for couleur, valeur in res.items():
                st.write(f"{couleur} : {valeur}")

if __name__ == '__main__':
    # call main function
    main_generatecost()