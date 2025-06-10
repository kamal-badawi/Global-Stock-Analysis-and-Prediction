def run_market_trends(language_index, app_title):
    import streamlit as st
    import datetime
    from dateutil.relativedelta import relativedelta
    import pandas as pd
    import pandas_ta as ta
    from bokeh.plotting import figure, column
    import plotly.express as px
    import Tickers as tic
    import yfinance as yf
    import Process_Button_Styling
    import Select_Store_Location
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

    def market_trends_load_data(start_date, end_date, selected_ticker, selected_interval):
        import streamlit as st


        title = selected_ticker



        # Lade die Daten des aktuellen Tickers
        data = yf.download(tickers=selected_ticker,
                           interval=selected_interval,
                           start=start_date,
                           end=end_date)

        # Lösche die Ticker-Level aus den Daten
        data.columns = data.columns.droplevel(1)

        # Index Spalte zurücksetzen
        data = data.reset_index()

        # Umbennen der Spalte 'Date' zu 'Datetime'
        data = data.rename(columns={"Date": "Datetime"})

        # Datetime format anpasse
        data["Datetime"] = data["Datetime"].dt.tz_localize(None)

        # Füge eine neue Spalte mit Tickernamen als erste Spalte im DataFrame
        data.insert(0, 'Ticker', selected_ticker)

        # Berechne Tech. Indikatoren
        data["Datetime"] = pd.to_datetime(data["Datetime"])
        data["BarColor"] = data[["Open", "Close"]].apply(lambda o: "red" if o.Open > o.Close else "green",
                                                         axis=1)
        data["Date_Text"] = data["Datetime"].astype(str)
        talib_indicators_select = []

        ####
        #### 1.2.	Trendindikatoren
        ####

        # 1.2.1 Berechnung von Moving Average (MA)
        try:
            data['SMA'] = ta.sma(data['Close'], length=14)

            # Berechnung der Exponential Moving Average (EMA)
            data['EMA'] = ta.ema(data['Close'], length=14)

            # Berechnung der Weighted Moving Average (WMA)
            data['WMA'] = ta.wma(data['Close'], length=14)

            talib_indicators_select = talib_indicators_select + ["Moving Average (MA)"]

        except:
            st.warning('Fehler bei der Berechnung von Moving Average (MA)-Indikatoren')

        # 1.2.2 Berechnung von Directional Moving Index (DMI)
        try:
            dm = ta.dm(data['High'], data['Low'], length=14)
            data['DMN'] = dm['DMN_14']
            data['DMP'] = dm['DMP_14']

            talib_indicators_select = talib_indicators_select + ["Directional Movement Index (DMI)"]


        # Im Falle eines Fehlers
        except Exception as e:
            st.warning(f'Fehler bei der Berechnung von Directional Movement Index (DMI)-Indikatoren {e}')

        # 1.2.3 Berechnung von Average Directional Movement Index (ADX)
        try:
            adx = ta.adx(data['High'], data['Low'], data['Close'], length=14)
            data['ADX'] = adx['ADX_14']

            talib_indicators_select = talib_indicators_select + ['Average Directional Movement Index (ADX)']


        # Im Falle eines Fehlers
        except Exception as e:
            st.warning(f'Fehler bei der Berechnung von Average Directional Movement Index (ADX)-Indikatoren {e}')

        # 1.2.4 Berechnung von Bölliger Bänder (BB)
        try:
            bb = ta.bbands(close=data['Close'], length=20, std=2, append=True)

            data['BB_Lower'] = bb['BBL_20_2.0']
            data['BB_Mid'] = bb['BBM_20_2.0']
            data['BB_Upper'] = bb['BBU_20_2.0']

            talib_indicators_select = talib_indicators_select + ['Bölliger Bänder (BB)']


        # Im Falle eines Fehlers
        except Exception as e:
            st.warning(f'Fehler bei der Berechnung von Bölliger Bänder (BB)-Indikatoren {e}')

        # 1.2.5 Berechnung von Supertrend-Indikator
        try:
            supertrend = ta.supertrend(data['High'], data['Low'], data['Close'], length=7)
            data['Supertrend'] = supertrend['SUPERT_7_3.0']

            talib_indicators_select = talib_indicators_select + ['Supertrend']


        # Im Falle eines Fehlers
        except:
            st.warning('Fehler bei der Berechnung von Supertrend-Indikator')

        ####
        #### 1.3.	Momentumindikatoren
        ####

        # 1.3.1 Berechnung von Willams %R Indikator
        try:
            data['Willams_%R'] = ta.willr(data['High'], data['Low'], data['Close'], length=14)

            talib_indicators_select = talib_indicators_select + ['Willams %R']


        # Im Falle eines Fehlers
        except:
            st.warning('Fehler bei der Berechnung von Willams %R-Indikator')

        # 1.3.2 Berechnung von Momentum Indikator (MOM)
        try:
            data['MOM'] = ta.mom(data['Close'], length=10)

            talib_indicators_select = talib_indicators_select + ['Momentum Indikator (MOM)']


        # Im Falle eines Fehlers
        except:
            st.warning('Fehler bei der Berechnung von Momentum (MOM)-Indikator')

        ####
        #### 1.4.	Volumenindikatoren
        ####

        # 1.4.1 Chaikin Money Flow Indikator (CMF)
        try:
            data['CMF'] = ta.cmf(data['High'], data['Low'], data['Close'], data['Volume'], length=20)

            talib_indicators_select = talib_indicators_select + ['Chaikin Money Flow (CMF)']


        # Im Falle eines Fehlers
        except:
            st.warning('Fehler bei der Berechnung von Chaikin Money Flow (CMF)-Indikator')

        # 1.4.2 Ease of Movement Indikator (EoM)
        try:
            data['EoM'] = ta.eom(high=data['High'], low=data['Low'], close=data['Close'], volume=data['Volume'],
                                 length=14)

            talib_indicators_select = talib_indicators_select + ['Ease of Movement (EoM)']


        # Im Falle eines Fehlers
        except Exception as e:
            st.warning(f'Fehler bei der Berechnung von Ease of Movement (EoM)-Indikator {e}')

        ####
        #### 1.5.	Volatilitätsindikatoren/Oszillatoren
        ####

        # 1.5.1 Commiodity Channel Index (CCI)-Indikator
        try:
            data['CCI'] = ta.cci(data['High'], data['Low'], data['Close'], length=20)

            talib_indicators_select = talib_indicators_select + ['Commiodity Channel Index (CCI)']


        # Im Falle eines Fehlers
        except:
            st.warning('Fehler bei der Berechnung von Commiodity Channel Index (CCI)-Indikator')

        # 1.5.2 Relative Strength Index (RSI)-Indikator
        try:
            rsi = ta.rsi(data['Close'], length=14)
            data['RSI'] = rsi

            talib_indicators_select = talib_indicators_select + ['Relative Strength Index (RSI)']


        # Im Falle eines Fehlers
        except Exception as e:
            st.warning(f'Fehler bei der Berechnung von Relative Strength Index (RSI)-Indikator {e}')

        # 1.5.3 Stochastik Oszillator %K und %D-Indikatoren
        try:
            stoch = ta.stoch(data['High'], data['Low'], data['Close'])

            data['Stoch_%K'] = stoch['STOCHk_14_3_3']
            data['Stoch_%D'] = stoch['STOCHd_14_3_3']

            talib_indicators_select = talib_indicators_select + ['Stochastik Oszillator %K und %D']


        # Im Falle eines Fehlers
        except:
            st.warning('Fehler bei der Berechnung von Stochastik Oszillator %K und %D-Indikatoren')

        # 1.5.4 Average True Range (ATR)-Indikator
        try:
            data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)
            talib_indicators_select = talib_indicators_select + ['Average True Range (ATR)']


        # Im Falle eines Fehlers
        except:
            st.warning('Fehler bei der Berechnung von Average True Range (ATR)-Indikator')

        return data, talib_indicators_select, title

    def create_chart(title, df, close_price_line=False, open_price_line=False, low_price_line=False,
                     high_price_line=False, indicators_input=[], selected_ticker='', indicator_colors=False):
        indicators_output = []
        for indicator in indicators_input:
            if indicator == 'Moving Average (MA)':
                indicators_output.append('SMA')
                indicators_output.append('EMA')
                indicators_output.append('WMA')

            elif indicator == 'Directional Movement Index (DMI)':
                indicators_output.append('DMP')
                indicators_output.append('DMN')

            elif indicator == 'Average Directional Movement Index (ADX)':
                indicators_output.append('ADX')

            elif indicator == 'Bölliger Bänder (BB)':
                indicators_output.append('BB_Lower')
                indicators_output.append('BB_Mid')
                indicators_output.append('BB_Upper')

            elif indicator == 'Supertrend':
                indicators_output.append('Supertrend')

            elif indicator == 'Willams %R':
                indicators_output.append('Willams_%R')

            elif indicator == 'Momentum Indikator (MOM)':
                indicators_output.append('MOM')

            elif indicator == 'Ease of Movement (EoM)':
                indicators_output.append('EoM')

            elif indicator == 'Commiodity Channel Index (CCI)':
                indicators_output.append('CCI')

            elif indicator == 'Relative Strength Index (RSI)':
                indicators_output.append('RSI')

            elif indicator == 'Stochastik Oszillator %K und %D':
                indicators_output.append('Stoch_%K')
                indicators_output.append('Stoch_%D')

            elif indicator == 'Average True Range (ATR)':
                indicators_output.append('ATR')

        ## Candlestick Pattern Logic
        candle = figure(x_axis_type="datetime",
                        outer_height=500,
                        inner_height=500,
                        x_range=(df.Datetime.values[0], df.Datetime.values[-1]),
                        tooltips=[("Datetime", "@Date_Text"),
                                  ("Open", "@Open"),
                                  ("High", "@High"),
                                  ("Low", "@Low"),
                                  ("Close", "@Close")], )

        candle.segment("Datetime", "Low", "Datetime", "High", color="black", line_width=0.5, source=df)
        candle.segment("Datetime", "Open", "Datetime", "Close", line_color="BarColor",
                       line_width=2 if len(df) > 100 else 6,
                       source=df)

        # Setze die Hintergrundfarbe
        candle.background_fill_color = '#eeeeee'  # Hier kannst du die Farbe ändern
        candle.border_fill_color = '#d5d5d5'  # Die Farbe des Rahmens (optional)

        # Diagramm Titel
        candle.title.text = f'{title} ({selected_interval}-Interval)'
        candle.title_location = "above"  # Titel über dem Diagramm
        candle.title.align = "center"  # Zentriere den Titel horizontal

        # Achsen Beschriftung
        candle.xaxis.axis_label = "Datetime"
        candle.yaxis.axis_label = f"Price ($)"

        ## Close Price Line
        if close_price_line:
            candle.line("Datetime",
                        "Close",
                        color='#009999',
                        source=df,
                        legend_label='Close')

        ## Open Price Line
        if open_price_line:
            candle.line("Datetime",
                        "Open",
                        color='#FF6F61',
                        source=df,
                        legend_label='Open')

        ## Low Price Line
        if low_price_line:
            candle.line("Datetime",
                        "Low",
                        color='#6B5B95',
                        source=df,
                        legend_label='Low')

        ## High Price Line
        if high_price_line:
            candle.line("Datetime",
                        "High",
                        color='#88B04B',
                        source=df,
                        legend_label='High')

        for indicator in indicators_output:
            candle.line("Datetime", indicator, color=indicator_colors[indicator], line_width=2, source=df,
                        legend_label=indicator)

        return column(children=[candle], sizing_mode="scale_width")

    # Logo sidebar
    st.sidebar.image("Images/Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)

    market_trends_countries_options = ['USA', 'China', 'Germany', 'Japan', 'United Kingdom']
    market_trends_selected_country = st.sidebar.selectbox(label='Country:',
                                                   options=market_trends_countries_options,
                                                          key='market_trends_selected_country')

    selected_ticker_col, selected_interval_col = st.sidebar.columns(2)

    with selected_ticker_col:
        tickers, big_four_tickers = tic.run_tickers(country=market_trends_selected_country)

        # Einfachauswahl für Ticker
        candle_scope_selected_ticker = st.selectbox(
            label="Ticker:",
            options=tickers
        )

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
        selected_interval = st.selectbox("Interval:",
                                         options=intervals,
                                         index=4
                                         )

    candle_scope_date_from_col, candle_scope_date_to_col = st.sidebar.columns(2)

    today = datetime.datetime.today().date()

    candle_scope_today_minus_two_years = today - relativedelta(years=2)
    candle_scope_today_minus_twenty_years = today - relativedelta(years=20)
    with candle_scope_date_from_col:
        candle_scope_date_from = st.date_input(label='Date (From):',
                                               min_value=candle_scope_today_minus_twenty_years,
                                               value=candle_scope_today_minus_two_years,
                                               key='candle_scope_date_from')

    candle_scope_date_from_plus_one_month = candle_scope_date_from + relativedelta(months=1)

    with candle_scope_date_to_col:
        candle_scope_date_to = st.date_input(label='Date (To):',
                                             value=today,
                                             min_value=candle_scope_date_from_plus_one_month,
                                             max_value=today,
                                             key='candle_scope_date_to')

    market_trends_close_price_line = False
    market_trends_open_price_line = False
    market_trends_low_price_line = False
    market_trends_high_price_line = False
    market_trends_volume_line_chart = False

    market_trends_included_kpis_options =['Closing price', 'Opening price', 'Lowest price', 'Highest price', 'Trading volume']
    market_trends_included_kpis = st.sidebar.multiselect(label="Key Figures:",
                                                        options=market_trends_included_kpis_options,
                                                        key='market_trends_included_kpis')

    if 'Closing price' in market_trends_included_kpis:
        market_trends_close_price_line = True
        # st.write(market_trends_close_price_line)

    if 'Opening price' in market_trends_included_kpis:
        market_trends_open_price_line = True
        # st.write(market_trends_open_price_line)

    if 'Lowest price' in market_trends_included_kpis:
        market_trends_low_price_line = True
        # st.write(market_trends_low_price_line)

    if 'Highest price' in market_trends_included_kpis:
        market_trends_high_price_line = True
        # st.write(market_trends_high_price_line)

    if 'Trading volume' in market_trends_included_kpis:
        market_trends_volume_line_chart = True
        # st.write(market_trends_volume_line_chart)

    # Page Title
    Centred_Title.run_centred_title(app_title)

    # Charts
    market_trends_data, candle_scope_talib_indicators, title = market_trends_load_data(
        start_date=candle_scope_date_from,
        end_date=candle_scope_date_to,
        selected_ticker=candle_scope_selected_ticker,
        selected_interval=selected_interval
    )




    # Farbzuordnung für Indikatoren basierend auf indicators_output
    candle_scope_indicator_colors = {
        "SMA": "#FF5733",  # Bright Orange
        "EMA": "#6A0DAD",  # Deep Purple
        "WMA": "#3498DB",  # Sky Blue
        "RSI": "#F1C40F",  # Vibrant Yellow
        "MOM": "#2C3E50",  # Dark Blue-Gray
        "BB_Upper": "#E67E22",  # Pumpkin Orange
        "BB_Mid": "#BDC3C7",  # Light Gray
        "BB_Lower": "#3498DB",  # Sky Blue
        "Stoch_%K": "#9B59B6",  # Amethyst
        "Stoch_%D": "#34495E",  # Wet Asphalt
        "ADX": "#F39C12",  # Yellow Orange
        "CCI": "#2980B9",  # Belize Hole Blue
        "Willams_%R": "#27AE60",  # Emerald Green
        "Supertrend": "#1F618D",  # Dark Blue
        "ATR": "#C0392B",  # Red
        "EoM": "#8E44AD",  # Purple
        "DMP": "#2ECC71",  # Green
        "DMN": "#D35400",  # Orange
    }

    candle_scope_tech_indicators = st.sidebar.multiselect(label="Technical Indicators:",
                                                  options=candle_scope_talib_indicators,
                                                  key='candle_scope_tech_indicators')




    st.bokeh_chart(create_chart(title, market_trends_data, market_trends_close_price_line, market_trends_open_price_line,
                                market_trends_low_price_line, market_trends_high_price_line, candle_scope_tech_indicators,
                                candle_scope_selected_ticker, candle_scope_indicator_colors), use_container_width=True)

    ## Volume Bars Logic
    if market_trends_volume_line_chart:
        # Eine horizontale zwei Pixel Linie hinzufügen
        draw_line(2)

        # Interaktives Liniendiagramm mit Plotly und Streamlit
        fig = px.line(market_trends_data,
                      x='Datetime',
                      y='Volume')

        # Hintergrund und Layout anpassen
        fig.update_layout(
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),  # Schriftfarbe
            title=dict(
                text=f'Trading volume between {candle_scope_date_from} and {candle_scope_date_to} for {candle_scope_selected_ticker}',
                # Titeltext
                x=0.5,  # Zentriert den Titel
                xanchor='center',  # Verankert den Titel in der Mitte
                font=dict(size=25)  # Schriftgröße des Titels
            )

        )

        # Achsenfarben anpassen
        fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
        fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))

        # Change the line color
        fig.update_traces(line=dict(color='#009999'))

        # Diagramm in Streamlit anzeigen
        st.plotly_chart(fig, use_container_width=True)

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

                market_trends_data.to_excel(rf'{store_location_path}/Stocksdata.xlsx',
                                           sheet_name='Stocks Data',
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

