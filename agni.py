# ==============================================================================
# 🚀 PREDATOR v44.0 : AGNI (NIFTY 500 UNIVERSE + ROCKET CATCHER)
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

# 🔥 THE BEAST UNIVERSE: Nifty 500 + Top Mid/Small Caps (500+ Stocks)
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
APARINDS CGPOWER HITACHI THERMAX HONAUT TRIVENI EIAHAHOTELS
"""
indian_stocks = sorted(list(set([f"{t.strip()}.NS" for t in raw_tickers.split() if t.strip()])))

print(f" 🚀 AGNI v44.0 : NIFTY 500 BEAST SCANNER INITIALIZED ({len(indian_stocks)} Stocks) ...")
send_telegram_alert(f"🟢 <b>AGNI v44.0 ONLINE</b>\n📡 Scanning Maximum Universe: {len(indian_stocks)} Stocks")

while True:
    now_ist = datetime.now(ist)
    if now_ist.time() > dtime(15, 30, 0):
        send_telegram_alert("🌙 <b>MARKET CLOSED. SYSTEM SHUTTING DOWN.</b>")
        break

    print(f"\n ⚡ SCAN STARTED AT : [{now_ist.strftime('%I:%M:%S %p')}]")
    
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
            if live_c < 30.0: continue # 30 रुपये से नीचे के पेनी स्टॉक्स इग्नोर

            df["Typ"] = (df["High"] + df["Low"] + df["Close"]) / 3
            df["Date"] = df.index.date
            df["VWAP"] = df.groupby("Date").apply(lambda x: (x["Typ"] * x["Volume"]).cumsum() / x["Volume"].cumsum()).reset_index(level=0, drop=True)
            df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
            
            today_data = df.loc[df["Date"] == df["Date"].iloc[-1]]
            if len(today_data) < 2: continue
            
            day_high = float(today_data["High"].max())
            prev_close = float(df_daily[s]["Close"].dropna().iloc[-2]) if len(df_daily[s].dropna()) > 1 else float(today_data["Open"].iloc[0])
            
            stock_pct_change = ((live_c - prev_close) / prev_close) * 100
            
            live_vwap, ema9_val = float(df["VWAP"].iloc[-1]), float(df["EMA9"].iloc[-1])
            live_v, prev_v = float(df["Volume"].iloc[-1]), float(df["Volume"].iloc[-2])
            vrr_delta = (live_v / prev_v) if prev_v > 0 else 1.0

            # 🔥 RULE 1: सिर्फ टॉप गेनर्स (कम से कम 2.5% ऊपर होना चाहिए)
            if stock_pct_change < 2.5: continue

            # 🔥 RULE 2: स्ट्रॉन्ग अपट्रेंड (VWAP और 9-EMA के ऊपर)
            if live_c < live_vwap or live_c < ema9_val: continue

            # 🔥 RULE 3: डे-हाई के पास (High से 1.2% से ज्यादा नहीं गिरना चाहिए)
            distance_from_high = ((day_high - live_c) / day_high) * 100
            if distance_from_high > 1.2: continue 

            # 🔥 RULE 4: वॉल्यूम ब्लास्ट
            if vrr_delta < 2.5: continue

            # SL और Targets
            final_sl = ema9_val * 0.998 
            risk_sh = abs(live_c - final_sl)
            
            if risk_sh <= 0: continue
            qty = max(1, int(BASE_MAX_RISK_BUDGET / risk_sh))
            
            t1 = live_c + (risk_sh * 2.0)
            t2 = live_c + (risk_sh * 4.0)

            stock_sym = s.replace(".NS", "").replace("&", "and")
            
            item_msg = (
                f"🚀 <b>{stock_sym}</b> (ROCKET RIDER)\n"
                f"💰 CMP: ₹{round(live_c, 2)} | 📈 Up: +{stock_pct_change:.2f}%\n"
                f"🔥 Vol Blast: {round(vrr_delta, 1)}x | 🛡️ SL (9-EMA): ₹{round(final_sl, 2)}\n"
                f"🎯 T1 (1:2): ₹{round(t1, 2)} | 🎯 T2 (1:4): ₹{round(t2, 2)}"
            )
            approved_alerts.append(item_msg)
        except: pass

    # सिंगल मैसेज भेजना
    if len(approved_alerts) > 0:
        final_message = (
            f"🔥 <b>AGNI MAX SCANNER ({len(indian_stocks)} Stocks)</b> 🔥\n"
            f"<i>(Catching Day-High Breakouts)</i>\n"
            f"-------------------------------------\n"
        )
        final_message += "\n\n".join(approved_alerts)
        final_message += f"\n-------------------------------------\n⏰ <b>Time:</b> {now_ist.strftime('%I:%M:%S %p IST')}"
        
        send_telegram_alert(final_message)
    else:
        print(f" ⏳ SCAN COMPLETE. No fresh rockets at Day-High. SLEEPING 5 MINS...")
    
    time.sleep(300)
