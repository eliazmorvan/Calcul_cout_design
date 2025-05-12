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
    somme_cmyk=np.sum(moyenne_cmyk)
    return dict(
        Cyan=f"{moyenne_cmyk[0]*100:.2f}%",
        Magenta=f"{moyenne_cmyk[1]*100:.2f}%",
        Jaune=f"{moyenne_cmyk[2]*100:.2f}%",
        Noir=f"{moyenne_cmyk[3]*100:.2f}%",
        Total=f"{somme_cmyk*100:.2f}%"
    )


def main_generatecost():
    st.markdown("<h1 style='text-align: center; color: #212121;'>🎨 Calculateur de taux d'encrage CMJN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Uploadez une image pour analyser la proportion de couleurs Cyan, Magenta, Jaune et Noir (CMJN).</p>", unsafe_allow_html=True)

    img_up = st.file_uploader('📁 Cliquez pour choisir une image (png, jpg, jpeg)', type=['png', 'jpg', 'jpeg'])

    if img_up is not None:
         
        if st.button("Lancer le calcul"):
            with st.spinner("Calcul en cours..."):
                res = pourcentage_cmjn(img_up)

            st.success("✅ Résultat obtenu avec succès !")
            st.markdown("---")
            st.subheader("Résultats CMJN")
            cols = st.columns(4)
            couleurs = ["Cyan", "Magenta", "Jaune", "Noir"]
            couleurs_hex = ["#00BCD4", "#E91E63", "#FFEB3B", "#212121"]

            for i, couleur in enumerate(couleurs):
                with cols[i]:
                    st.markdown(f"<div style='background-color:{couleurs_hex[i]}; padding:10px; border-radius:10px; text-align:center; color:white; font-weight:bold;'>{couleur}<br>{res[couleur]}</div>", unsafe_allow_html=True)
            st.markdown("### Taux d'encrage total :")
            st.markdown(
                f"<div style='background-color:#607D8B; padding:15px; border-radius:10px; text-align:center; color:white; font-size:24px;'>"
                f"{res['Total']}"
                f"</div>", unsafe_allow_html=True)
        st.image(img_up, caption="Image téléchargée")

if __name__ == '__main__':
    main_generatecost()