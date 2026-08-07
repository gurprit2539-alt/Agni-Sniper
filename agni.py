# ==============================================================================
# 🚀 PREDATOR v41.0 : AGNI (CONTINUOUS EXACT 5-MIN LOOP + HTML TELEGRAM)
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
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(" ⚠️ TELEGRAM WARNING: Token या Chat ID नहीं मिला।")
        return
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
MAX_STOCKS_PER_SECTOR = 2
MAX_VRR_CAP = 15.0

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
    "NEW_AGE_RETAIL": ["ZOMATO.NS", "PAYTM.NS", "NYKAA.NS", "POLICYBKR.NS", "TRENT.NS", "ABFRL.NS", "INDHOTEL.NS", "JUBLFOOD.NS", "SUNTV.NS", "ZEEL.NS", "PVRINOX.NS", "DEVYANI.NS", "SAPPHIRE.NS", "WESTLIFE.NS", "CHALET.NS", "LEMONTREE.NS", "CERA.NS", "KAYNES.NS", "SYRMA.NS", "AWL.NS", "TRIDENT.NS", "WELSPUNIND.NS", "KPRMILL.NS", "RAYMOND.NS", "SWIGGY.NS"],
    "LOGISTICS_AVIATION": ["INDIGO.NS", "BLUEDART.NS", "DELHIVERY.NS", "EASEMYTRIP.NS", "IRCTC.NS"],
    "CAPITAL_GOODS": ["ULTRACEMCO.NS", "AMBUJACEM.NS", "SHREECEM.NS", "ACC.NS", "DALBHARAT.NS", "ABB.NS", "SIEMENS.NS", "CUMMINSIND.NS", "BHEL.NS", "POLYCAB.NS", "KEI.NS", "VOLTAS.NS", "HAVELLS.NS", "CROMPTON.NS", "DIXON.NS", "ASTRAL.NS", "FINCABLES.NS", "VGUARD.NS", "APARINDS.NS", "CGPOWER.NS", "HITACHI.NS", "THERMAX.NS", "HONAUT.NS", "TRIVENI.NS", "EIAHAHOTELS.NS"]
}
indian_stocks = sorted(list(set([s for sec in sector_map.values() for s in sec])))

print(" 🚀 AGNI v41.0 : CONTINUOUS LOOP INITIALIZED ...")
send_telegram_alert("🟢 <b>AGNI SNIPER ONLINE (EXACT 5-MIN LOOP ACTIVE)</b> 🚀")

# ------------------------------------------------------------------------------
# 🔄 CONTINUOUS LOOP ENGINE (मार्केट आवर्स में सर्वर जिंदा रखेगा)
# ------------------------------------------------------------------------------
while True:
    now_ist = datetime.now(ist)
    
    # 🕒 3:30 PM के बाद लूप अपने आप टूट जाएगा और सर्वर बंद हो जाएगा
    if now_ist.time() > dtime(15, 30, 0):
        send_telegram_alert("🌙 <b>MARKET CLOSED. SYSTEM SHUTTING DOWN TILL TOMORROW.</b>")
        print(" 🌙 Market Closed. Exiting Loop.")
        break

    print(f"\n ⚡ SCAN STARTED AT : [{now_ist.strftime('%I:%M:%S %p')}]")
    passed_stocks_count = 0
    
    try:
        df_daily = yf.download(indian_stocks + ["^NSEI"], period="1mo", interval="1d", group_by="ticker", threads=True, progress=False)
        df_5m = yf.download(indian_stocks + ["^NSEI"], period="5d", interval="5m", group_by="ticker", threads=True, progress=False)
    except Exception as e:
        print(f" ⛔ FETCH ERROR: {e}")
        time.sleep(60)
        continue

    nifty_regime = "🟡 CHOPPY / NEUTRAL"
    macro_gap_down_freeze = False
    macro_gap_up_freeze = False
    nifty_pct_change = 0.0

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
            nifty_pct_change = ((n_live - n_prev_close) / n_prev_close) * 100
            
            if nifty_gap_pct <= -0.30 and now_ist.time() < dtime(10, 30, 0): macro_gap_down_freeze, nifty_regime = True, f"🔴 GAP-DOWN FREEZE"
            elif nifty_gap_pct >= 0.30 and now_ist.time() < dtime(10, 30, 0): macro_gap_up_freeze, nifty_regime = True, f"🟢 GAP-UP FREEZE"
            else:
                buffer = n_live * 0.0008
                if n_live > (n_ema20 + buffer) and n_live > n_day_o and n_ema9 >= n_ema20: nifty_regime = "🟢 BULLISH"
                elif n_live < (n_ema20 - buffer) and n_live < n_day_o and n_ema9 <= n_ema20: nifty_regime = "🔴 BEARISH"
    except: pass

    is_choppy = "CHOPPY" in nifty_regime or "FREEZE" in nifty_regime
    min_score_required = 80 if is_choppy else 70
    MY_MAX_RISK_BUDGET = BASE_MAX_RISK_BUDGET / 2.0 if is_choppy else BASE_MAX_RISK_BUDGET

    is_afternoon_session = now_ist.time() >= dtime(14, 0, 0)
    current_vrr_ceiling = 6.0 if is_afternoon_session else 10.0

    parent_audit, sector_perf = {}, {}
    for s in indian_stocks:
        try:
            d_df = df_daily[s].dropna().copy()
            if len(d_df) < 15: continue
            d_df["H-L"] = d_df["High"] - d_df["Low"]
            d_df["H-PC"] = (d_df["High"] - d_df["Close"].shift(1)).abs()
            d_df["L-PC"] = (d_df["Low"] - d_df["Close"].shift(1)).abs()
            parent_audit[s] = {"ADR": float(d_df[["H-L", "H-PC", "L-PC"]].max(axis=1).iloc[-15:-1].mean()), "EMA20_D": float(d_df["Close"].ewm(span=20, adjust=False).mean().iloc[-1]), "Prev_Candle": "BEAR" if d_df["Close"].iloc[-2] < d_df["Open"].iloc[-2] else "BULL"}
        except: pass

    for sec_name, tickers in sector_map.items():
        gains = []
        for t in tickers:
            try:
                df_t = df_5m[t].dropna()
                df_today = df_t.loc[df_t.index.date == df_t.index.date[-1]]
                if len(df_today) > 0: gains.append(((float(df_today["Close"].iloc[-1]) - float(df_today["Open"].iloc[0])) / float(df_today["Open"].iloc[0])) * 100)
            except: pass
        sector_perf[sec_name] = pd.Series(gains).median() if gains else 0.0

    sorted_sec = sorted(sector_perf.items(), key=lambda x: x[1], reverse=True)
    top_sec_bull, top_sec_bear = [s[0] for s in sorted_sec[:4]], [s[0] for s in sorted_sec[-4:]]

    for s in indian_stocks:
        try:
            if s not in df_5m.columns.levels[0] or s not in parent_audit: continue
            df = df_5m[s].dropna()
            live_c = float(df["Close"].iloc[-1])
            if live_c < MIN_STOCK_PRICE: continue

            df["Typ"] = (df["High"] + df["Low"] + df["Close"]) / 3
            df["Date"] = df.index.date
            df["VWAP"] = df.groupby("Date").apply(lambda x: (x["Typ"] * x["Volume"]).cumsum() / x["Volume"].cumsum()).reset_index(level=0, drop=True)
            df["EMA20"], df["EMA9"] = df["Close"].ewm(span=20, adjust=False).mean(), df["Close"].ewm(span=9, adjust=False).mean()
            atr_14 = float(df[["High", "Low", "Close"]].apply(lambda x: max(x["High"]-x["Low"], abs(x["High"]-x["Close"]), abs(x["Low"]-x["Close"])), axis=1).rolling(14).mean().iloc[-1])
            
            curr_o, curr_h, curr_l = float(df["Open"].iloc[-1]), float(df["High"].iloc[-1]), float(df["Low"].iloc[-1])
            close_pct = ((live_c - curr_l) / (curr_h - curr_l)) * 100 if (curr_h - curr_l) > 0 else 50.0
            live_vwap, ema_val, ema9_val = float(df["VWAP"].iloc[-1]), float(df["EMA20"].iloc[-1]), float(df["EMA9"].iloc[-1])
            live_v, prev_v = float(df["Volume"].iloc[-1]), float(df["Volume"].iloc[-2])

            last_candle_time = ist.localize(df.index[-1]) if df.index[-1].tzinfo is None else df.index[-1]
            seconds_from_start = (now_ist - last_candle_time).total_seconds()
            vrr_multiplier = min(300.0 / max(20.0, seconds_from_start), 15.0) if 0 < seconds_from_start < 300 else 1.0
            vrr_delta = (live_v * vrr_multiplier / prev_v) if prev_v > 0 else 1.0

            p_data = parent_audit[s]
            today_data = df.loc[df["Date"] == df["Date"].iloc[-1]]
            day_high, day_low = float(today_data["High"].max()), float(today_data["Low"].min())
            prev_close = float(df["Close"].iloc[-len(today_data)-1]) if len(df) > len(today_data) else float(today_data["Open"].iloc[0])
            
            stock_pct_change = ((live_c - prev_close) / prev_close) * 100
            rs_outperformance = stock_pct_change - nifty_pct_change
            adr_used_pct = ((max(day_high, prev_close) - min(day_low, prev_close)) / p_data["ADR"]) * 100
            my_sec = next((sec for sec, ticks in sector_map.items() if s in ticks), "OTHER")
            
            # Simple Ignition check (2.5x volume delta)
            has_ignition_early = (vrr_delta >= 2.5)

            trade_dir, is_contrarian_jackpot, fake_defensive, sec_divergence = None, False, False, False

            if "BULLISH" in nifty_regime and live_c > p_data["EMA20_D"] and p_data["Prev_Candle"] == "BULL": trade_dir = "LONG"
            elif "BEARISH" in nifty_regime and live_c < p_data["EMA20_D"] and p_data["Prev_Candle"] == "BEAR": trade_dir = "SHORT"
            
            if not trade_dir and rs_outperformance >= 2.0 and live_c > live_vwap and has_ignition_early:
                trade_dir, is_contrarian_jackpot = "LONG", True

            if trade_dir == "SHORT" and "BULLISH" in nifty_regime and rs_outperformance > 0: continue
            if trade_dir == "LONG" and ("BEARISH" in nifty_regime) and not is_contrarian_jackpot: continue

            if not trade_dir: continue
            
            is_wick_rejection, wick_alert = False, ""
            if (curr_h - curr_l) > 0:
                upper_wick_pct = (curr_h - max(curr_o, live_c)) / (curr_h - curr_l)
                lower_wick_pct = (min(curr_o, live_c) - curr_l) / (curr_h - curr_l)
                if trade_dir == "LONG" and upper_wick_pct > 0.40: is_wick_rejection = True
                elif trade_dir == "SHORT" and lower_wick_pct > 0.40: is_wick_rejection = True

            candle_body_pct = abs(curr_o - live_c) / (curr_h - curr_l) if (curr_h - curr_l) > 0 else 0
            
            score, reasons = 0, []
            if trade_dir == "LONG" and rs_outperformance >= 1.5: score += 20; reasons.append(f"💪 RS(+{rs_outperformance:.1f}%)")
            vwap_dist = ((live_c - live_vwap) / live_vwap) * 100
            if trade_dir == "LONG" and 0.1 <= vwap_dist <= 2.5: score += 35; reasons.append("VWAP-Base")
            elif trade_dir == "SHORT" and -2.5 <= vwap_dist <= -0.1: score += 35; reasons.append("VWAP-Reject")
            if has_ignition_early and adr_used_pct <= 70.0: score += 25; reasons.append("⚡Fresh-Fuel")
            if has_ignition_early and ((trade_dir == "LONG" and close_pct >= 50.0) or (trade_dir == "SHORT" and close_pct <= 50.0)):
                score += 40; reasons.append(f"🔥 True-Ignition(VRR {vrr_delta:.1f}x)")

            if score >= min_score_required:
                sl_buffer = atr_14 * 0.05
                final_sl = min(live_vwap, ema_val) - sl_buffer if trade_dir == "LONG" else max(live_vwap, ema_val) + sl_buffer
                risk_sh = abs(live_c - final_sl)
                
                if risk_sh <= 0: continue
                qty = max(1, int(MY_MAX_RISK_BUDGET / risk_sh))
                t1 = live_c + (risk_sh * 3.0) if trade_dir == "LONG" else live_c - (risk_sh * 3.0)
                t2 = live_c + (risk_sh * 5.0) if trade_dir == "LONG" else live_c - (risk_sh * 5.0)

                verdict = "🟢 PASS"
                if (curr_h - curr_l) == 0 and abs(stock_pct_change) > 4.5: verdict = "REJECT"
                elif adr_used_pct > 250.0: verdict = "REJECT"
                elif is_wick_rejection: verdict = "REJECT"
                elif vrr_delta >= MAX_VRR_CAP: verdict = "REJECT"
                elif vrr_delta >= current_vrr_ceiling: verdict = "REJECT"

                if "REJECT" not in verdict:
                    passed_stocks_count += 1
                    stock_sym = s.replace(".NS", "")
                    msg = (
                        f"🔥 <b>AGNI BREAKOUT ALERT</b> 🔥\n"
                        f"-------------------------------------\n"
                        f"📌 <b>Stock:</b> <code>{stock_sym}</code> ({trade_dir})\n"
                        f"💰 <b>CMP:</b> ₹{round(live_c, 2)}\n"
                        f"📊 <b>Volume:</b> {round(vrr_delta, 1)}x\n"
                        f"🛡️ <b>SL:</b> ₹{round(final_sl, 2)}\n"
                        f"🎯 <b>T1:</b> ₹{round(t1, 2)}\n"
                        f"🎯 <b>T2:</b> ₹{round(t2, 2)}\n"
                        f"📦 <b>Qty:</b> {qty} Shares\n"
                        f"🧠 <b>Logic:</b> { ' + '.join(reasons) }\n"
                        f"-------------------------------------\n"
                        f"⏰ <b>Time:</b> {now_ist.strftime('%I:%M:%S %p IST')}"
                    )
                    send_telegram_alert(msg)
        except: pass

    # हार्टबीट मैसेज (हर बार नहीं, सिर्फ कंसोल में प्रिंट करेगा ताकि टेलीग्राम स्पैम न हो)
    print(f" ⏳ SCAN COMPLETE. Stocks passed: {passed_stocks_count}. SLEEPING FOR EXACTLY 5 MINS...")
    
    # 300 सेकंड (5 मिनट) का परफेक्ट स्लीप (GitHub इसे बंद नहीं कर पाएगा)
    time.sleep(300)
