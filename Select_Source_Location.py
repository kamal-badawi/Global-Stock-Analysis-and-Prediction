def run_select_source_location(language_index):
    import streamlit as st
    translations_select_source_folder = {
        1: [
            "Select Source location",
            "Einen Quellort auswählen",
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
    st.write(f'{translations_select_source_folder.get(1)[language_index]}')
    store_folder_button_column,store_folder_dummy_column, store_folder_text_column = st.columns([1,0.1,4])
    with store_folder_button_column:
        import tkinter as tk
        from tkinter import filedialog
        source_location_path = ''
        speicherort = ''

        def select_source_location_():
            root = tk.Tk()
            root.withdraw()
            # Mach den PopUp on Top aller den PopUp
            root.wm_attributes('-topmost', 1)
            ornder_pfad = filedialog.askdirectory(master=root)
            root.destroy()
            return ornder_pfad

        source_location_path = st.session_state.get("source_location_path", None)
        # "Choose folder"

        ordner_button = st.button(f'{translations_select_source_folder.get(2)[language_index]}',
                                  key='source_location')




    with store_folder_dummy_column:
        pass

    with store_folder_text_column:
        if ordner_button:
            source_location_path = select_source_location_()
            st.session_state.source_location_path = source_location_path

    if source_location_path is not None:
        st.write(source_location_path)
        return source_location_path
    else:
        st.write(f'{translations_select_source_folder.get(3)[language_index]}')
        return ''