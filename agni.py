# ==============================================================================
# 🚀 PREDATOR v51.0 : AGNI (THE PULLBACK SNIPER - 750+ STOCKS)
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

# 🔥 THE ULTIMATE UNIVERSE: 750+ Liquid Stocks 
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

print(f" 🚀 AGNI v51.0 : PULLBACK SNIPER INITIALIZED ({len(indian_stocks)} Stocks) ...")
send_telegram_alert(f"🟢 <b>AGNI v51.0 ONLINE (PULLBACK MODE)</b>\n📡 Universe: {len(indian_stocks)} Stocks\n🛡️ Strategy: Buy on Support Bounces")

while True:
    now_ist = datetime.now(ist)
    if now_ist.time() > dtime(15, 30, 0):
        send_telegram_alert("🌙 <b>MARKET CLOSED. SYSTEM SHUTTING DOWN.</b>")
        break

    if now_ist.time() > dtime(15, 15, 0):
        time.sleep(300)
        continue

    # 🔥 9:35 AM Cooling Rule
    if now_ist.time() < dtime(9, 35, 0):
        print(f" ⏳ Cooling off morning volatility... [{now_ist.strftime('%I:%M:%S %p')}]")
        time.sleep(120)
        continue

    print(f"\n ⚡ SCAN STARTED AT : [{now_ist.strftime('%I:%M:%S %p')}] - Hunting Pullbacks...")
    
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
            df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
            df["Vol_SMA20"] = df["Volume"].rolling(20).mean()
            
            today_data = df.loc[df["Date"] == df["Date"].iloc[-1]]
            if len(today_data) < 2: continue
            
            day_high = float(today_data["High"].max())
            prev_close = float(df_daily[s]["Close"].dropna().iloc[-2]) if len(df_daily[s].dropna()) > 1 else float(today_data["Open"].iloc[0])
            
            # -------------------------------------------------------------
            # 🧠 THE PULLBACK BOUNCE LOGIC
            # -------------------------------------------------------------
            stock_pct_change = ((live_c - prev_close) / prev_close) * 100
            
            # 1. स्टॉक आज मजबूत होना चाहिए (Top Gainer list material)
            if stock_pct_change < 1.5: continue 
            
            # 2. पुलबैक चेक (डे-हाई से स्टॉक को 0.8% से 3.5% के बीच गिरा हुआ होना चाहिए)
            dist_from_high = ((day_high - live_c) / day_high) * 100
            if dist_from_high < 0.8 or dist_from_high > 3.5: continue 
            
            live_vwap, ema9_val, ema20_val = float(df["VWAP"].iloc[-1]), float(df["EMA9"].iloc[-1]), float(df["EMA20"].iloc[-1])
            
            # 3. ट्रेंड अभी भी ज़िंदा होना चाहिए (VWAP और 20-EMA के ऊपर)
            if live_c < live_vwap or live_c < ema20_val: continue

            # 4. सपोर्ट पर टच / बाउंस चेक (Curent Low 9-EMA या VWAP के एकदम पास होना चाहिए)
            curr_o = float(today_data["Open"].iloc[-1])
            curr_h = float(today_data["High"].iloc[-1])
            curr_l = float(today_data["Low"].iloc[-1])
            
            near_ema9 = curr_l <= (ema9_val * 1.003)  # 9-EMA के 0.3% दायरे में छुआ हो
            near_vwap = curr_l <= (live_vwap * 1.003) # VWAP के 0.3% दायरे में छुआ हो
            
            if not (near_ema9 or near_vwap): continue # अगर सपोर्ट पर नहीं है, तो रिजेक्ट

            # 5. रिजेक्शन / ग्रीन बाउंस कन्फर्मेशन
            candle_body = abs(curr_o - live_c)
            lower_wick = min(curr_o, live_c) - curr_l
            
            is_green_candle = live_c > curr_o
            good_bottom_rejection = lower_wick > candle_body # नीचे से हथौड़ा (Hammer) बना हो
            
            if not (is_green_candle or good_bottom_rejection): continue # लाल कैंडल पर एंट्री नहीं

            # 6. वॉल्यूम (पुलबैक बाउंस में 10x वॉल्यूम नहीं चाहिए, 1.2x से 4x का RVOL काफी है)
            live_v = float(df["Volume"].iloc[-1])
            avg_vol_20 = float(df["Vol_SMA20"].iloc[-2]) 
            vrr_delta = (live_v / avg_vol_20) if avg_vol_20 > 0 else 0.0
            
            if vrr_delta < 1.0 or vrr_delta > 5.0: continue

            # 🛡️ SL और Targets
            # SL सपोर्ट (VWAP या EMA) के थोड़ा सा नीचे होगा, ना कि करंट प्राइस से
            major_support = min(ema9_val, live_vwap)
            final_sl = major_support * 0.997 # सपोर्ट से 0.3% नीचे
            
            risk_sh = abs(live_c - final_sl)
            if risk_sh <= 0: continue
            
            # अगर SL बहुत बड़ा (2% से ज़्यादा) है, तो ट्रेड इग्नोर करो
            if (risk_sh / live_c) * 100 > 2.0: continue

            qty = max(1, int(BASE_MAX_RISK_BUDGET / risk_sh))
            t1 = live_c + (risk_sh * 1.5)  # Hit & Run Target (1:1.5)
            t2 = live_c + (risk_sh * 3.0)  # Ride Target (1:3)

            stock_sym = s.replace(".NS", "").replace("&", "and")
            
            item_msg = (
                f"🎯 <b>{stock_sym}</b> (PULLBACK BOUNCE)\n"
                f"💰 Entry: ₹{round(live_c, 2)} | 📈 Up: +{stock_pct_change:.2f}%\n"
                f"🔥 Bounce Vol: {round(vrr_delta, 1)}x | 🛡️ SL (Safe): ₹{round(final_sl, 2)}\n"
                f"🎯 T1 (1:1.5): ₹{round(t1, 2)} | 🎯 T2 (1:3.0): ₹{round(t2, 2)}"
            )
            approved_alerts.append(item_msg)
        except: pass

    if len(approved_alerts) > 0:
        final_message = (
            f"🔥 <b>AGNI PULLBACK SNIPER</b> 🔥\n"
            f"<i>(Buying near VWAP/EMA Support)</i>\n"
            f"-------------------------------------\n"
        )
        final_message += "\n\n".join(approved_alerts)
        final_message += f"\n-------------------------------------\n⏰ <b>Time:</b> {now_ist.strftime('%I:%M:%S %p IST')}"
        
        send_telegram_alert(final_message)
    else:
        print(f" ⏳ SCAN COMPLETE. No support bounces found right now. SLEEPING 5 MINS...")
    
    time.sleep(300)
