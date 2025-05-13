import streamlit as st
from PIL import Image
import numpy as np

def rgb_to_cmyk(r, g, b):
    r_, g_, b_ = 1- r / 255.0, 1- g / 255.0, 1- b / 255.0
    k = min(r_, g_, b_)
    if k == 1:
        return 0, 0, 0, 1
    c = (r_ - k) / (1 - k)
    m = (g_ - k) / (1 - k)
    y = (b_ - k) / (1 - k)
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

def analyse_base_blanche(image_file):
    # Exemple d’analyse spécifique si tu veux traiter la base blanche différemment (ici juste une moyenne d’intensité pour illustrer)
    image = Image.open(image_file).convert("L")  # niveau de gris
    pixels = np.array(image)
    blancheur_moyenne = 1 - (np.mean(pixels) / 255.0)  # plus c’est sombre, plus on imprime en blanc
    return f"{blancheur_moyenne*100:.2f}%"

def main_generatecost():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎨 Analyse d’encrage</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Sélectionnez le type de visuel à analyser :</p>", unsafe_allow_html=True)

    choix = st.radio("Quel type d’impression souhaitez-vous effectuer ?", [
        "1 visuel coloré sur textile blanc",
        "1 visuel coloré sur textile noir",
        "1 visuel blanc sur textile noir",
        "1 visuel noir sur textile blanc"
    ], index=0)

    img_up = st.file_uploader('📁 Uploadez votre image (formats : jpg, jpeg, png)', type=['png', 'jpg', 'jpeg'])

    if img_up is not None:
        

        if st.button("Lancer le calcul"):
            st.markdown("---")
            if (choix == "1 visuel coloré sur textile blanc") or (choix == "1 visuel noir sur textile blanc"):
                with st.spinner("Analyse CMJN en cours..."):
                    res = pourcentage_cmjn(img_up)

                st.success("✅ Analyse terminée")
                cols = st.columns(4)
                couleurs = ["Cyan", "Magenta", "Jaune", "Noir"]
                couleurs_hex = ["#00BCD4", "#E91E63", "#FFEB3B", "#212121"]

                for i, couleur in enumerate(couleurs):
                    with cols[i]:
                        st.markdown(
                            f"<div style='background-color:{couleurs_hex[i]}; padding:10px; border-radius:10px; text-align:center; color:white; font-weight:bold;'>"
                            f"{couleur}<br>{res[couleur]}"
                            f"</div>", unsafe_allow_html=True)

                st.markdown("### Taux d'encrage total :")
                st.markdown(
                    f"<div style='background-color:#607D8B; padding:15px; border-radius:10px; text-align:center; color:white; font-size:24px;'>"
                    f"{res['Total']}"
                    f"</div>", unsafe_allow_html=True)

            elif choix == "1 visuel blanc sur textile noir":
                with st.spinner("Analyse de la base blanche en cours..."):
                    taux_blanc = analyse_base_blanche(img_up)

                st.success("✅ Analyse terminée")
                st.markdown("### Taux estimé d’encrage blanc :")
                st.markdown(
                    f"<div style='background-color:#F5F5F5; padding:15px; border-radius:10px; text-align:center; font-size:24px;'>"
                    f"{taux_blanc}"
                    f"</div>", unsafe_allow_html=True)
            st.image(img_up, caption="Image téléchargée", use_column_width=True)

if __name__ == '__main__':
    main_generatecost()