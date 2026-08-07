# ==============================================================================
# 🚀 PREDATOR v42.0 : AGNI (STRICT GROWW-STYLE + SINGLE MSG + NIFTY GAP LOGIC)
# ==============================================================================
import logging, os, sys, warnings, urllib.request, xml.etree.ElementTree as ET, re, time
from datetime import datetime, time as dtime
import pandas as pd, pytz, yfinance as yf

warnings.filterwarnings("ignore")
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
ist = pytz.timezone("Asia/Kolkata")

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
    safe_chat_id = str(TELEGRAM_CHAT_ID).strip() 
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN.strip()}/sendMessage"
    payload = {"chat_id": safe_chat_id, "text": message, "parse_mode": "HTML"}
    for attempt in range(3):
        try:
            import json
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=20) as response:
                if response.status == 200: return 
        except Exception: time.sleep(2)

BASE_MAX_RISK_BUDGET = 180.0
MIN_STOCK_PRICE = 50.0

sector_map = {
    "IT": ["INFY.NS", "TCS.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS", "COFORGE.NS", "BSOFT.NS", "PERSISTENT.NS", "MPHASIS.NS", "LTTS.NS", "OFSS.NS", "CYIENT.NS", "KPITTECH.NS", "TATAELXSI.NS", "LTIM.NS", "SONATSOFTW.NS", "ZENSARTECH.NS", "INTELLECT.NS", "MASTEK.NS", "HAPPSTMNDS.NS", "LATENTVIEW.NS", "NEWGEN.NS", "DATAPATTNS.NS", "CEINFO.NS", "AFFLE.NS", "ROUTE.NS", "TANLA.NS", "INFIBEAM.NS", "RATEGAIN.NS", "FSL.NS", "NETWEB.NS"],
    "BANK_FIN": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS", "KOTAKBANK.NS", "INDUSINDBK.NS", "BANKBARODA.NS", "PNB.NS", "FEDERALBNK.NS", "AUBANK.NS", "IDFCFIRSTB.NS", "BANDHANBNK.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "CHOLAFIN.NS", "SHRIRAMFIN.NS", "MUTHOOTFIN.NS", "MANAPPURAM.NS", "RECLTD.NS", "PFC.NS", "JIOFIN.NS", "CANBK.NS", "CUB.NS", "RBLBANK.NS", "L&TFH.NS", "LICHSGFIN.NS", "M&MFIN.NS", "HDFCAMC.NS", "ABCAPITAL.NS", "IEX.NS", "MCX.NS", "BSE.NS", "CDSL.NS", "ANGELONE.NS", "UTIAMC.NS", "NAM-INDIA.NS", "CAMS.NS", "KFINTECH.NS", "POONAWALLA.NS", "CREDITACC.NS", "MAHABANK.NS", "INDIANB.NS", "UCOBANK.NS", "CENTRALBK.NS", "IOB.NS", "IFCI.NS"],
    "PHARMA": ["SUNPHARMA.NS", "CIPLA.NS", "DIVISLAB.NS", "DRREDDY.NS", "APOLLOHOSP.NS", "MAXHEALTH.NS", "LUPIN.NS", "AUROPHARMA.NS", "ALKEM.NS", "TORNTPHARM.NS", "BIOCON.NS", "GLENMARK.NS", "LAURUSLABS.NS", "SYNGENE.NS", "GRANULES.NS", "LALPATHLAB.NS", "ZYDUSLIFE.NS", "IPCALAB.NS", "PEL.NS", "NATCOPHARM.NS", "AJANTPHARM.NS", "JBCHEPHARM.NS", "SANOFI.NS", "ABBOTINDIA.NS", "PFIZER.NS", "GLAXO.NS", "MANKIND.NS", "MEDPLUS.NS", "FORTIS.NS", "STARHEALTH.NS", "METROPOLIS.NS", "THYROCARE.NS"],
    "AUTO": ["TATAMOTORS.NS", "M&M.NS", "MARUTI.NS", "HEROMOTOCO.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "TVSMOTOR.NS", "ASHOKLEY.NS", "SONACOMS.NS", "BOSCHLTD.NS", "MRF.NS", "BALKRISIND.NS", "APOLLOTYRE.NS", "MOTHERSON.NS", "EXIDEIND.NS", "ESCORTS.NS", "BHARATFORG.NS", "TIINDIA.NS", "AMARAJABAT.NS", "CEATLTD.NS", "MINDAIND.NS", "UNO-MINDA.NS", "ENDURANCE.NS", "CRAFTSMAN.NS", "JAMNAAUTO.NS", "SUNDRMFAST.NS", "GABRIEL.NS", "OLECTRA.NS", "OLAELEC.NS"],
    "ENERGY": ["RELIANCE.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "COALINDIA.NS", "TATAPOWER.NS", "ADANIGREEN.NS", "JSWENERGY.NS", "GAIL.NS", "BPCL.NS", "HINDPETRO.NS", "IOC.NS", "PETRONET.NS", "IGL.NS", "MGL.NS", "GUJGASLTD.NS", "OIL.NS", "CASTROLIND.NS", "SJVN.NS", "NHPC.NS", "TORNTPOWER.NS", "CESC.NS", "PTC.NS", "SUZLON.NS"],
    "FMCG": ["ITC.NS", "HINDUNILVR.NS", "NESTLEIND.NS", "TATACONSUM.NS", "BRITANNIA.NS", "GODREJCP.NS", "DABUR.NS", "MARICO.NS", "COLPAL.NS", "UBL.NS", "MCDOWELL-N.NS", "TITAN.NS", "PAGEIND.NS", "BATAINDIA.NS", "RADICO.NS", "BALRAMCHIN.NS", "VARROC.NS", "VBL.NS", "EMAMILTD.NS", "PROCTER.NS", "GILLETTE.NS", "WHIRLPOOL.NS", "TTKPRESTIG.NS", "SYMPHONY.NS", "EUREKAFORBE.NS", "CAMPUS.NS", "METROBRAND.NS", "RELAXO.NS", "MANYAVAR.NS", "KALYANKJIL.NS", "BLUESTONE.NS"],
    "DEFENCE_RAIL": ["HAL.NS", "BEL.NS", "MAZDOCK.NS", "COCHINSHIP.NS", "BDL.NS", "IRFC.NS", "RVNL.NS", "IRCON.NS", "TITAGARH.NS", "TEXRAIL.NS", "ASTRAMICRO.NS", "MTARTECH.NS", "BEML.NS", "GRSE.NS", "ZENITHEXPO.NS"],
    "REAL_ESTATE": ["DLF.NS", "GODREJPROP.NS", "OBEROIRLTY.NS", "PRESTIGE.NS", "MACROTECH.NS", "LODHA.NS", "SOBHA.NS", "BRIGADE.NS", "PHOENIXLTD.NS", "IBREALEST.NS", "SUNTECK.NS", "PURVA.NS", "MAHLIFE.NS", "LT.NS", "GRASIM.NS", "GMRINFRA.NS", "IRB.NS", "PNCINFRA.NS", "KNRCON.NS", "NCC.NS", "HGINFRA.NS", "ASHOKA.NS", "JWL.NS", "RITES.NS", "ENGINERSIN.NS", "NBCC.NS", "HUDCO.NS", "JKCEMENT.NS", "RAMCOCEM.NS"],
    "CHEMICALS": ["SRF.NS", "PIIND.NS", "DEEPAKNTR.NS", "TATACHEM.NS", "NAVINFLUOR.NS", "AARTIIND.NS", "GUJALKALI.NS", "ATUL.NS", "COROMANDEL.NS", "CHAMBLFERT.NS", "GNFC.NS", "GSFC.NS", "FACT.NS", "RCF.NS", "UPL.NS", "ALKYLAMINE.NS", "BALAMINES.NS", "CLEAN.NS", "FINEORG.NS", "VINATIORGA.NS", "NEOGEN.NS", "JUBILANT.NS", "SUDARSCHEM.NS", "SUMICHEM.NS", "ASTEC.NS", "SHARDACROP.NS", "BHARATRAS.NS", "BASF.NS", "BODALCHEM.NS", "MEGH.NS", "PARADEEP.NS"],
    "METALS": ["TATASTEEL.NS", "JSWSTEEL.NS", "HINDALCO.NS", "VEDL.NS", "NMDC.NS", "NATIONALUM.NS", "SAIL.NS", "JINDALSTEL.NS", "APLAPOLLO.NS", "HZL.NS", "RATNAMANI.NS", "WELCORP.NS", "JSL.NS", "JSLHISAR.NS", "HINDCOPPER.NS", "HINDZINC.NS", "MUKANDLTD.NS", "MOIL.NS", "GMDC.NS", "UML.NS", "SHYAMMETL.NS", "GRAVITA.NS"],
    "NEW_AGE_RETAIL": ["ZOMATO.NS", "PAYTM.NS", "NYKAA.NS", "POLICYBKR.NS", "TRENT.NS", "ABFRL.NS", "INDHOTEL.NS", "JUBLFOOD.NS", "SUNTV.NS", "ZEEL.NS", "PVRINOX.NS", "DEVYANI.NS", "SAPPHIRE.NS", "WESTLIFE.NS", "CHALET.NS", "LEMONTREE.NS", "CERA.NS", "KAYNES.NS", "SYRMA.NS", "AWL.NS", "TRIDENT.NS", "WELSPUNIND.NS", "KPRMILL.NS", "RAYMOND.NS", "SWIGGY.NS"]
}
indian_stocks = sorted(list(set([s for sec in sector_map.values() for s in sec])))

print(" 🚀 AGNI v42.0 : STRICT SINGLE-MSG LOOP INITIALIZED ...")
send_telegram_alert("🟢 <b>AGNI v42.0 ONLINE</b> (Strict Filters + Single Msg)")

while True:
    now_ist = datetime.now(ist)
    if now_ist.time() > dtime(15, 30, 0):
        send_telegram_alert("🌙 <b>MARKET CLOSED. SYSTEM SHUTTING DOWN.</b>")
        break

    # 🔥 STRICT RULE: 1:00 PM के बाद कोई ट्रेड नहीं (Afternoon Traps Avoid)
    if now_ist.time() > dtime(13, 0, 0):
        print(f" ⏳ No new trades after 1:00 PM. Just keeping server alive... [{now_ist.strftime('%I:%M:%S %p')}]")
        time.sleep(300)
        continue

    print(f"\n ⚡ SCAN STARTED AT : [{now_ist.strftime('%I:%M:%S %p')}]")
    
    try:
        df_daily = yf.download(indian_stocks + ["^NSEI"], period="1mo", interval="1d", group_by="ticker", threads=True, progress=False)
        df_5m = yf.download(indian_stocks + ["^NSEI"], period="5d", interval="5m", group_by="ticker", threads=True, progress=False)
    except Exception as e:
        time.sleep(60)
        continue

    nifty_context = "🟡 NIFTY NEUTRAL"
    nifty_gap_info = "Flat"
    macro_gap_down_freeze, macro_gap_up_freeze = False, False

    try:
        nifty_df_5m = df_5m["^NSEI"].dropna()
        nifty_df_daily = df_daily["^NSEI"].dropna()
        n_live = float(nifty_df_5m["Close"].iloc[-1])
        n_ema20 = float(nifty_df_5m["Close"].ewm(span=20, adjust=False).mean().iloc[-1])
        n_ema9 = float(nifty_df_5m["Close"].ewm(span=9, adjust=False).mean().iloc[-1])
        
        today_data_n = nifty_df_5m.loc[nifty_df_5m.index.date == nifty_df_5m.index.date[-1]]
        
        if len(today_data_n) > 0 and len(nifty_df_daily) > 1:
            n_day_o = float(today_data_n["Open"].iloc[0])
            n_prev_close = float(nifty_df_daily["Close"].iloc[-2])
            nifty_gap_pct = ((n_day_o - n_prev_close) / n_prev_close) * 100
            
            nifty_gap_info = f"{nifty_gap_pct:+.2f}%"
            
            if nifty_gap_pct <= -0.30: 
                macro_gap_down_freeze = True
                nifty_context = f"🔴 GAP-DOWN ({nifty_gap_info}) - NO LONGS"
            elif nifty_gap_pct >= 0.30: 
                macro_gap_up_freeze = True
                nifty_context = f"🟢 GAP-UP ({nifty_gap_info}) - STRONG LONGS ONLY"
            else:
                if n_live > n_ema20 and n_ema9 >= n_ema20: nifty_context = f"🟢 BULLISH (Gap: {nifty_gap_info})"
                elif n_live < n_ema20 and n_ema9 <= n_ema20: nifty_context = f"🔴 BEARISH (Gap: {nifty_gap_info})"
    except: pass

    parent_audit = {}
    for s in indian_stocks:
        try:
            d_df = df_daily[s].dropna()
            if len(d_df) < 15: continue
            parent_audit[s] = {"EMA20_D": float(d_df["Close"].ewm(span=20, adjust=False).mean().iloc[-1]), "Prev_Candle": "BEAR" if d_df["Close"].iloc[-2] < d_df["Open"].iloc[-2] else "BULL"}
        except: pass

    # यह लिस्ट उन सारे स्टॉक्स को जमा करेगी जो पास होंगे
    approved_alerts = []

    for s in indian_stocks:
        try:
            if s not in df_5m.columns.levels[0] or s not in parent_audit: continue
            df = df_5m[s].dropna()
            live_c = float(df["Close"].iloc[-1])
            if live_c < MIN_STOCK_PRICE: continue

            df["Typ"] = (df["High"] + df["Low"] + df["Close"]) / 3
            df["Date"] = df.index.date
            df["VWAP"] = df.groupby("Date").apply(lambda x: (x["Typ"] * x["Volume"]).cumsum() / x["Volume"].cumsum()).reset_index(level=0, drop=True)
            df["EMA20"] = df["Close"].ewm(span=20, adjust=False).mean()
            atr_14 = float(df[["High", "Low", "Close"]].apply(lambda x: max(x["High"]-x["Low"], abs(x["High"]-x["Close"]), abs(x["Low"]-x["Close"])), axis=1).rolling(14).mean().iloc[-1])
            
            curr_o, curr_h, curr_l = float(df["Open"].iloc[-1]), float(df["High"].iloc[-1]), float(df["Low"].iloc[-1])
            live_vwap, ema_val = float(df["VWAP"].iloc[-1]), float(df["EMA20"].iloc[-1])
            live_v, prev_v = float(df["Volume"].iloc[-1]), float(df["Volume"].iloc[-2])

            vrr_delta = (live_v / prev_v) if prev_v > 0 else 1.0

            p_data = parent_audit[s]
            today_data = df.loc[df["Date"] == df["Date"].iloc[-1]]
            prev_close = float(df["Close"].iloc[-len(today_data)-1]) if len(df) > len(today_data) else float(today_data["Open"].iloc[0])
            
            stock_pct_change = ((live_c - prev_close) / prev_close) * 100
            
            trade_dir = None
            if live_c > p_data["EMA20_D"] and live_c > live_vwap and vrr_delta >= 2.5: trade_dir = "LONG"
            elif live_c < p_data["EMA20_D"] and live_c < live_vwap and vrr_delta >= 2.5: trade_dir = "SHORT"

            if not trade_dir: continue

            # 🔥 STRICT GROWW-STYLE FILTER: स्टॉक को कम से कम 2% भागा हुआ होना ही चाहिए
            if trade_dir == "LONG" and stock_pct_change < 2.0: continue
            if trade_dir == "SHORT" and stock_pct_change > -2.0: continue

            if trade_dir == "LONG" and macro_gap_down_freeze: continue

            is_wick_rejection = False
            if (curr_h - curr_l) > 0:
                upper_wick_pct = (curr_h - max(curr_o, live_c)) / (curr_h - curr_l)
                if trade_dir == "LONG" and upper_wick_pct > 0.40: is_wick_rejection = True

            vwap_dist = ((live_c - live_vwap) / live_vwap) * 100
            if trade_dir == "LONG" and (vwap_dist < 0.1 or vwap_dist > 3.0): continue # VWAP से बहुत दूर वालों को इग्नोर

            if not is_wick_rejection and vrr_delta < 15.0:
                sl_buffer = atr_14 * 0.05
                final_sl = min(live_vwap, ema_val) - sl_buffer if trade_dir == "LONG" else max(live_vwap, ema_val) + sl_buffer
                risk_sh = abs(live_c - final_sl)
                
                if risk_sh <= 0: continue
                qty = max(1, int(BASE_MAX_RISK_BUDGET / risk_sh))
                
                # 🔥 PRACTICAL TARGETS (T1 = 1:1.5 | T2 = 1:3)
                t1 = live_c + (risk_sh * 1.5) if trade_dir == "LONG" else live_c - (risk_sh * 1.5)
                t2 = live_c + (risk_sh * 3.0) if trade_dir == "LONG" else live_c - (risk_sh * 3.0)

                stock_sym = s.replace(".NS", "").replace("&", "and") # HTML ब्रेक न हो इसलिए & को बदल दिया
                
                # सिंगल स्टॉक का डाटा तैयार
                item_msg = (
                    f"📌 <b>{stock_sym}</b> ({trade_dir})\n"
                    f"💰 CMP: ₹{round(live_c, 2)} | 📈 Up: {stock_pct_change:+.2f}%\n"
                    f"📊 Vol: {round(vrr_delta, 1)}x | 🛡️ SL: ₹{round(final_sl, 2)}\n"
                    f"🎯 T1 (1:1.5): ₹{round(t1, 2)} | 🎯 T2 (1:3): ₹{round(t2, 2)}"
                )
                approved_alerts.append(item_msg)
        except: pass

    # ------------------------------------------------------------------------------
    # 📉 SENDING ONE CONSOLIDATED MESSAGE
    # ------------------------------------------------------------------------------
    if len(approved_alerts) > 0:
        final_message = (
            f"🔥 <b>AGNI TOP GAINERS SCAN</b> 🔥\n"
            f"<b>{nifty_context}</b>\n"
            f"-------------------------------------\n"
        )
        final_message += "\n\n".join(approved_alerts)
        final_message += f"\n-------------------------------------\n⏰ <b>Time:</b> {now_ist.strftime('%I:%M:%S %p IST')}"
        
        send_telegram_alert(final_message)
    else:
        print(f" ⏳ SCAN COMPLETE. No strict Groww-style setups found. SLEEPING FOR EXACTLY 5 MINS...")
    
    time.sleep(300)
