# ==============================================================================
# 🚀 PREDATOR v48.0 : AGNI (TRUE INSTITUTIONAL VOLUME + ANTI-TRAP GUARDS)
# ==============================================================================
import logging, os, sys, warnings, urllib.request, json, time
from datetime import datetime, time as dtime
import pandas as pd, pytz, yfinance as yf

warnings.filterwarnings("ignore")
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ist = pytz.timezone("Asia/Kolkata")

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN.strip()}/sendMessage"
    payload = {"chat_id": str(TELEGRAM_CHAT_ID).strip(), "text": message, "parse_mode": "HTML"}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=20) as response:
                if response.status == 200: return 
        except Exception: time.sleep(2)

BASE_MAX_RISK_BUDGET = 180.0

# 🔥 THE ULTIMATE UNIVERSE: 750+ Stocks 
raw_tickers = """
RELIANCE TCS HDFCBANK ICICIBANK INFY SBI ITC BHARTIARTL HINDUNILVR L&T BAJFINANCE HCLTECH KOTAKBANK AXISBANK ADANIENT 
ASIANPAINT MARUTI SUNPHARMA TATASTEEL TITAN ULTRACEMCO ONGC TATAMOTORS NTPC POWERGRID NESTLEIND M&M WRO ADANIPORTS 
BAJAJFINSV JSWSTEEL HINDALCO COALINDIA TECHM GRASIM TATACHEM CIPLA DIVISLAB SBILIFE DRREDDY APOLLOHOSP HDFCLIFE EICHERMOT 
BRITANNIA TATACONSUM INDUSINDBK BAJAJ-AUTO HEROMOTOCO UPL BPCL HAL BEL MAZDOCK COCHINSHIP RVNL IRFC ZOMATO PAYTM NYKAA 
POLICYBKR TRENT INDHOTEL JUBLFOOD DIXON POLYCAB KALYANKJIL SUZLON NAVINFLUOR DEEPAKNTR SRF AWL VOLTAS SIEMENS ABB BHEL 
PFC RECLTD JIOFIN ADANIGREEN AMBUJACEM ZYDUSLIFE CHENNPETRO ROLEXRINGS MRPL BSE MCX CDSL ANGELONE LUPIN AUROPHARMA ALKEM 
TORNTPHARM BIOCON GLENMARK LAURUSLABS SYNGENE GRANULES LALPATHLAB IPCALAB PEL NATCOPHARM AJANTPHARM JBCHEPHARM SANOFI 
ABBOTINDIA PFIZER GLAXO MANKIND MEDPLUS FORTIS STARHEALTH METROPOLIS THYROCARE ASHOKLEY SONACOMS BOSCHLTD MRF BALKRISIND 
APOLLOTYRE MOTHERSON EXIDEIND ESCORTS BHARATFORG TIINDIA AMARAJABAT CEATLTD MINDAIND UNO-MINDA ENDURANCE CRAFTSMAN JAMNAAUTO 
SUNDRMFAST GABRIEL OLECTRA TATAPOWER JSWENERGY GAIL HINDPETRO IOC PETRONET IGL MGL GUJGASLTD OIL CASTROLIND SJVN NHPC 
TORNTPOWER CESC PTC GODREJCP DABUR MARICO COLPAL UBL MCDOWELL-N PAGEIND BATAINDIA RADICO BALRAMCHIN VARROC VBL EMAMILTD 
PROCTER GILLETTE WHIRLPOOL TTKPRESTIG SYMPHONY EUREKAFORBE CAMPUS METROBRAND RELAXO MANYAVAR BLUESTONE BDL IRCON TITAGARH 
TEXRAIL ASTRAMICRO MTARTECH BEML GRSE DLF GODREJPROP OBEROIRLTY PRESTIGE MACROTECH LODHA SOBHA BRIGADE PHOENIXLTD IBREALEST 
SUNTECK PURVA MAHLIFE GRASIM GMRINFRA IRB PNCINFRA KNRCON NCC HGINFRA ASHOKA JWL RITES ENGINERSIN NBCC HUDCO JKCEMENT 
RAMCOCEM PIIND AARTIIND GUJALKALI ATUL COROMANDEL CHAMBLFERT GNFC GSFC FACT RCF ALKYLAMINE BALAMINES CLEAN FINEORG 
VINATIORGA NEOGEN JUBILANT SUDARSCHEM SUMICHEM ASTEC SHARDACROP BHARATRAS BASF BODALCHEM MEGH PARADEEP NMDC NATIONALUM 
SAIL JINDALSTEL APLAPOLLO HZL RATNAMANI WELCORP JSL JSLHISAR HINDCOPPER HINDZINC MUKANDLTD MOIL GMDC UML SHYAMMETL GRAVITA 
SUNTV ZEEL PVRINOX DEVYANI SAPPHIRE WESTLIFE CHALET LEMONTREE CERA KAYNES SYRMA TRIDENT WELSPUNIND KPRMILL RAYMOND SWIGGY 
INDIGO BLUEDART DELHIVERY EASEMYTRIP IRCTC SHREECEM ACC DALBHARAT CUMMINSIND KEI HAVELLS CROMPTON ASTRAL FINCABLES VGUARD 
APARINDS CGPOWER HITACHI THERMAX HONAUT TRIVENI EIAHAHOTELS 3MINDIA AIAENG AUBANK AAVAS ATGL ABCAPITAL ABFRL AEGISCHEM 
AETHER AFFLE APLLTD ALLCARGO ANANDRATHI ANUPAM APTUS ARAMCO ASTERDM ASTRAZEN AVANTIFEED DMART BANKINDIA MAHABANK BAYERCROP 
BERGEPAINT BIRLACORPN BSOFT BLUESTARCO BOMBAYDYEING CRISIL CSBBANK CANFINHOME CANBK CAPLIPOINT CENTRALBK CENTURYPLY CENTURYTEX 
CHOLAHLD CAMS CONCOR CREDITACC CUB CYIENT DCBBANK DCMSHRIRAM EIDPARRY EIHOTEL EPL ELECON ELGIEQUIP EQUITASBNK ERIS FEDERALBNK 
FINPIPE GRINFRA GMMPFAUDLER GALAXYSURF GARFIBRES GICRE GLAND GOCOLORS GODFRYPHLP GODREJAGRO GODREJIND GRINDWELL GRAPHITE 
GESHIP GAEL GSPL HEG HDFCAMC HFCL HLEGLAS HLVLTD HUDCO ICICIGI ICICIPRULI ISEC IDBI IDFCFIRSTB IDFC IFBIND IFCI IIFL IEX 
INDIAMART INDIANHOTEL INDIGOPNTS NAUKRI INFIBEAM INOXWIND INTELLECT IOBC IPCA ITI J&KBANK JKLAKSHMI JKPAPER JKTYRE JAMNAAUTO 
JUBLPHARMA KANSAINER KARURVYSYA KPITTECH KRBL KFINTECH L&TFH LT LTI LTIM LTTS LICHSGFIN LAOPALA LIC LICI LINDEINDIA LLOYDSME 
LUXIND MMTC MACROTECH M&MFIN MAHLIFE MAJESCO MANAPPURAM MASTEK MFSL MAXHEALTH MEDANTA MFL MINDACORP MOTILALOFS MPHASIS 
MUTHOOTFIN NATCOPHARM NETWORK18 NEWGEN NAM-INDIA NIPPON OBEDIENT OBEROIRLTY ORIENTELEC PNB PATANJALI PERSISTENT PHOENIXLTD 
PIDILITIND POLYMED POONAWALLA PRSMJOHNSN PRIVISCL QUESS RRKABEL RAILTEL RAIN RAJESHEXPO REDINGTON RBA ROUTE SBICARD SCHAEFFLER 
SHOOPERS SHRIRAMFIN SKFINDIA SONATSOFTW SOUTHBANK SPARC STLTECH SUNDARMFIN SUPRAJIT SUPREMEIND SWSOLAR SWANENERGY SYNGENE 
TCI TTKPRESTIG TANLA TATACOMM TATAELXSI TATAINVEST TEJASNET TIMKEN TRIVENIGQ TUBEINVEST UCOBANK UFLEX UNO-MINDA UJJIVANSFB 
UNIONBANK UTIAMC VIPIND VAIBHAVGBL VAKRANGEE VIJAYA WONDERLA YESBANK ZEELEARN ZENSARTECH ZYDUSWELL AHLUCONT AHLWEST ALOKINDS 
BAJAJCON BALMLAWRIE BECTORFOOD BBOX BURGERKING CIGNITITEC COFFEEDAY DEN DBREALTY DISHTV DREDGECORP EDELWEISS EMUDHRA ENIL 
EPIGIGRAM EQUITAS EVERESTIND FILATEX GALLANTT GATI GENUSPOWER GOCLCORP GREENPANEL GREENPLY HCC HIKAL HIL HINDWARE HSCL IBREALEST 
IFB INDOCO INOXGREEN IONEXCHANG ISGEC JAGRAN JAICORP JTEKTINDIA JUBILANT KAMATHOTEL KCP KIRIINDUS KOPRAN KSL LINC LOKESHMACH 
LUMAXIND MANALIPETC MARATHON MARKSANS MATRIMONY MAXIND MAYURUNIQ MOLDTKPAC MONTECARLO MOREPENLAB MPSLTD MUKTAARTS MUNJALAU 
MUNJALSHOW NAZAARA NCLIND NECLIFE NELCAST NELCO NESCO NILKAMAL NIPPOBATRY NITINSPIN NRBBEARING NUCLEUS OASIS OMAXAUTO OMAXE 
ONMOBILE OPTIEMUS ORIENTABRA ORIENTBELL ORIENTCEM ORIENTHOT PANAMAPET PANACEABIO PAPERPROD PARABDRUGS PARAGMILK PARSVNATH 
PATELENG PCJEWELLER PENIND PENINLAND PETRONENG PGHL PIONDIST PNBGILTS PNBHOUSING POCL PODDARHOUS POLYPLEX PONNIERODE PRAKASH 
PRAKASHSTL PRECAM PREMIER PRICOL PRIMESECU PROZONINTU PTL PUNJABCHEM PURVA QUICKHEAL RADIOCITY RAMASTEEL RAMCOIND RAMCOSYS 
RANEENGINE RANEMADRAS RBLBANK RELIGARE REPCOHOME REPRO RESPONSIND REVATHI RICOAUTO RKFORGE RMCL RML RNAM ROLTA ROSSELLIND 
RPGNIFES RPOWER RTNPOWER RUPA RUSHIL SREINFRA SREINTFIN SRHHYPOLTD SHRIRAMCIT SHYAMCENT SHYAMTEL SIGIND SIL SILINV SILLYMONKS 
SIMBHALS SIMPLEXINF SINTEX SIRCA SIS SKMEGGPROD SMARTLINK SMCGLOBAL SMLISUZU SMPL SMSLIFE SMSPHARMA SNOWMAN SOMANYCERA SOMATEX 
SORILINFRA SPAL SPANDANA SPECIALITY SPENCERS SPIC SPLIL SPMICRO SPMLINFRA SPORTKING SREEL SRICTA SRIRAM SRTRANSFIN SSWL STAMPEDE 
STAR STARPAPER STCINDIA STEELCITY STEELXIND STEL STERTOOLS SUBEX SUBROS SUMIT SUNCLAYLTD SUNFLAG SUPERHOUSE SUPERSPIN SUPREMEENG 
SURANASOL SURANAT&P SURLA SURYALAXMI SURYAROSNI SUTLEJTEX SUVEN SUVENPHAR SUVIDHAA SUYOG SWARAJENG SWELECTES SYNCOM TAINWALCHM 
TAJGVK TAKE TALBROAUTO TALENTER TALLY TARMAT TASTYBITE TATACOFFEE TATAMETALI TATASTLLP TBZ TCIEXP TCNSBRANDS TCPLPACK TDPOWERSYS 
TEAMLEASE TECHIN TECHNOE TERASOFT TEXINFRA TFCILTD TFL TGBHOTELS THANGAMAYL THEINVEST THEMISMED THIRUSUGAR THOMASCOOK TI 
TIDEWATER TIIL TIMESGTY TIMETECHNO TINPLATE TIPSINDLTD TIRUMALCHM TMRVL TNPL TOKYOPLAST TOTAL TOUCHWOOD TPLPLASTEH TREEHOUSE 
TREJHARA TRF TRIGYN TRIL TRITURBINE TTKHLTHCARE TTL TV18BRDCST TVSSELECT
"""
indian_stocks = sorted(list(set([f"{t.strip()}.NS" for t in raw_tickers.split() if t.strip()])))

print(f" 🚀 AGNI v48.0 : INSTITUTIONAL VOLUME SCANNER INITIALIZED ({len(indian_stocks)} Stocks) ...")
send_telegram_alert(f"🟢 <b>AGNI v48.0 ONLINE</b>\n📡 Scanning: {len(indian_stocks)} Stocks\n🛡️ Strict RVOL (Average Volume) Filter Active")

while True:
    now_ist = datetime.now(ist)
    if now_ist.time() > dtime(15, 30, 0):
        send_telegram_alert("🌙 <b>MARKET CLOSED. SYSTEM SHUTTING DOWN.</b>")
        break

    if now_ist.time() > dtime(15, 15, 0):
        print(f" ⏳ No new trades after 3:15 PM. Just keeping server alive... [{now_ist.strftime('%I:%M:%S %p')}]")
        time.sleep(300)
        continue

    print(f"\n ⚡ SCAN STARTED AT : [{now_ist.strftime('%I:%M:%S %p')}] - Fetching Data...")
    
    try:
        df_daily = yf.download(indian_stocks + ["^NSEI"], period="5d", interval="1d", group_by="ticker", threads=True, progress=False)
        df_5m = yf.download(indian_stocks + ["^NSEI"], period="5d", interval="5m", group_by="ticker", threads=True, progress=False)
    except Exception as e:
        time.sleep(60)
        continue

    approved_alerts = []

    for s in indian_stocks:
        try:
            if s not in df_5m.columns.levels[0]: continue
            df = df_5m[s].dropna()
            live_c = float(df["Close"].iloc[-1])
            if live_c < 30.0: continue 

            df["Typ"] = (df["High"] + df["Low"] + df["Close"]) / 3
            df["Date"] = df.index.date
            df["VWAP"] = df.groupby("Date").apply(lambda x: (x["Typ"] * x["Volume"]).cumsum() / x["Volume"].cumsum()).reset_index(level=0, drop=True)
            df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
            
            # 🔥 NEW: 20-Period Volume Average (RVOL Baseline)
            df["Vol_SMA20"] = df["Volume"].rolling(20).mean()
            
            today_data = df.loc[df["Date"] == df["Date"].iloc[-1]]
            if len(today_data) < 2: continue
            
            day_high = float(today_data["High"].max())
            prev_close = float(df_daily[s]["Close"].dropna().iloc[-2]) if len(df_daily[s].dropna()) > 1 else float(today_data["Open"].iloc[0])
            stock_pct_change = ((live_c - prev_close) / prev_close) * 100
            
            live_vwap, ema9_val = float(df["VWAP"].iloc[-1]), float(df["EMA9"].iloc[-1])
            live_v = float(df["Volume"].iloc[-1])
            
            # 🛡️ FIX: Calculating Volume Multiplier against the 20-candle AVERAGE, not just the last candle
            avg_vol_20 = float(df["Vol_SMA20"].iloc[-2]) 
            vrr_delta = (live_v / avg_vol_20) if avg_vol_20 > 0 else 0.0

            # -------------------------------------------------------------
            # 🛡️ THE ANTI-TRAP GUARDS (OHLC DATA)
            # -------------------------------------------------------------
            curr_o = float(today_data["Open"].iloc[-1])
            curr_h = float(today_data["High"].iloc[-1])
            curr_l = float(today_data["Low"].iloc[-1])
            candle_height = curr_h - curr_l

            if candle_height > 0:
                upper_wick_pct = (curr_h - max(curr_o, live_c)) / candle_height
                close_pct = ((live_c - curr_l) / candle_height) * 100
                current_candle_size_pct = (candle_height / curr_l) * 100
            else:
                upper_wick_pct, close_pct, current_candle_size_pct = 0, 50.0, 0

            # 🚫 GUARD 1: ANTI-FOMO (अगर 1 ही कैंडल में 2.5% से ज्यादा भागा है, तो रिजेक्ट)
            if current_candle_size_pct > 2.5: continue

            # 🚫 GUARD 2: WICK REJECTION (अगर कैंडल में ऊपर 35% से बड़ी पूंछ है, तो रिजेक्ट)
            if upper_wick_pct > 0.35: continue

            # 🚫 GUARD 3: STRONG CLOSE (कैंडल को अपने टॉप 40% हिस्से में बंद होना ज़रूरी है)
            if close_pct < 60.0: continue

            # 🚫 GUARD 4: RVOL REJECTION (अब वॉल्यूम 20-कैंडल एवरेज से कम से कम 3x ज़्यादा होना चाहिए)
            if vrr_delta < 3.0 or vrr_delta > 15.0: continue

            # -------------------------------------------------------------
            # 🚀 BASE LOGIC
            # -------------------------------------------------------------
            if stock_pct_change < 2.0: continue 
            if live_c < live_vwap or live_c < ema9_val: continue
            
            distance_from_high = ((day_high - live_c) / day_high) * 100
            if distance_from_high > 1.2: continue 

            final_sl = ema9_val * 0.998 
            risk_sh = abs(live_c - final_sl)
            
            if risk_sh <= 0: continue
            qty = max(1, int(BASE_MAX_RISK_BUDGET / risk_sh))
            
            t1 = live_c + (risk_sh * 2.0)
            t2 = live_c + (risk_sh * 4.0)

            stock_sym = s.replace(".NS", "").replace("&", "and")
            
            item_msg = (
                f"🚀 <b>{stock_sym}</b> (INSTITUTIONAL BREAKOUT)\n"
                f"💰 CMP: ₹{round(live_c, 2)} | 📈 Up: +{stock_pct_change:.2f}%\n"
                f"🔥 True Vol (RVOL): {round(vrr_delta, 1)}x | 🛡️ SL (9-EMA): ₹{round(final_sl, 2)}\n"
                f"🎯 T1 (1:2): ₹{round(t1, 2)} | 🎯 T2 (1:4): ₹{round(t2, 2)}"
            )
            approved_alerts.append(item_msg)
        except: pass

    if len(approved_alerts) > 0:
        final_message = (
            f"🔥 <b>AGNI MAX SCANNER (Safe Mode)</b> 🔥\n"
            f"<i>(Filtered Fake Spikes using True RVOL)</i>\n"
            f"-------------------------------------\n"
        )
        final_message += "\n\n".join(approved_alerts)
        final_message += f"\n-------------------------------------\n⏰ <b>Time:</b> {now_ist.strftime('%I:%M:%S %p IST')}"
        
        send_telegram_alert(final_message)
    else:
        print(f" ⏳ SCAN COMPLETE. Traps avoided. No safe rockets found. SLEEPING 5 MINS...")
    
    time.sleep(300)
