def run_forecasting(language_index, app_title):
    import streamlit as st
    import Footer as ft
    import plotly.graph_objects as go
    import datetime
    from dateutil.relativedelta import relativedelta
    import numpy as np
    import pandas as pd
    import logging
    from prophet import Prophet
    import yfinance as yf
    import Tickers as tic
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

    def create_forecast_line_chart(line_chart_data, is_forecast_line_chart_date_from, is_forecast_line_chart_date_to,
                                   is_forecast_line_chart_ticker, today):

        # Erstes Datum finden
        first_forecast_date = line_chart_data[line_chart_data['Is Forecast'] == 'Yes'].iloc[0]['Datetime']

        # Farben der Linie
        colors = ['#FFD700' if forecast == 'Yes' else '#009999' for forecast in line_chart_data['Is Forecast']]

        # Basisdiagramm erstellen
        fig = go.Figure()

        # Linie hinzufügen
        fig.add_trace(go.Scatter(
            x=line_chart_data['Datetime'],
            y=line_chart_data['Close'],
            mode='lines',
            name='Close',
            line=dict(color=None),
            showlegend=False
        ))

        # Linie in Segmenten zeichnen
        for i in range(len(line_chart_data['Datetime']) - 1):
            fig.add_trace(go.Scatter(
                x=line_chart_data['Datetime'][i:i + 2],
                y=line_chart_data['Close'][i:i + 2],
                mode='lines',
                line=dict(color=colors[i]),
                showlegend=False
            ))

        # Vertikale gestrichelte Linie hinzufügen (100% der Y-Achse)
        fig.add_shape(
            type="line",
            x0=first_forecast_date,
            x1=first_forecast_date,
            y0=0,
            y1=1,
            line=dict(
                color="#2C3E50",
                width=2,
                dash="dot",
            ),
            xref="x",
            yref="paper",

        )

        # Layout des Diagramms anpassen
        fig.update_layout(
            plot_bgcolor='#eeeeee',
            paper_bgcolor='#d5d5d5',
            font=dict(color='#009999'),
            title=dict(
                text=f' Forecast between {is_forecast_line_chart_date_from} an {is_forecast_line_chart_date_to} for {is_forecast_line_chart_ticker}',
                x=0.5,
                xanchor='center',
                font=dict(size=25)
            )
        )

        # Achsenfarben anpassen
        fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
        fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))

        # Diagramm in Streamlit anzeigen
        st.plotly_chart(fig, use_container_width=True)

    def forecasting_get_data(
                             selected_ticker,
                             training_date_from,
                             training_date_to,
                             forecast_start_date,
                             count_of_forecast_periods,
                             selected_forecast_interval):

        try:
            selected_ticker_dummy = selected_ticker

            title = selected_ticker



            logging.getLogger("prophet.plot").disabled = True


            selected_ticker = str(selected_ticker).upper()
            title = selected_ticker + ' / USD'



            # Lade die Daten des aktuellen Tickers
            training_date_to_plus_one_day = training_date_to + relativedelta(days=1)
            training_data = yf.download(tickers=selected_ticker,
                                        interval='1d',
                                        start=training_date_from,
                                        end=training_date_to_plus_one_day)

            # Lösche die Ticker-Level aus den Daten
            training_data.columns = training_data.columns.droplevel(1)

            #  Index Spalte zurücksetzen
            training_data = training_data.reset_index()

            training_data = training_data.loc[:, ['Date', 'Close']]

            training_data = training_data.rename(columns={"Date": "Datetime"})

            # Datetime format anpassen
            training_data["Datetime"] = training_data["Datetime"].dt.tz_localize(None)

            # Erstelle das Forecast
            training_data = training_data.rename(
                columns={'Datetime': 'ds', 'Close': 'y'})

            # st.write('training_data',training_data)


            training_data = training_data[training_data['y'] > 0]

            # Logarithmische Transformation anwenden, um Werte zu stabilisieren
            training_data['y'] = np.log(training_data['y'])



            # Prophet-Modell initialisieren
            model = Prophet(weekly_seasonality=True, yearly_seasonality=True)

            # Falls Feiertage definiert sind, dem Modell hinzufügen
            model.add_country_holidays(country_name='US')

            # Modell trainieren
            model.fit(training_data)

            # Zukünftigen Zeitraum definieren

            future = model.make_future_dataframe(periods=count_of_forecast_periods + 1,
                                                 freq=selected_forecast_interval)

            # Vorhersage erstellen
            forecast_result_dataframe = model.predict(future)

            # Exponentielle Rücktransformation der Vorhersagen
            forecast_result_dataframe['yhat'] = np.exp(forecast_result_dataframe['yhat'])

            # Negative Werte durch Mindestwert (z. B. 0) ersetzen
            forecast_result_dataframe['yhat'] = forecast_result_dataframe['yhat'].clip(lower=0)

            # Ausgabe: DataFrame mit den vorhergesagten Werten
            forecast_result_dataframe = forecast_result_dataframe.loc[:, ['ds', 'yhat']]

            forecast_result_dataframe = forecast_result_dataframe.rename(
                columns={'ds': 'Datetime', 'yhat': 'Close'})

            # st.write(forecast_result_dataframe)

            # forecast_result_dataframe = forecast_result_dataframe[forecast_result_dataframe['Is Forecast'] == 'Yes']

            forecast_result_dataframe = forecast_result_dataframe.loc[:, ['Datetime', 'Close']]
            # st.write('forecast_result_dataframe', forecast_result_dataframe)



            forecast_result_dataframe['Is Forecast'] = forecast_result_dataframe['Datetime'].apply(
                lambda x: 'Yes' if x >= pd.to_datetime(forecast_start_date) else 'No'
            )

            # Füge eine neue Spalte mit Tickernamen als erste Spalte im DataFrame
            forecast_result_dataframe.insert(0, 'Ticker', selected_ticker)



            return forecast_result_dataframe,  title
        except:
            st.warning('Bitte andere Daten Wählen')
            return pd.DataFrame({'Datetime': [], 'Close': [], 'Close (Actual)': []}), pd.DataFrame(
                {'Datetime': [], 'Close (Actual)': []}), ''

    # Logo sidebar erstellen
    st.sidebar.image("Images/Logo.png",
                     use_column_width=True)

    # Erstellen einer 3 Pixel-Linie für das Sidebar
    draw_line_sidebar(3)

    forecasting_country_col, forecasting_selected_ticker_col = st.sidebar.columns(2)
    with forecasting_country_col:
        forecasting_countries_options = ['USA', 'China', 'Germany', 'Japan', 'United Kingdom']
        forecasting_selected_country = st.selectbox(label='Country:',
                                              options=forecasting_countries_options)

    with forecasting_selected_ticker_col:
        # Tickers importieren
        tickers, big_four_tickers = tic.run_tickers(country=forecasting_selected_country)

        # Einfachauswahl für Ticker
        selected_ticker = st.selectbox(
            label="Ticker:",
            options=tickers
        )

    today = datetime.datetime.today().date()
    today_minus_ten_years = today - relativedelta(years=10)
    today_minus_seven_days = today - relativedelta(days=7)
    today_minus_one_year = today - relativedelta(years=1)

    training_date_from_col, training_date_to_col, = st.sidebar.columns(2)

    with training_date_from_col:
        training_date_from = st.date_input(label='Training-Date (From):',
                                           value=today_minus_one_year,
                                           min_value=today_minus_ten_years,
                                           max_value=today_minus_seven_days,
                                           key='training_date_from')

    with training_date_to_col:
        training_date_to = st.date_input(label='Training-Date (To):',
                                         value=today,
                                         min_value=today,
                                         max_value=today,
                                         disabled=True,
                                         key='training_date_to')

    selected_interval_col, count_of_periods_col, = st.sidebar.columns(2)

    with selected_interval_col:
        # Liste der Intervalle für Facebook Prophet (Tag, Woche und Monat)
        intervals = [
            "D",
            "W",
            "M",

        ]

        # Liste umkehren
        intervals.reverse()

        # Dropdown-Liste in Streamlit zur Auswahl des Intervalls
        selected_forecast_interval = st.selectbox("Forecast-Interval:",
                                                  options=intervals,
                                                  index=1,
                                                  key='selected_forecast_interval'
                                                  )

    with count_of_periods_col:
        count_of_forecast_periods = st.number_input(label='No. of Periods:',
                                                    min_value=1,
                                                    max_value=1000,
                                                    value=12,
                                                    key='count_of_forecast_periods')

    # Page Title
    Centred_Title.run_centred_title(app_title)

    forecast_start_date = training_date_to + relativedelta(days=1)
    forecast_data,  title = forecasting_get_data(
                                                             selected_ticker,
                                                             training_date_from,
                                                             training_date_to,
                                                             forecast_start_date,
                                                             count_of_forecast_periods,
                                                             selected_forecast_interval)

    forecast_end_date = forecast_start_date + relativedelta(days=count_of_forecast_periods)





    # Erstelle das Liniendiagramm für das Forecast
    create_forecast_line_chart(forecast_data, forecast_start_date, forecast_end_date, selected_ticker, today)

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