import Tickers


def run_plan_actual_comparison(language_index,title):
    import streamlit as st
    import datetime
    import pandas as pd
    import yfinance as yf
    import Footer as ft
    import Process_Button_Styling
    import Select_Store_Location
    import Centred_Title
    import Background_Style
    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Erstelle eine dicke Linie Funktion (Sidebar)
    def draw_line_sidebar(width):
        st.sidebar.markdown(f"<hr style='border: {width}px dashed #009999;'>",
                            unsafe_allow_html=True)

    def create_is_plan_line_chart(line_chart_data, is_forecast_line_chart_date_from, is_forecast_line_chart_date_to, is_forecast_line_chart_ticker):
        import plotly.graph_objects as go
        import streamlit as st

        # Basisdiagramm erstellen
        fig = go.Figure()

        # Linie für "Close (Forecast)"
        fig.add_trace(go.Scatter(
            x=line_chart_data['Datetime'],
            y=line_chart_data['Close (Forecast)'],
            mode='lines',
            name='Close (Forecast)',  # Name in der Legende
            line=dict(color='#009999')  # Farbe der Linie
        ))

        # Linie für "Close (Actual)"
        if 'Close (Actual)' in line_chart_data.columns:  # Prüfen, ob die Spalte existiert
            fig.add_trace(go.Scatter(
                x=line_chart_data['Datetime'],
                y=line_chart_data['Close (Actual)'],
                mode='lines',
                name='Close (Actual)',  # Name in der Legende
                line=dict(color='#ff6600')  # Farbe der Linie
            ))

        # Hintergrund und Layout anpassen
        fig.update_layout(
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),  # Schriftfarbe
            title=dict(
                text=f'Close Preis (Forecast) vs. Close Preis (Actual) between {is_forecast_line_chart_date_from} and {is_forecast_line_chart_date_to} for {is_forecast_line_chart_ticker}',
                x=0.5,  # Zentriert den Titel
                xanchor='center',  # Verankert den Titel in der Mitte
                font=dict(size=25)  # Schriftgröße des Titels
            )
        )

        # Achsenfarben anpassen
        fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
        fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))

        # Diagramm in Streamlit anzeigen
        st.plotly_chart(fig, use_container_width=True)




    def plan_actual_comparison_get_data(selected_ticker,
                                      training_date_from,
                                      training_date_to,
                                      forecast_start_date,
                                      count_of_forecast_periods):
        try:
            import logging
            logging.getLogger("prophet.plot").disabled = True
            from prophet import Prophet
            import numpy as np




            selected_ticker = str(selected_ticker).upper()
            title = selected_ticker + ' / USD'




            ######
            ######
            #####
            # Lade die Daten des aktuellen Tickers
            from datetime import date
            match_actual_data = yf.download(tickers=selected_ticker,
                                                  interval='1d',
                                                  start=pd.to_datetime('2002-01-01').date(),
                                                  end=date.today())
            # Lösche die Ticker-Level aus den Daten
            match_actual_data.columns = match_actual_data.columns.droplevel(1)

            #  Index Spalte zurücksetzen
            match_actual_data = match_actual_data.reset_index()

            match_actual_data = match_actual_data.loc[:, ['Date', 'Close']]

            match_actual_data = match_actual_data.rename(columns={"Date": "Datetime"})

            # Datetime format anpasse
            match_actual_data["Datetime"] = match_actual_data["Datetime"].dt.tz_localize(None)

            match_actual_data = match_actual_data.rename(
                columns={'Close': 'Close (Actual)'})



            #####
            ####
            ####

            # Lade die Daten des aktuellen Tickers
            training_data = yf.download(tickers=selected_ticker,
                               interval='1d',
                               start=training_date_from,
                               end=training_date_to)





            # Lösche die Ticker-Level aus den Daten
            training_data.columns = training_data.columns.droplevel(1)

            #  Index Spalte zurücksetzen
            training_data = training_data.reset_index()

            training_data = training_data.loc[:,['Date','Close']]


            training_data = training_data.rename(columns={"Date": "Datetime"})


            # Datetime format anpasse
            training_data["Datetime"] = training_data["Datetime"].dt.tz_localize(None)







            # FORECAST ERSTELLEN
            training_data = training_data.rename(
                columns={'Datetime':'ds', 'Close':'y'})

            #st.write('training_data',training_data)

            # Annahme: 'training_data' ist ein DataFrame mit Spalten ['ds', 'y'] (für Prophet)
            # Feiertage oder Markt-geschlossene Tage herausfiltern
            training_data = training_data[training_data['y'] > 0]

            # Logarithmische Transformation anwenden, um Werte zu stabilisieren
            training_data['y'] = np.log(training_data['y'])

            # Feiertage definieren (wenn verfügbar)
            # holidays_df = pd.DataFrame({
            #     'holiday': 'market_closed',
            #     'ds': pd.to_datetime(['2023-12-25', '2024-01-01']),  # Beispiel-Feiertage
            #     'lower_window': 0,
            #     'upper_window': 0,
            # })

            # Prophet-Modell initialisieren
            model = Prophet(weekly_seasonality=True, yearly_seasonality=True)

            # Falls Feiertage definiert sind, dem Modell hinzufügen
            model.add_country_holidays(country_name='US')  # Für US-Feiertage
            #model.add_regressor('holiday') # Optional für spezifische Feiertage

            # Modell trainieren
            model.fit(training_data)

            # Zukünftigen Zeitraum definieren
            future = model.make_future_dataframe(periods=count_of_forecast_periods+1, freq='D')

            # Vorhersage erstellen
            forecast_result_dataframe = model.predict(future)

            # Exponentielle Rücktransformation der Vorhersagen
            forecast_result_dataframe['yhat'] = np.exp(forecast_result_dataframe['yhat'])

            # Negative Werte durch Mindestwert (z. B. 0) ersetzen
            forecast_result_dataframe['yhat'] = forecast_result_dataframe['yhat'].clip(lower=0)

            # Ausgabe: DataFrame mit den vorhergesagten Werten
            forecast_result_dataframe = forecast_result_dataframe.loc[:,['ds','yhat']]


            forecast_result_dataframe = forecast_result_dataframe.rename(
                columns={'ds': 'Datetime', 'yhat': 'Close (Forecast)'})


            forecast_result_dataframe['Is Forecast'] = forecast_result_dataframe['Datetime'].apply(
                lambda x: 'Yes' if x > pd.to_datetime(forecast_start_date) else 'No'
            )



            forecast_result_dataframe = forecast_result_dataframe[forecast_result_dataframe['Is Forecast'] == 'Yes']


            forecast_result_dataframe = forecast_result_dataframe.loc[:, ['Datetime', 'Close (Forecast)']]
            #st.write('forecast_result_dataframe', forecast_result_dataframe)

            # Merge on the 'Datetime' column
            forecast_data = pd.merge(
                    forecast_result_dataframe,
                    match_actual_data,
                    on='Datetime',  # Specify the common column
                    how='inner'     # Choose 'inner', 'outer', 'left', or 'right' join as needed
                    )

            #st.write('forecast_data',forecast_data)

            # Füge eine neue Spalte mit Tickernamen als erste Spalte im DataFrame
            forecast_data.insert(0, 'Ticker', selected_ticker)


            return forecast_data, title
        except:
            st.warning('Bitte andere Daten Wählen')
            return pd.DataFrame({'Datetime':[],'Close (Forecast)':[],'Close (Actual)':[]}),pd.DataFrame({'Datetime':[],'Close (Actual)':[]}),''

    # Logo sidebar
    st.sidebar.image("Images/Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)



    selected_country_col, selected_ticker_col = st.sidebar.columns(2)

    with selected_country_col:
        # Market auswählen
        plan_actual_comparison_countries_options = ['USA', 'China', 'Germany', 'Japan', 'United Kingdom']
        # Dropdown-Liste in Streamlit zur Auswahl des Intervalls
        plan_actual_comparison_selected_country = st.selectbox("Country:",
                                                                       options=plan_actual_comparison_countries_options,
                                                                       index=0,
                                                                       key='plan_actual_comparison_selected_country'

                                                                       )

    with selected_ticker_col:

        tickers, big_four_tickers  = Tickers.run_tickers(country=plan_actual_comparison_selected_country)

        # Einfachauswahl für Ticker
        selected_ticker = st.selectbox(
            label="Ticker:",
            options=tickers
        )

    from dateutil.relativedelta import relativedelta
    today = datetime.datetime.today().date()
    today_minus_ten_years = today - relativedelta(years=10)




    training_date_from_col, training_date_to_col, = st.sidebar.columns(2)

    with training_date_from_col:
        training_date_from = st.date_input(label='Training-Date (From):',
                                              value=today_minus_ten_years,
                                              min_value=today_minus_ten_years,
                                              max_value=today,
                                              key='training_date_from')

    with training_date_to_col:
        training_date_to = st.date_input(label='Training-Date (To):',
                                            value=pd.to_datetime('2022-12-31').date(),
                                            min_value=today_minus_ten_years,
                                            max_value=today,
                                            key='training_date_to')



    count_of_forecast_periods = st.sidebar.number_input(label='Anzahl der Forecast-Tage:',
                                       min_value=12,
                                       max_value=1000,
                                       value=365,
                                       key='count_of_forecast_periods')



    # Page Title
    Centred_Title.run_centred_title(title)

    forecast_start_date = training_date_to + relativedelta(days=1)
    forecast_data, title = plan_actual_comparison_get_data(selected_ticker,
                                                                      training_date_from,
                                                                      training_date_to,
                                                                      forecast_start_date,
                                                                      count_of_forecast_periods)

    forecast_end_date = forecast_start_date + relativedelta(days=count_of_forecast_periods)



    create_is_plan_line_chart(forecast_data,forecast_start_date,forecast_end_date,selected_ticker)





    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)

    store_location_path = Select_Store_Location.run_select_store_location(language_index=language_index)

    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)
    # Daten speichern
    process_button_dummy_one, process_button, process_button_dummy_two = st.columns([1.5, 1, 1.5])
    with process_button_dummy_one:
        pass
    with process_button:
        Process_Button_Styling.run_process_button_style()
        if st.button("Store data locally"):
            if len(store_location_path) > 0:

                forecast_data.to_excel(rf'{store_location_path}/Forecast vs. Actual.xlsx',
                                          sheet_name='Forecast vs. Actual',
                                          index=False)




                st.success('Successfully stored')
            else:
                st.warning(
                    # "Please complete your details and check them for accuracy"
                    f'Please complete your entries')
    with process_button_dummy_two:
        pass


    # Footer importieren
    ft.run_footer(language_index=language_index)


