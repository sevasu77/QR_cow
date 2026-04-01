import streamlit as st
import yfinance as yf

# --- 1. Python側：市場データ取得 (yfinance) ---
@st.cache_data(ttl=3600)  # 1時間キャッシュ
def get_nvda_market_data():
    try:
        nvda = yf.Ticker("NVDA")
        hist = nvda.history(period="2d")
        if len(hist) < 2:
            return 1.02  # デフォルト値
        prev_close = hist['Close'].iloc[-2]
        current_price = hist['Close'].iloc[-1]
        change = ((current_price - prev_close) / prev_close) * 100
        return round(change, 2)
    except:
        return 1.02

nvda_change = get_nvda_market_data()

# --- 2. HTML/JavaScript/CSS 統合コード ---
game_code = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <style>
        body {{ 
            margin: 0; background: #000428; color: white; 
            font-family: 'Courier New', Courier, monospace; overflow: hidden; 
        }}
        #game-container {{ 
            position: relative; width: 400px; height: 600px; 
            background: linear-gradient(to bottom, #000428, #004e92); 
            margin: auto; border: 4px solid #fff; border-radius: 20px; 
            overflow: hidden;
        }}
        #cow-container {{ 
            position: absolute; z-index: 10; display: flex; 
            align-items: center; justify-content: center;
        }}
        #cow {{ font-size: 50px; user-select: none; line-height: 1; }}
        #qr-holder-mini {{
            position: absolute; top: 5px; right: 8px;
            width: 18px; height: 18px; background: white;
            padding: 1px; border: 1px solid #333; border-radius: 2px;
        }}
        #pause-overlay {{
            position: absolute; inset: 0; background: rgba(0,0,0,0.85);
            display: none; z-index: 1500; align-items: center; justify-content: center;
        }}
        #pause-card {{
            background: rgba(255,255,255,0.1); border: 2px solid gold;
            padding: 20px; border-radius: 15px; text-align: center;
            width: 280px; backdrop-filter: blur(5px); box-shadow: 0 0 30px rgba(255,215,0,0.3);
        }}
        #qr-holder-large {{
            background: white; padding: 10px; display: inline-block;
            margin: 15px 0; border-radius: 8px;
        }}
        .market-alert {{
            animation: blink 0.5s infinite alternate;
            border-color: red !important;
        }}
        @keyframes blink {{
            from {{ box-shadow: 0 0 2px red; }}
            to {{ box-shadow: 0 0 10px red; background: #fdd; }}
        }}
        .bull-mode {{ text-shadow: 0 0 20px gold; }}
        .bear-mode {{ text-shadow: 0 0 20px #a0f; filter: saturate(0.6); }}
        .platform {{ 
            position: absolute; height: 12px; background: #00ffcc; 
            border-radius: 6px; box-shadow: 0 0 15px #00ffcc; 
        }}
        #ui {{ 
            position: absolute; top: 15px; left: 15px; z-index: 100; 
            background: rgba(0,0,0,0.7); padding: 10px; border-radius: 8px; font-size: 12px;
            border: 1px solid #444;
        }}
        .market-val {{ 
            color: {{ '#00ff00' if nvda_change >= 0 else '#ff00ff' }}; 
            font-weight: bold; 
        }}
    </style>
</head>
<body>
<div id="game-container">
    <div id="pause-overlay">
        <div id="pause-card">
            <h2 style="color: gold; margin: 0;">MARKET ANALYSIS</h2>
            <p style="font-size: 13px; color: #ccc; margin: 10px 0;">
                Scanning the chip to access<br><b>ASML Investor Relations</b>
            </p>
            <div id="qr-holder-large"></div>
            <div style="font-size: 40px; margin: 10px 0;">🐄</div>
            <p style="font-size: 14px; margin: 0; color: gold;">Press [P] to Resume</p>
        </div>
    </div>
    <div id="ui">
        REAL-TIME NVDA: <span class="market-val">{nvda_change}%</span><br>
        ALTITUDE: <span id="altitude" style="color: gold;">0</span>m<br>
        <span style="color: #aaa;">[P] Pause & Analysis</span>
    </div>
    <div id="cow-container">
        <div id="qr-holder-mini"></div>
        <div id="cow">🐄</div>
    </div>
</div>
<script>
    const container = document.getElementById('game-container');
    const cowBox = document.getElementById('cow-container');
    const qrMini = document.getElementById('qr-holder-mini');
    const qrLarge = document.getElementById('qr-holder-large');
    const pauseOverlay = document.getElementById('pause-overlay');
    const altDisp = document.getElementById('altitude');
    
    // --- 市場パラメータ ---
    const nvdaChange = {nvda_change};
    let gravity = 0.4 * (1 - (nvdaChange / 20));
    let jumpPower = -11 * (1 + (nvdaChange / 100)); // ジャンプ力をマイルドに調整
    
    if(nvdaChange >= 0) {{
        cowBox.classList.add('bull-mode');
    }} else {{
        cowBox.classList.add('bear-mode');
        qrMini.classList.add('market-alert');
    }}

    // QRコード生成
    const irUrl = "https://www.asml.com/en/investors";
    new QRCode(qrMini, {{ text: irUrl, width: 18, height: 18, correctLevel: QRCode.CorrectLevel.L }});
    new QRCode(qrLarge, {{ text: irUrl, width: 150, height: 150, correctLevel: QRCode.CorrectLevel.H }});

    // サウンド
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playMoo() {{
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        const freq = 150 + (nvdaChange * 10);
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq * 0.7, audioCtx.currentTime + 0.4);
        gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(); osc.stop(audioCtx.currentTime + 0.4);
    }}

    // ゲーム変数
    let cow = {{ x: 175, y: 300, vx: 0, vy: 0 }};
    let platforms = [];
    let altitude = 0;
    let isPaused = false;
    let keys = {{}};

    // 初期化
    function init() {{
        // 足場を6つ生成（1つ目は牛の真下）
        platforms.push({{ x: 150, y: 500, w: 100 }});
        for(let i=1; i<6; i++) {{
            platforms.push({{ x: Math.random() * 300, y: 500 - (i * 110), w: 100 }});
        }}
        // 足場要素をDOMに作成
        platforms.forEach((p, i) => {{
            const el = document.createElement('div');
            el.className = 'platform';
            el.id = 'plt-' + i;
            container.appendChild(el);
        }});
        loop();
    }}

    function togglePause() {{
        isPaused = !isPaused;
        pauseOverlay.style.display = isPaused ? 'flex' : 'none';
        if(!isPaused) loop();
    }}

    function loop() {{
        if(isPaused) return;

        cow.vy += gravity;
        cow.y += cow.vy;

        if(keys['ArrowLeft']) cow.x -= 7;
        if(keys['ArrowRight']) cow.x += 7;

        if(cow.x < -30) cow.x = 380; if(cow.x > 380) cow.x = -30;

        if(cow.y > 600) {{
            alert("MARKET CRASH! Alt: " + Math.floor(altitude) + "m");
            location.reload(); return;
        }}

        // 当たり判定
        platforms.forEach(p => {{
            if(cow.vy > 0 && cow.x + 35 > p.x && cow.x < p.x + p.w &&
               cow.y + 50 > p.y && cow.y + 50 < p.y + 15) {{
                cow.vy = jumpPower;
                playMoo();
            }}
        }});

        // スクロール処理
        if(cow.y < 250) {{
            let diff = 250 - cow.y; 
            cow.y = 250;
            altitude += diff / 5;
            platforms.forEach(p => {{
                p.y += diff;
                // 足場が下に消えたら上へ戻す（無限ループ）
                if(p.y > 600) {{ 
                    p.y -= 600; 
                    p.x = Math.random() * 300; 
                }}
            }});
        }}

        // 表示更新
        cowBox.style.left = cow.x + 'px';
        cowBox.style.top = cow.y + 'px';
        altDisp.innerText = Math.floor(altitude);
        
        platforms.forEach((p, i) => {{
            const el = document.getElementById('plt-' + i);
            if(el) {{
                el.style.left = p.x + 'px';
                el.style.top = p.y + 'px';
                el.style.width = p.w + 'px';
            }}
        }});

        requestAnimationFrame(loop);
    }}

    window.addEventListener('keydown', e => {{
        keys[e.key] = true;
        if(e.key.toLowerCase() === 'p') togglePause();
    }});
    window.addEventListener('keyup', e => keys[e.key] = false);
    
    init();
</script>
</body>
</html>
"""

st.set_page_config(page_title="NVDA Cow Jump", layout="centered")
st.components.v1.html(game_code, height=650)
