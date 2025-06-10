def run_footer(language_index):
    import streamlit as st

    footer_translations = [
        "Created by Kamal Badawi",  # Englisch
        "Erstellt von Kamal Badawi",  # Deutsch
        "Creato da Kamal Badawi",  # Italienisch
        "Créé par Kamal Badawi",  # Französisch
        "Creado por Kamal Badawi",  # Spanisch
        "Criado por Kamal Badawi",  # Portugiesisch
        "Skapad av Kamal Badawi",  # Schwedisch
        "Opprettet av Kamal Badawi",  # Norwegisch
        "Oprettet af Kamal Badawi",  # Dänisch
        "Utworzone przez Kamal Badawi",  # Polnisch
        "Создано Камалем Бадави",  # Russisch
        "Створено Камалем Бадаві"  # Ukrainisch
    ]


    st.write('')
    st.write('')


    # "Created by Kamal Badawi"
    st.write(f'**{footer_translations[language_index]} ©**')