import streamlit as st




def main_generatecost():

    st.title("Calculateur de coût d'impression")
    st.markdown('Generate costs of designs')
    st.write('\n')  # add spacing

    st.text_input('Nom du projet')
    dim=st.number_input('Dimensions du design (en cm2)')
    rempl=st.number_input('Taux de remplissage (%)')
    blanc=st.number_input('Dose de blanc (en ml)')
    encre=st.number_input('Coût de l\'encre')
    
    st.file_uploader('Fichier RIP')

    res=dim+rempl+blanc
    rep= f"Le coût est de {res} €."
    if st.button("Lancer le calcul"):
        st.write(rep)

if __name__ == '__main__':
    # call main function
    main_generatecost()