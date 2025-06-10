def run_multi_stock_analysis(language_index, title):
    import streamlit as st
    import yfinance as yf
    import pandas as pd
    import plotly.graph_objects as go
    import datetime
    from dateutil.relativedelta import relativedelta
    import Tickers as tic
    import Select_Store_Location
    import Process_Button_Styling
    import Centred_Title
    import Background_Style
    import Footer as ft

    Background_Style.run_background_styl()

    # Erstelle eine dicke Linie Funktion
    def draw_line(groesse):
        st.markdown(f"<hr style='border: {groesse}px solid black;'>", unsafe_allow_html=True)

    # Erstelle eine dicke Linie Funktion (Sidebar)
    def draw_line_sidebar(width):
        st.sidebar.markdown(f"<hr style='border: {width}px dashed #009999;'>",
                            unsafe_allow_html=True)

    

    def create_line_chart(data, tickers_multi_stock_analysis,stock_metric, selected_interval):

        data_selected_date_from_to = pd.DataFrame(data)

        # Layout und Grunddiagramm erstellen
        fig = go.Figure()

        # Schleife über alle Spalten außer 'date'
        for col in data_selected_date_from_to.columns:
            if col != 'Date':
                fig.add_trace(
                    go.Scatter(
                        x=data_selected_date_from_to['Date'],
                        y=data_selected_date_from_to[col],
                        mode='lines',
                        name=col
                    )
                )
        title = ''
        count_of_tickers = len(tickers_multi_stock_analysis)
        count_of_tickers_minus_one = count_of_tickers - 1
        counter = 0
        for word in tickers_multi_stock_analysis:
            counter += 1
            title += word
            if counter < count_of_tickers_minus_one:
                title += ', '

            if counter == count_of_tickers_minus_one:
                title += ' and '

        # Layout anpassen
        fig.update_layout(
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),  # Schriftfarbe
            title=dict(
                text=f'{stock_metric} for {title} ({selected_interval}-Interval)',  # Titeltext
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

    # Daten abrufen
    @st.cache_data
    def multi_stock_analysis_fetch_data(tickers, start_date, end_date,stock_metric,selected_interval):
        try:
            if len(tickers) > 1:
                data = yf.download(tickers,
                                   start=start_date,
                                   end=end_date,
                                   interval=selected_interval)['Close']


                for ticker in tickers:
                    if stock_metric == 'Price Change (Absolute)':
                        data[ticker] = data[ticker].diff()
                    elif stock_metric == 'Price Change (%)':
                        data[ticker] = data[ticker].pct_change()  * 100


            else:

                ticker = tickers
                # Lade die Daten des aktuellen Tickers
                data = yf.download(tickers=ticker,
                                   interval=selected_interval,
                                   start=start_date,
                                   end=end_date)['Close']
                if stock_metric == 'Price Change (Absolute)':
                    data[ticker] = data[ticker].diff()
                elif stock_metric == 'Price Change (%)':
                    data[ticker] = data[ticker].pct_change() * 100


            return data
        except:
            st.warning('Bitte andere Daten wählen')
            data = pd.DataFrame({'Date': [None],
                                 'None1': [None],
                                 'None2': [None],
                                 'None3': [None],
                                 'None4': [None]
                                 })

            return data

    # Logo sidebar
    st.sidebar.image("Images/Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)

    multi_stock_analysis_countries_options = ['USA', 'China', 'Germany', 'Japan', 'United Kingdom']

    # Tickers importieren
    tickers_multi_stock_analysis = []
    for country in multi_stock_analysis_countries_options:
        tickers, big_four_tickers = tic.run_tickers(country=country)

        # Einfachauswahl für Ticker
        tickers_multi_stock_analysis_selection = st.sidebar.multiselect(f'{country}-Tickers:',
                                                                        options=tickers,
                                                                        key=f'tickers_multi_stock_analysis_{country}',
                                                                        default=big_four_tickers)
        tickers_multi_stock_analysis = tickers_multi_stock_analysis + tickers_multi_stock_analysis_selection

    # st.write(market_caps)
    multi_stock_analysis_date_from_col, multi_stock_analysis_date_to_col = st.sidebar.columns(2)

    today = datetime.datetime.today().date()

    today_minus_one_year = today - relativedelta(years=1)
    with multi_stock_analysis_date_from_col:
        multi_stock_analysis_date_from = st.date_input(label='Date (From)',
                                                       value=today_minus_one_year,
                                                       key='multi_stock_analysis_date_from')

    multi_stock_analysis_date_from_plus_one_minute = multi_stock_analysis_date_from + relativedelta(minutes=1)

    with multi_stock_analysis_date_to_col:
        multi_stock_analysis_date_to = st.date_input(label='Date (To)',
                                                     value=today,
                                                     min_value=multi_stock_analysis_date_from_plus_one_minute,
                                                     max_value=today,
                                                     key='multi_stock_analysis_date_to')

    selected_interval_col,stock_metrics_col = st.sidebar.columns(2)
    with selected_interval_col:
        # Liste der Intervalle für yfinance
        intervals = [
            "1d",  # 1 day
            "5d",  # 5 days
            "1wk",  # 1 week
            "1mo",  # 1 month
            "3mo"  # 3 months
        ]

        # Liste umkehren
        intervals.reverse()

        # Dropdown-Liste in Streamlit zur Auswahl des Intervalls
        selected_interval = st.selectbox("Interval",
                                         options=intervals,
                                         index=4
                                         )

    with stock_metrics_col:
        stock_metrics_options = ['Current Price',  'Price Change (Absolute)', 'Price Change (%)']
        stock_metric = st.selectbox('Stock metric',
                                       options=stock_metrics_options,
                                       key='stock_metric')

    # Foto Sidebar Stocks API
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')

    # Page Title
    Centred_Title.run_centred_title(title)

    data_multi_stock_analysis = multi_stock_analysis_fetch_data(tickers_multi_stock_analysis,
                                                                multi_stock_analysis_date_from,
                                                                multi_stock_analysis_date_to,
                                                                stock_metric,
                                                                selected_interval)

    data_multi_stock_analysis = data_multi_stock_analysis.reset_index()

    # Daten visualisieren
    create_line_chart(data_multi_stock_analysis, tickers_multi_stock_analysis,stock_metric,selected_interval)

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
                # Lösche die TimeZone Infos
                data_multi_stock_analysis['Date'] = data_multi_stock_analysis['Date'].dt.tz_localize(None)

                data_multi_stock_analysis.to_excel(rf'{store_location_path}/Multi Stock Analysis.xlsx',
                              sheet_name='Multi Stock Analysis Data',
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
