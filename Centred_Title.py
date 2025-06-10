def run_centred_title(title_text):
    import streamlit as st

    # Erstelle eine dicke Linie Funktion
    def draw_line_centred_title(groesse):
        st.markdown(f"<hr style='border: {groesse}px dotted #009999;margin-bottom: 0;'>", unsafe_allow_html=True)
        st.markdown(f"<hr style='border: {groesse}px dotted black;margin: 0;'>", unsafe_allow_html=True)
    # CSS zum Zentrieren des Textes
    st.markdown(
        """
        <style>
        .centered-title {
            display: flex;
            justify-content: center;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Den Titel mit der CSS-Klasse formatieren
    st.markdown(f'<h1 class="centered-title">{title_text}</h1>', unsafe_allow_html=True)

    # Erstelle eine drei pixel dicke Linie
    draw_line_centred_title(3)


    st.write('')
