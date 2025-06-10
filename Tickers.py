def run_tickers(country):
    # Liste der Tickers
    tickers = []
    big_one_ticker = []


    # USA
    if country == 'USA':
        tickers = [
                "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK-B", "UNH", "V",
                "JNJ", "HD", "PYPL", "DIS", "INTC", "CSCO", "NFLX", "PFE", "MA", "KO", "PEP",
                "MRK", "CRM", "BA", "MCD", "NVAX", "WMT"
            ]
        big_one_ticker = [ "AAPL"]

    # China
    elif country == 'China':
        tickers = [
            "BABA", "TCEHY", "JD", "PDD", "NTES", "MELI", "KWEB", "BIDU", "IQ", "XPEV",
            "LI", "NIO", "BABA", "ZTO", "TAL", "NTEC", "HUYA", "BAIDU", "PDD", "STNE",
            "PINGD", "AMZN", "SE", "LK", "HNP", "ZNH"
        ]
        big_one_ticker = ["BABA"]

    # Germany
    elif country == 'Germany':
        tickers = [
        "SAP.DE","SIE.DE", "BMW.DE", "DTE.DE", "LHA.DE", "SIE.DE", "VOW3.DE", "ALV.DE", "BAS.DE", "DAI.DE", "RWE.DE",
        "MTX.DE", "ADS.DE", "DBK.DE", "EOAN.DE", "MUV2.DE", "ZAL.DE", "IFX.DE", "FRE.DE", "BAYN.DE", "HEI.DE",
        "LGS.DE", "CON.DE", "MBG.DE", "FNTN.DE", "CTS.DE", "HLAG.DE",'DBK.DE','CBK.DE'
        ]
        big_one_ticker = ["SAP.DE"]

    # Japan
    elif country == 'Japan':
        tickers = [
            "7203.T", "6758.T", "9984.T", "9432.T", "8306.T", "6971.T", "6367.T", "8058.T",
            "9983.T", "7751.T", "7011.T", "9735.T", "4063.T", "6594.T", "7201.T", "4901.T",
            "7733.T", "8267.T", "7202.T", "9433.T", "6501.T", "9001.T", "8028.T", "6503.T",
            "6752.T"
        ]
        big_one_ticker = ["7203.T"]

    # UK
    elif country == 'United Kingdom':
        tickers = [
                "TSCO.L", "HSBC", "RDSB.L", "GSK.L", "VOD.L", "LLOY.L", "BP.L", "BATS.L",
                "SHEL.L", "RBS.L", "AAL.L", "AZN.L", "BA.L", "ITV.L", "GLEN.L", "MNG.L",
                "PRU.L", "JMAT.L", "CRH.L", "LSEG.L", "RIO.L", "NXT.L", "ULVR.L", "DGE.L",
                "RMG.L", "BARC.L"
            ]
        big_one_ticker = ["TSCO.L"]

    return tickers,big_one_ticker