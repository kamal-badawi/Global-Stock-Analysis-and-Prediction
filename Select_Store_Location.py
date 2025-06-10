def run_select_store_location(language_index):
    import streamlit as st
    translations_select_store_folder = {
        1: [
            "Select Store location",
            "Einen Speicherort auswählen",
            "Seleziona posizione",
            "Sélectionnez l'emplacement",
            "Seleccionar ubicación",
            "Selecionar local",
            "Välj plats",
            "Velg plassering",
            "Vælg placering",
            "Wybierz lokalizację",
            "Выберите место",
            "Вибрати місце розташування"
        ],
        2: [
            "Folder selection",
            "Ordner auswählen",
            "Seleziona cartella",
            "Sélection de dossier",
            "Seleccionar carpeta",
            "Selecionar pasta",
            "Mappval",
            "Mappevalg",
            "Mappetræk",
            "Wybór folderu",
            "Выбор папки",
            "Вибір теки"
        ],
        3: [
            "No location selected",
            "Es wurde kein Speicherort ausgewählt",
            "Nessuna posizione selezionata",
            "Aucune position sélectionnée",
            "No se ha seleccionado ninguna ubicación",
            "Nenhuma localização selecionada",
            "Ingen plats vald",
            "Ingen plassering valgt",
            "Ingen placering valgt",
            "Nie wybrano lokalizacji",
            "Местоположение не выбрано",
            "Місце розташування не вибрано"
        ]

    }

    # "Select a location"
    st.write(f'{translations_select_store_folder.get(1)[language_index]}:')
    store_folder_button_column, store_folder_dummy_column, store_folder_text_column = st.columns([1, 0.1, 4])
    with store_folder_button_column:
        import tkinter as tk
        from tkinter import filedialog
        store_location_path = ''
        speicherort = ''

        def select_store_location():
            root = tk.Tk()
            root.withdraw()
            # Mach den PopUp on Top aller den PopUp
            root.wm_attributes('-topmost', 1)
            ornder_pfad = filedialog.askdirectory(master=root)
            root.destroy()
            return ornder_pfad

        store_location_path = st.session_state.get("store_location_path", None)
        # "Choose folder"

        ordner_button = st.button(f'{translations_select_store_folder.get(2)[language_index]}',
                                  key='store_location')

    with store_folder_dummy_column:
        pass
    with store_folder_text_column:
        # Button Ordner Auswählen
        if ordner_button:
            store_location_path = select_store_location()
            st.session_state.store_location_path = store_location_path



        # Text ausgewählter Ornder
        if store_location_path is not None:
            st.write(store_location_path)
            return store_location_path
        else:
            st.write(f'{translations_select_store_folder.get(3)[language_index]}')
            return ''