def run_sentiment_analysis(language_index,title):
    from transformers import pipeline, MarianMTModel, MarianTokenizer
    import streamlit as st
    import Footer as ft
    import Centred_Title
    import Background_Style
    import Process_Button_Styling


    Process_Button_Styling.run_process_button_style()
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)


    # Erstelle eine dicke Linie Funktion (Sidebar)
    def draw_line_sidebar(width):
        st.sidebar.markdown(f"<hr style='border: {width}px dashed #009999;'>",
                            unsafe_allow_html=True)

    # Wahrscheinlichkeiten Erklärungen visualisieren
    def make_sidebar_metric(probability_text, probability_value):

        if probability_text =='Very sure':
            text_color = 'green'
        elif probability_text =='Moderately sure':
            text_color = '#FFD700'
        elif probability_text =='Unsure':
            text_color = '#871614'

        st.markdown(
            f"""
            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                 <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;color:{text_color};'> {probability_text}</h1>
                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                    <span style='color:black; '>
                    {probability_value} 
                    </span>
                </h1>
               
            </div>
            """, unsafe_allow_html=True
        )

        st.write('')
        st.write('')


    # Sentiment Score visualisieren
    def make_result_score_metric(score_text, score_value):


        if score_text == 'Positive':
            text_color = 'green'
        elif score_text == 'Neutral':
            text_color = '#FFD700'
        elif score_text == 'Negative':
            text_color = '#871614'


        st.markdown(
            f"""
            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                 <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;color:{text_color};'> {score_text}</h1>
                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                    <span style='color:black;'>
                    {score_value*100:.2f}%
                    </span>
                </h1>

            </div>
            """, unsafe_allow_html=True
        )

        st.write('')
        st.write('')


    # Keywords metrics visualisieren
    def make_result_keywords_metric(keyword_type, keyword_value):



        st.markdown(
            f"""
            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                 <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;'> {keyword_type}</h1>
                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>
                    <span style='color:black;'>
                    {keyword_value } 
                    </span>
                </h1>

            </div>
            """, unsafe_allow_html=True
        )

        st.write('')
        st.write('')



    # Lade Modelle
    @st.cache_resource
    def load_translation_model():
        model_name = "Helsinki-NLP/opus-mt-de-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return pipeline("translation", model=model, tokenizer=tokenizer)

    @st.cache_resource
    def load_finbert():
        return pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

    @st.cache_resource
    def load_ner_model():
        return pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

    translator = load_translation_model()
    finbert = load_finbert()
    ner_model = load_ner_model()

    # Logo sidebar
    st.sidebar.image("Images/Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)
    st.sidebar.markdown(
        f"""
                <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                    Probabilities
                </div>
                """,
        unsafe_allow_html=True
    )
    st.sidebar.write('')

    _,probability_col,_ = st.sidebar.columns([1,10000,1])
    with probability_col:

        make_sidebar_metric('Very sure','86% – 100%')
        make_sidebar_metric('Moderately sure', '66% – 85%')
        make_sidebar_metric('Unsure', '50% – 65%')


    # Page Title
    Centred_Title.run_centred_title(title)



    user_input = st.text_area("Financial Text (German):",
                              height=500)

    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)


    if st.button("Determine Sentiment Score"):

        if user_input.strip():#

            translated_text = translator(user_input)[0]['translation_text']

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)
            # Übersetzung
            st.markdown(
                f"""
                           <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                               Translation (English)
                           </div>
                           """,
                unsafe_allow_html=True
            )
            st.write('')


            st.write(translated_text)

            # Eine horizontale ein Pixel Linie hinzufügen
            draw_line(1)

            # Sentiment-Analyse
            st.markdown(
                f"""
               <div style='text-align: center; font-weight: bold; font-size: 1.2vw;'>
                  Sentiment-Score and Keywords
               </div>
               """,
                unsafe_allow_html=True
            )
            st.write('')

            # Übersetzung
            sentiment = finbert(translated_text)



            for result in sentiment:
                result_text = result['label']
                result_value = result['score']
                make_result_score_metric(result_text,result_value)


            st.write('')
            st.write('')

            # NER KEWWORDS
            entities = ner_model(translated_text)

            keywords_col_one, keywords_col_two, keywords_col_three, keywords_col_four = st.columns(4)
            with keywords_col_one:
                iteration = 1
                for entity in entities:
                    if iteration % 4 == 1:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1

            with keywords_col_two:
                iteration = 1
                for entity in entities:
                    if iteration % 4 == 2:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1


            with keywords_col_three:
                iteration = 1
                for entity in entities:
                    if iteration % 4 == 3:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1



            with keywords_col_four:

                iteration = 1
                for entity in entities:
                    if iteration % 4 != 1 and iteration % 4 != 2 and iteration % 4 != 3:
                        keyword_type = entity['entity_group']
                        keyword_value = entity['word']
                        make_result_keywords_metric(keyword_type, keyword_value)
                    iteration += 1




        else:
            st.warning("Please enter a text")






    # Footer importieren
    ft.run_footer(language_index=language_index)


