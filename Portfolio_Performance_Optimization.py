def run_portfolio_performance_optimization(language_index,title):
    import streamlit as st
    import yfinance as yf
    import pandas as pd
    import numpy as np
    from scipy.cluster.hierarchy import linkage, fcluster
    import plotly.express as px
    import plotly.graph_objects as go
    import datetime
    from dateutil.relativedelta import relativedelta
    import Tickers as tic
    from scipy.optimize import minimize
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

    def make_metric(ticker, weight, tickers_count, market_caps):
        distributed_weight = 1 / tickers_count

        market_cap = float(market_caps[market_caps['Ticker'] == ticker]['Market Cap'])
        # st.write(market_cap)

        # Zahl formatieren

        if market_cap >= (1000_000_000_000):  # Billionen
            market_cap = f"{market_cap / 1000_000_000_000:.2f} Bn"

        elif market_cap >= 1_000_000_000:  # Milliarden
            market_cap = f"{market_cap / 1_000_000_000:.2f} Md"


        elif market_cap >= 1_000_000:  # Millionen
            market_cap = f"{market_cap / 1_000_000:.2f} Mio"

        elif market_cap >= 1_000:  # Tausend
            market_cap = f"{market_cap / 1_000:.2f} Tsd"


        else:  # Weniger als Tausend
            market_cap = f"{market_cap:.2f}"

        # st.write(market_cap)

        weight = weight * 100
        distributed_weight = distributed_weight * 100

        if weight > distributed_weight:

            st.markdown(
                f"""
                <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                     <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>{ticker}</h1>
                    <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;'>
                        <span style='color:green; '>
                        <span style='color:green; '>↑ ‎ </span>
                        {weight:.1f} %
                        </span>
                    </h1>
                    <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>{market_cap}</h1>
                </div>
                """, unsafe_allow_html=True
            )
        elif weight == distributed_weight:
            st.markdown(
                f"""
                            <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                                 <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>{ticker}</h1>
                                <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;'>
                                    <span style='color:#FFDF00; '>
                                    <span style='color:#FFDF00; '>↔ ‎ </span>
                                    {weight:.1f} %
                                    </span>
                                </h1>
                                <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>{market_cap}</h1>
                            </div>
                            """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='border: 1px solid black; box-shadow: 0px 0px 25px 3px black; padding: 10px; background-color: #f8f8f8; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                     <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>{ticker}</h1>
                    <h1 style='text-align: center; background-color:#eeeeee; margin: 0; padding: 5px; height: 50%;'>
                        <span style='color:red; '>
                        <span style='color:red; '>↓ ‎ </span>
                        {weight:.1f} %
                        </span>
                    </h1>
                    <h1 style='text-align: center; background-color:#d5d5d5; margin: 0; padding: 5px; height: 50%;'>{market_cap}</h1>
                </div>
                """, unsafe_allow_html=True
            )
        st.write('')
        st.write('')


    def calculate_performance_optimization(data, selected_optimization_method, market_caps=None):

        try:
            if selected_optimization_method == 'Mean-Variance Optimization':
                method_name, weights_df = mean_variance_optimization(data)

            if selected_optimization_method == 'Minimum Variance Portfolio':
                method_name, weights_df = minimum_variance_portfolio(data)

            if selected_optimization_method == 'Maximum Sharpe Ratio Portfolio':
                method_name, weights_df = maximum_sharpe_ratio(data)



            if selected_optimization_method == 'Risk Parity Portfolio':
                method_name, weights_df = risk_parity_portfolio(data)


            if selected_optimization_method == 'Black-Litterman Model Portfolio':
                method_name, weights_df = black_litterman_portfolio(data, market_caps)

            if selected_optimization_method == 'Hierarchical Risk Parity Portfolio':
                method_name, weights_df = hierarchical_risk_parity_portfolio(data)


        except Exception as e:
            method_name, weights_df = '', pd.DataFrame(columns=['Ticker', 'Weight'])

        return method_name, weights_df

    def create_pie_chart(data):
        # Erstellen des Kreisdiagramms mit Plotly
        fig = px.pie(data, values='Weight', names='Ticker',
                     title='Verteilung der Gewichte in %',
                     color_discrete_sequence=px.colors.sequential.RdBu,
                     hole=0.3)  # Optional für einen Donut-Style

        # Layout des Diagramms anpassen (Titel zentrieren)
        fig.update_layout(
            height=600,  # Höhe des Diagramms
            title={
                'text': 'Verteilung der Gewichte in %',
                'x': 0.5,  # Zentrieren des Titels (x=0.5 bedeutet mittig)
                'xanchor': 'center',
                'yanchor': 'top'
            },
            title_font_size=24,  # Titelgröße
            plot_bgcolor='#eeeeee',  # Hintergrundfarbe des Plots
            paper_bgcolor='#d5d5d5',  # Hintergrundfarbe der gesamten Figur
            font=dict(color='#009999'),
            margin=dict(l=50, r=50, t=100, b=50)  # Ränder anpassen
        )

        # Darstellung des Diagramms mit Streamlit
        st.plotly_chart(fig, use_container_width=True)



    # Daten abrufen
    def portfolio_performacne_fetch_data(tickers, start_date, end_date):
        try:


            data = yf.download(tickers,
                               start=start_date,
                               end=end_date,
                               interval='1d')['Close']

            return data
        except:
            st.warning('Bitte andere Daten wählen')
            data = pd.DataFrame({'Date': [None],
                                 'None1': [None],
                                 'None2': [None]})

            return data

    # Marktkapitalisierung für Aktien
    def get_market_caps_stocks(tickers):
        market_caps = {}
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            # Holen Sie die Marktkapitalisierung direkt ab und konvertieren Sie sie in einen float
            market_cap = stock.info.get("marketCap")

            # Überprüfen, ob die Marktkapitalisierung vorhanden ist und in eine Zahl konvertierbar ist
            if market_cap is not None:
                try:
                    market_caps[ticker] = float(market_cap)  # In float konvertieren
                except ValueError:
                    pass

        # Rückgabe als DataFrame für bessere Übersicht
        market_caps_df = pd.DataFrame(list(market_caps.items()), columns=["Ticker", "Market Cap"])
        return market_caps_df







    # Mean-Variance Optimization
    def mean_variance_optimization(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        cov_matrix = returns.cov()
        avg_returns = returns.mean()
        num_assets = len(avg_returns)

        def portfolio_volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
        bounds = [(0, 1) for _ in range(num_assets)]
        initial_weights = np.array([1 / num_assets] * num_assets)

        result = minimize(portfolio_volatility, initial_weights, bounds=bounds, constraints=constraints)
        weights = result.x
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Mean-Variance Optimization", weight_df

    # Minimum Variance Portfolio
    def minimum_variance_portfolio(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        cov_matrix = returns.cov()
        num_assets = len(cov_matrix)

        def portfolio_volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
        bounds = [(0, 1) for _ in range(num_assets)]
        initial_weights = np.array([1 / num_assets] * num_assets)

        result = minimize(portfolio_volatility, initial_weights, bounds=bounds, constraints=constraints)
        weights = result.x
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Minimum Variance Portfolio", weight_df

    # Maximum Sharpe Ratio Portfolio
    def maximum_sharpe_ratio(df, risk_free_rate=0.01):
        # Berechnung der täglichen Renditen
        returns = df.iloc[:, 1:].pct_change().dropna()
        cov_matrix = returns.cov()
        avg_returns = returns.mean()
        num_assets = len(avg_returns)

        # Zielfunktion: Negative Sharpe Ratio
        def negative_sharpe_ratio(weights):
            portfolio_return = np.dot(weights, avg_returns)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            return -(portfolio_return - risk_free_rate) / portfolio_volatility

        # Constraints: Summe der Gewichte = 1
        constraints = [{'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}]

        # Zusatz: Mindestgewicht für Diversifikation
        min_weight = 0  # Mindestens 5% Gewicht pro Asset
        max_weight = 1  # Maximal 50% Gewicht pro Asset
        bounds = [(min_weight, max_weight) for _ in range(num_assets)]

        # Startwerte: Gleichgewichtetes Portfolio
        initial_weights = np.array([1 / num_assets] * num_assets)

        # Optimierung
        result = minimize(
            negative_sharpe_ratio,
            initial_weights,
            bounds=bounds,
            constraints=constraints
        )

        # Überprüfung, ob die Optimierung erfolgreich war
        if not result.success:
            raise ValueError("The optimization has failed: " + result.message)

        # Ergebnis: Gewichte der Assets
        weights = result.x

        # Ausgabe als DataFrame
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Maximum Sharpe Ratio Portfolio", weight_df


    # Risk Parity Portfolio
    def risk_parity_portfolio(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        cov_matrix = returns.cov()
        inv_volatility = 1 / np.sqrt(np.diag(cov_matrix))
        weights = inv_volatility / np.sum(inv_volatility)
        weight_df = pd.DataFrame({'Ticker': df.columns[1:], 'Weight': weights})

        return "Risk Parity Portfolio", weight_df






    # Black-Litterman Model Portfolio
    def black_litterman_portfolio(df, market_capitalizations, tau=0.025):
        # Berechnung der historischen Renditen (Änderungen über die Zeit für jede Spalte außer Datum)
        returns = df.iloc[:, 1:].pct_change().dropna()
        avg_returns = returns.mean()

        # Sicherstellen, dass die Ticker aus 'df' und 'market_capitalizations' übereinstimmen
        tickers = df.columns[1:]
        market_capitalizations = market_capitalizations.set_index('Ticker')

        # Überprüfen, ob die Tickers in beiden DataFrames übereinstimmen und ordnen
        market_caps = market_capitalizations.reindex(tickers)['Market Cap']

        # Fehlende Werte abfangen
        if market_caps.isnull().any():
            missing_tickers = market_caps[market_caps.isnull()].index.tolist()
            raise ValueError(f"Market capitalizations are missing for the following ticker: {missing_tickers}")

        # Normalisierung der Gewichte aus den Marktkapitalisierungen
        weights = market_caps.values / market_caps.sum()

        # Black-Litterman-Anpassung der erwarteten Renditen
        adjusted_returns = tau * avg_returns + (1 - tau) * weights
        weights = adjusted_returns / adjusted_returns.sum()

        # Ausgabe der Gewichtungen als DataFrame
        weight_df = pd.DataFrame({'Ticker': tickers, 'Weight': weights})

        return "Black-Litterman Model Portfolio", weight_df

    # Hierarchical Risk Parity (HRP) Portfolio
    def hierarchical_risk_parity_portfolio(df):
        returns = df.iloc[:, 1:].pct_change().dropna()
        corr_matrix = returns.corr()
        distances = np.sqrt((1 - corr_matrix) / 2)
        clusters = linkage(distances, method='ward')
        tickers = df.columns[1:]
        cluster_assignments = fcluster(clusters, t=1.5, criterion='distance')
        unique_clusters = np.unique(cluster_assignments)
        weights = np.zeros(len(tickers))
        for cluster in unique_clusters:
            cluster_indices = np.where(cluster_assignments == cluster)[0]
            equal_weight = 1 / len(cluster_indices)
            weights[cluster_indices] = equal_weight
        weights /= weights.sum()
        weight_df = pd.DataFrame({'Ticker': tickers, 'Weight': weights})

        return "Hierarchical Risk Parity Portfolio", weight_df

    # Logo sidebar
    st.sidebar.image("Images/Logo.png",
                     use_column_width=True)

    # Draw Line for the sidebar (3 Pixel)
    draw_line_sidebar(3)

    portfolio_performance_optimization_countries_options = ['USA', 'China', 'Germany', 'Japan', 'United Kingdom']

    # Tickers importieren
    tickers_portfolio_performance_optimization = []
    for country in portfolio_performance_optimization_countries_options:

        tickers, big_four_tickers = tic.run_tickers(country=country)

        # Einfachauswahl für Ticker
        tickers_portfolio_performance_optimization_selection = st.sidebar.multiselect(f'{country}-Tickers:',
                                                                            options=tickers,
                                                                            key=f'tickers_portfolio_performance_optimization_{country}',
                                                                            default=big_four_tickers)
        tickers_portfolio_performance_optimization = tickers_portfolio_performance_optimization + tickers_portfolio_performance_optimization_selection


    # st.write(market_caps)
    performance_optimization_date_from_col, performance_optimization_date_to_col = st.sidebar.columns(2)


    today = datetime.datetime.today().date()

    today_minus_one_year = today - relativedelta(years=1)
    with performance_optimization_date_from_col:
        performance_optimization_date_from = st.date_input(label='Date (From)',
                                                           value=today_minus_one_year,
                                                           key='performance_optimization_date_from')

    performance_optimization_date_from_plus_one_minute = performance_optimization_date_from + relativedelta(minutes=1)

    with performance_optimization_date_to_col:
        performance_optimization_date_to = st.date_input(label='Date (To)',
                                                         value=today,
                                                         min_value=performance_optimization_date_from_plus_one_minute,
                                                         max_value=today,
                                                         key='performance_optimization_date_to')

    # Liste der Methodennamen
    optimization_method_names = [
        "Mean-Variance Optimization",
        "Minimum Variance Portfolio",
        "Maximum Sharpe Ratio Portfolio",
        "Risk Parity Portfolio",
        "Black-Litterman Model Portfolio",
        "Hierarchical Risk Parity Portfolio"
    ]

    selected_optimization_method = st.sidebar.selectbox('Optimaziation-Method:',
                                                        options=optimization_method_names,
                                                        key='selected_optimization_method')


    # Marktkapital Aktien

    market_caps = get_market_caps_stocks(tickers_portfolio_performance_optimization)



    # Foto Sidebar Stocks API
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')
    st.sidebar.write('')

    # Page Title
    Centred_Title.run_centred_title(title+' ('+selected_optimization_method+')')



    data = portfolio_performacne_fetch_data(tickers_portfolio_performance_optimization,
                                            performance_optimization_date_from,
                                            performance_optimization_date_to)

    data = data.reset_index()







    # Calculate Perofrmance Optimization

    result_text, result_df = calculate_performance_optimization(data=data,
                                                                selected_optimization_method=selected_optimization_method,
                                                                market_caps=market_caps)

    # st.write(result_df)
    # Index-Spalte umbennen (index -> Ticker)
    result_df = result_df.rename(columns={'index': 'Ticker'})

    # Ergebnis nach Gewichten absteigend sortieren
    result_df = result_df.sort_values(by='Weight',
                                      ascending=False)



    create_pie_chart(result_df)
    tickers_count = len(result_df['Ticker'].values)

    # Eine horizontale zwei Pixel Linie hinzufügen
    draw_line(2)

    ticker_weight_col_one, ticker_weight_col_two, ticker_weight_col_three, ticker_weight_col_four = st.columns(4)

    with ticker_weight_col_one:
        iteration = 1

        for ticker in result_df['Ticker']:

            weight = float(result_df[result_df['Ticker'] == ticker]['Weight'].values)

            if iteration % 4 == 1:
                make_metric(ticker, weight, tickers_count, market_caps)
            iteration += 1

    with ticker_weight_col_two:
        iteration = 1
        for ticker in result_df['Ticker']:

            weight = float(result_df[result_df['Ticker'] == ticker]['Weight'].values)

            if iteration % 4 == 2:
                make_metric(ticker, weight, tickers_count, market_caps)
            iteration += 1

    with ticker_weight_col_three:
        iteration = 1
        for ticker in result_df['Ticker']:
            weight = float(result_df[result_df['Ticker'] == ticker]['Weight'].values)
            if iteration % 4 == 3:
                make_metric(ticker, weight, tickers_count, market_caps)
            iteration += 1

    with ticker_weight_col_four:
        iteration = 1
        for ticker in result_df['Ticker']:
            weight = float(result_df[result_df['Ticker'] == ticker]['Weight'].values)
            if iteration % 4 != 1 and iteration % 4 != 2 and iteration % 4 != 3:
                make_metric(ticker, weight, tickers_count, market_caps)
            iteration += 1

    # Eine horizontale drei Pixel Linie hinzufügen
    draw_line(3)

    # Footer importieren
    ft.run_footer(language_index=language_index)


