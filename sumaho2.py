import pandas as pd
import json
import os

def safe_float(value, default=0.0):
    try:
        val_str = str(value).strip()
        if val_str in ['#N/A!', '#N/A', 'NaN', 'nan', 'null', '']:
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_str(value, default="-"):
    if pd.isna(value):
        return default
    val_str = str(value).strip()
    if val_str in ['#N/A!', '#N/A', 'NaN', 'nan', 'null', '', 'F0']:
        return default
    return val_str

# ============================================================
# HTML / CSS テンプレート
# ============================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ボートレース 分析ダッシュボード</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div id="phone-scene">
  <div id="phone-frame">
    <div id="phone-notch">
      <div id="notch-camera"></div>
      <div id="notch-speaker"></div>
    </div>
    <div id="phone-screen">
<div id="dashboard">
  <div id="top-row">
    <div class="card" id="logo-card">
      <div id="logo-ring-outer">
        <div id="logo-ring-inner">
          <div id="logo-text">
            <span id="venue-name">--</span>
            <span id="race-num">--</span>
          </div>
        </div>
        <canvas id="ring-canvas"></canvas>
      </div>
    </div>
    <div class="card" id="donut-card">
      <div class="card-title" id="target-player-name">In逃げ率</div>
      <div id="donut-wrap">
        <canvas id="donutChart"></canvas>
        <div id="donut-center-val">--</div>
      </div>
    </div>
    <div class="card" id="mini-bar-card">
      <div class="mini-kpi-row">
        <div class="mini-kpi">
          <div class="card-title">1-2率</div>
          <canvas id="miniBarChart1"></canvas>
          <div class="kpi-val accent-red" id="kpi-1-2">--%</div>
        </div>
        <div class="mini-kpi">
          <div class="card-title">1-3率</div>
          <canvas id="miniBarChart2"></canvas>
          <div class="kpi-val accent-yellow" id="kpi-1-3">--%</div>
        </div>
      </div>
    </div>
    <div class="card" id="hbar-card">
      <div class="card-title">決まり手データ</div>
      <canvas id="hbarChart"></canvas>
    </div>
    <div class="card" id="rentai-card">
      <div class="card-title-row">
        <span class="card-title">3連対率</span>
        <div class="legend-row">
          <span class="legend-dot" style="background:#444444"></span><span>1着</span>
          <span class="legend-dot" style="background:#888888"></span><span>2着</span>
          <span class="legend-dot" style="background:#CCCCCC"></span><span>3着</span>
        </div>
      </div>
      <canvas id="rentaiChart"></canvas>
    </div>
  </div>
  <div id="bottom-row">
    <div class="card" id="player-table-card">
      <table id="player-table">
        <thead>
          <tr>
            <th>艇</th>
            <th>選手名</th>
            <th>級別</th>
            <th>支部</th>
            <th>FL</th>
            <th>全国勝率</th>
            <th>当地勝率</th>
            <th>評価</th>
            <th>モーター</th>
            <th>point</th>
          </tr>
        </thead>
        <tbody id="player-tbody"></tbody>
      </table>
    </div>
    <div id="center-charts">
      <div class="dot-row">
        <div class="card dot-card">
          <div class="card-title">コース平均ST</div>
          <canvas id="dot1"></canvas>
        </div>
        <div class="card dot-card">
          <div class="card-title">今節平均ST</div>
          <canvas id="dot2"></canvas>
        </div>
      </div>
      <div class="dot-row">
        <div class="card dot-card">
          <div class="card-title">コース平均ST順位</div>
          <canvas id="dot3"></canvas>
        </div>
        <div class="card dot-card">
          <div class="card-title">今節平均ST順位</div>
          <canvas id="dot4"></canvas>
        </div>
      </div>
      <div class="bottom-bar-row">
        <div class="card bottom-bar-card">
          <div class="card-title">コースSTトップ率</div>
          <canvas id="bottomBar1"></canvas>
        </div>
        <div class="card bottom-bar-card">
          <div class="card-title">コースST最下位率</div>
          <canvas id="bottomBar2"></canvas>
        </div>
      </div>
    </div>
    <div id="right-panels">
      <div class="card right-panel" id="right-panel-top">
        <div class="panel-header">枠番進入・1着時2着傾向</div>
        <table class="data-table" id="statsTable1">
          <thead id="statsHead1"></thead>
          <tbody id="statsBody1"></tbody>
        </table>
      </div>
      <div class="card right-panel" id="right-panel-bottom">
        <div class="panel-header">今節成績</div>
        <table class="konsetsu-table" id="konsetsuTable">
          <thead id="konsetsuHead"></thead>
          <tbody id="konsetsuBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>
    </div>
  </div>
</div>
<script src="js/data.js"></script>
<script src="js/charts.js"></script>
<script src="js/main.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('donut-center-val').textContent = KPI.donut.val.toFixed(0) + '%';
    document.getElementById('kpi-1-2').textContent = (KPI.miniBar1.val).toFixed(0) + '%';
    document.getElementById('kpi-1-3').textContent = (KPI.miniBar2.val).toFixed(0) + '%';
    if(PLAYERS && PLAYERS.length > 0) {
      const playerNameDiv = document.createElement('div');
      playerNameDiv.style.cssText = 'position:absolute;top:37%;left:50%;transform:translate(-50%,-50%);font-size:10px;color:#ffffff;font-weight:600;';
      playerNameDiv.textContent = PLAYERS[0].name;
      document.getElementById('donut-wrap').appendChild(playerNameDiv);
    }
  });
</script>
</body>
</html>"""

CSS_TEMPLATE = """*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
#phone-scene {
  width: 100vw; height: 100vh;
  background: radial-gradient(ellipse at 50% 50%, #1a2035 0%, #080c14 100%);
  display: flex; align-items: center; justify-content: center; overflow: hidden;
}
#phone-frame {
  position: relative; width: min(96vw, 170vh); aspect-ratio: 16 / 7.5;
  background: linear-gradient(145deg, #2a2f3d 0%, #1a1d28 40%, #0f1118 100%);
  border-radius: 40px;
  box-shadow: 0 50px 100px rgba(0,0,0,0.7), inset 0 2px 4px rgba(255,255,255,0.05);
}
#phone-notch {
  position: absolute; top: 0; left: 50%; transform: translateX(-50%);
  width: 180px; height: 30px; background: #0a0c10; border-radius: 0 0 18px 18px; z-index: 100;
  display: flex; align-items: center; justify-content: center; gap: 10px;
}
#notch-camera { width: 12px; height: 12px; border-radius: 50%; background: #1a1d24; box-shadow: inset 0 1px 2px rgba(0,0,0,0.4); }
#notch-speaker { width: 50px; height: 4px; border-radius: 2px; background: #0e1014; }
#phone-screen {
  position: absolute; inset: 14px; border-radius: 30px; overflow: hidden;
  background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
}
#dashboard {
  width: 100%; height: 100%; display: flex; flex-direction: column; gap: 6px; padding: 12px 10px;
  overflow-y: auto; overflow-x: hidden;
  scrollbar-width: thin; scrollbar-color: #3498db #1a1f2e;
}
#dashboard::-webkit-scrollbar { width: 4px; }
#dashboard::-webkit-scrollbar-track { background: #1a1f2e; border-radius: 2px; }
#dashboard::-webkit-scrollbar-thumb { background: #3498db; border-radius: 2px; }
#top-row, #bottom-row { display: grid; gap: 6px; }
#top-row { grid-template-columns: 1fr 0.7fr 0.7fr 1.3fr 1.3fr; height: 160px; }
#bottom-row { grid-template-columns: 1.7fr 1.5fr 0.7fr; max-height: 480px; overflow: hidden; }

.card {
  background: linear-gradient(135deg, #1e2538 0%, #151823 100%);
  border: 1px solid rgba(52, 152, 219, 0.2);
  border-radius: 6px; padding: 6px; overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}
.card-title {
  font-size: 9px; font-weight: 600; color: #9bb2cc; margin-bottom: 4px;
  text-align: center; text-transform: uppercase; letter-spacing: 0.2px;
}
.card-title-row {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 6px; font-size: 10px; font-weight: 600; color: #9bb2cc;
}
.legend-row { display: flex; gap: 6px; align-items: center; font-size: 8px; }
.legend-dot { width: 8px; height: 8px; border-radius: 2px; display: inline-block; }

#logo-card {
  display: flex; align-items: center; justify-content: center;
  background: radial-gradient(circle, #1e3a5f 0%, #0d1b2e 100%);
  border: 2px solid #3498db;
}
#logo-ring-outer { position: relative; width: 100%; height: 100%; }
#logo-ring-inner {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
}
#logo-text {
  display: flex; flex-direction: column; align-items: center; z-index: 10;
}
#venue-name { font-size: 14px; font-weight: 700; color: #ffffff; }
#race-num { font-size: 24px; font-weight: 900; color: #3498db; }
#ring-canvas { position: absolute; inset: 0; pointer-events: none; }

#donut-card { display: flex; flex-direction: column; }
#donut-wrap { position: relative; flex: 1; display: flex; align-items: center; justify-content: center; }
#donutChart { max-width: 100%; max-height: 100%; }
#donut-center-val {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-size: 20px; font-weight: 900; color: #ffffff; pointer-events: none;
}

#mini-bar-card { display: flex; flex-direction: column; justify-content: center; padding: 6px 8px; }
.mini-kpi-row { display: flex; flex-direction: row; gap: 8px; height: 100%; align-items: center; justify-content: center; }
.mini-kpi { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.mini-kpi .card-title { font-size: 9px; margin-bottom: 4px; }
.mini-kpi canvas { max-height: 50px; width: 95%; margin: 0 auto; display: block; }
.kpi-val { font-size: 16px; font-weight: 800; margin-top: 4px; }
.accent-red { color: #e74c3c; }
.accent-yellow { color: #f39c12; }

#player-table-card {
  overflow: auto; padding: 4px 4px 0px 4px; display: flex; flex-direction: column;
  scrollbar-width: thin; scrollbar-color: #3498db #1a1f2e;
}
#player-table {
  width: 100%; border-collapse: collapse; font-size: 8px; color: #d0dae8;
}
#player-table thead th {
  background: #2563eb; color: white; padding: 2px 1px; text-align: center;
  position: sticky; top: 0; z-index: 10; font-size: 7px; font-weight: 700;
}
#player-table tbody td {
  padding: 8px 1px; text-align: center; border-bottom: 1px solid #2a3349; font-size: 8px;
}
#player-table tbody td:nth-child(2) {
  text-align: left; font-weight: 600; color: #ffffff;
}

#center-charts { display: flex; flex-direction: column; gap: 4px; overflow: hidden; max-height: 100%; }
.dot-row { display: flex; gap: 4px; flex: 1; min-height: 0; }
.dot-card { flex: 1; padding: 4px; display: flex; flex-direction: column; min-height: 0; }
.dot-card .card-title { font-size: 8px; margin-bottom: 2px; }
.dot-card canvas { width: 100% !important; height: 100% !important; }
.bottom-bar-row { display: flex; gap: 4px; flex: 1.1; min-height: 0; }
.bottom-bar-card { flex: 1; padding: 4px; display: flex; flex-direction: column; min-height: 0; }
.bottom-bar-card .card-title { font-size: 8px; margin-bottom: 2px; }
.bottom-bar-card canvas { width: 100% !important; height: 100% !important; }

#right-panels { display: flex; flex-direction: column; gap: 3px; max-height: 100%; overflow: hidden; }
.right-panel { padding: 3px; overflow: auto; flex: 1; min-height: 0; display: flex; flex-direction: column; }
.panel-header {
  font-size: 7px; font-weight: 700; color: #ffffff; margin-bottom: 3px;
  border-bottom: 1px solid #3498db; padding-bottom: 1px;
}
.data-table { width: 100%; border-collapse: collapse; font-size: 6px; }
.data-table th {
  background: #2563eb; color: white; padding: 1px; text-align: center; font-size: 6px;
}
.data-table td {
  padding: 1px; text-align: center; border-bottom: 1px solid #2a3349; color: #d0dae8; font-size: 6px;
}
.data-table td:first-child { text-align: left; font-weight: 600; color: #ffffff; }
.konsetsu-table { 
  width: 100%; 
  border-collapse: collapse; 
  font-size: 5px;
  background: #1a1f2e;
}
.konsetsu-table th {
  background: #2563eb; 
  color: white; 
  padding: 1px; 
  text-align: center; 
  font-size: 5px;
  border-right: 1px solid rgba(255,255,255,0.1);
}
.konsetsu-table td {
  padding: 1px; 
  text-align: center; 
  border-bottom: 1px solid #2a3349;
  border-right: 1px solid #2a3349;
  color: #d0dae8;
  font-size: 5px;
}
.konsetsu-table td:first-child {
  text-align: left;
  font-weight: 600;
  color: #ffffff;
  background: rgba(37, 99, 235, 0.2);
  font-size: 6px;
  padding-left: 2px;
}
.waku-cell {
  font-weight: 700;
  font-size: 6px;
  color: #fff;
}
.highlight { color: #ffffff; font-weight: 600; }
.val-high { color: #44ff88; font-weight: 700; }
.val-low { color: #ff6666; font-weight: 700; }

#konsetsu-container { overflow: auto; max-height: 100%; }
.konsetsu-grid {
  display: grid;
  grid-template-columns: 60px repeat(12, 1fr);
  font-size: 7px;
  color: #d0dae8;
  gap: 1px;
  background: #2a3349;
}
.ks-header {
  background: #2563eb;
  color: white;
  padding: 3px 2px;
  text-align: center;
  font-weight: 700;
  font-size: 7px;
}
.ks-header.name-col { grid-column: 1; }
.ks-header.day-col { grid-column: span 2; border-left: 1px solid rgba(255,255,255,0.2); }
.ks-subheader {
  background: #1e40af;
  color: white;
  padding: 2px;
  text-align: center;
  font-size: 6px;
}
.ks-name-cell {
  background: #1a1f2e;
  padding: 3px 4px;
  font-weight: 600;
  font-size: 7px;
  color: #ffffff;
  display: flex;
  align-items: center;
}
.ks-data-cell {
  background: #1a1f2e;
  padding: 2px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ks-waku {
  font-size: 9px;
  font-weight: 800;
  padding: 2px 4px;
  border-radius: 3px;
}
.waku-bg-1 { background: #ffffff; color: #000; }
.waku-bg-2 { background: #000000; color: #fff; }
.waku-bg-3 { background: #ff3333; color: #fff; }
.waku-bg-4 { background: #3333ff; color: #fff; }
.waku-bg-5 { background: #ffcc00; color: #000; }
.waku-bg-6 { background: #00aa00; color: #fff; }
"""

CHARTS_JS_TEMPLATE = """function createDonutChart(canvasId, val, maxVal, color) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['達成', '残り'],
      datasets: [{
        data: [val, Math.max(0, maxVal - val)],
        backgroundColor: [color, 'rgba(50,50,50,0.3)'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: true, cutout: '72%',
      plugins: { legend: { display: false }, tooltip: { enabled: false } }
    }
  });
}

function createMiniBarChart(canvasId, val, color) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [''],
      datasets: [{
        data: [val],
        backgroundColor: color,
        borderWidth: 0,
        barThickness: 50
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      layout: {
        padding: 0
      },
      scales: {
        x: { display: false },
        y: { display: false, max: 100 }
      },
      plugins: { legend: { display: false }, tooltip: { enabled: false } }
    }
  });
}

function createRentaiChart(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: datasets.map(ds => ({
        label: ds.label,
        data: ds.data,
        backgroundColor: ds.color,
        borderWidth: 0
      }))
    },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: {
        x: { 
          stacked: true,
          max: 100,
          ticks: { color: '#9bb2cc', font: { size: 7 } }, 
          grid: { color: '#333' } 
        },
        y: { 
          stacked: true,
          ticks: { color: '#ffffff', font: { size: 7 } }, 
          grid: { display: false } 
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true, callbacks: { label: (ctx) => ctx.dataset.label + ': ' + ctx.parsed.x.toFixed(1) + '%' } }
      }
    }
  });
}

function createHBarChart(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: datasets.map(ds => ({
        label: ds.label,
        data: ds.data,
        backgroundColor: ds.color,
        borderWidth: 0
      }))
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      layout: {
        padding: {
          bottom: 20
        }
      },
      scales: {
        x: { ticks: { color: '#ffffff', font: { size: 6 } }, grid: { display: false } },
        y: { 
          max: 50,
          ticks: { color: '#9bb2cc', font: { size: 7 }, callback: (val) => val + '%' }, 
          grid: { color: '#333' } 
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true, callbacks: { label: (ctx) => ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(1) + '%' } }
      }
    }
  });
}

function createDotChart(canvasId, points, isSTData = false) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  
  // データが空の場合は何も描画しない
  if (!points || points.length === 0) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = '#666';
    ctx.font = '8px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('データなし', ctx.canvas.width / 2, ctx.canvas.height / 2);
    return;
  }

  new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        data: points.map(p => ({ x: p.x, y: p.y })),
        backgroundColor: points.map(p => p.c),
        borderColor: '#ffffff',
        borderWidth: 0.5,
        pointRadius: 3
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: {
          type: 'linear',
          min: 0.5, max: 6.5,
          ticks: { 
            stepSize: 1, 
            color: '#9bb2cc', 
            font: { size: 8 },
            callback: function(value) {
              return Number.isInteger(value) ? value : '';
            }
          },
          grid: { color: '#333' },
          display: true
        },
        y: {
          type: 'linear',
          reverse: isSTData ? false : true,
          min: isSTData ? 0 : 0.5,
          max: isSTData ? 0.3 : 6.5,
          ticks: {
            stepSize: isSTData ? 0.05 : 1,
            color: '#9bb2cc',
            font: { size: 8 },
            callback: function(value) {
              if (isSTData) {
                return value.toFixed(2);
              } else {
                return Number.isInteger(value) ? value : '';
              }
            }
          },
          grid: { color: '#333' },
          display: true
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          enabled: true,
          callbacks: {
            label: (ctx) => {
              const p = ctx.raw;
              return isSTData ? `ST: ${p.y.toFixed(2)}` : `順位: ${p.y}`;
            }
          }
        }
      }
    }
  });
}

function createBarChart(canvasId, labels, values, colors) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: colors,
        borderWidth: 0
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      layout: {
        padding: {
          left: 5,
          right: 5,
          top: 5,
          bottom: 5
        }
      },
      scales: {
        x: { ticks: { color: '#ffffff', font: { size: 6 } }, grid: { display: false } },
        y: { 
          max: 50,
          ticks: { color: '#9bb2cc', font: { size: 7 }, callback: (val) => val + '%' }, 
          grid: { color: '#333' } 
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true, callbacks: { label: (ctx) => ctx.parsed.y.toFixed(1) + '%' } }
      }
    }
  });
}
"""

MAIN_JS_TEMPLATE = """document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('venue-name').textContent = RACE_INFO.venue;
  const raceNum = String(RACE_INFO.race).replace(/R$/i, '');
  document.getElementById('race-num').textContent = raceNum + 'R';
  
  createDonutChart('donutChart', KPI.donut.val, KPI.donut.max, KPI.donut.color);
  createMiniBarChart('miniBarChart1', KPI.miniBar1.val, KPI.miniBar1.color);
  createMiniBarChart('miniBarChart2', KPI.miniBar2.val, KPI.miniBar2.color);
  
  createHBarChart('hbarChart', HBAR_DATA.labels, HBAR_DATA.datasets);
  createRentaiChart('rentaiChart', RENTAI_DATA.labels, RENTAI_DATA.datasets);
  
  // ドットチャート（STデータと順位データを区別）
  if (DOT_DATA[0] && DOT_DATA[0].points.length > 0) {
    createDotChart('dot1', DOT_DATA[0].points, true);  // コース平均ST（数値）
  }
  if (DOT_DATA[1] && DOT_DATA[1].points.length > 0) {
    createDotChart('dot2', DOT_DATA[1].points, true);  // 今節平均ST（数値）
  }
  if (DOT_DATA[2] && DOT_DATA[2].points.length > 0) {
    createDotChart('dot3', DOT_DATA[2].points, false); // コース平均ST順位
  }
  if (DOT_DATA[3] && DOT_DATA[3].points.length > 0) {
    createDotChart('dot4', DOT_DATA[3].points, false); // 今節平均ST順位
  }
  
  createBarChart('bottomBar1', BOTTOM_BAR[0].labels, BOTTOM_BAR[0].values, BOTTOM_BAR[0].colors);
  createBarChart('bottomBar2', BOTTOM_BAR[1].labels, BOTTOM_BAR[1].values, BOTTOM_BAR[1].colors);
  
  renderPlayerTable(PLAYERS);
  renderStatsTable(STATS1, 'statsHead1', 'statsBody1');
  renderKonsetsuTable(KONSETSU_DATA);
  
  drawRingCanvas();
});

function renderPlayerTable(players) {
  const tbody = document.getElementById('player-tbody');
  tbody.innerHTML = '';
  players.forEach(p => {
    const tr = document.createElement('tr');
    
    // 0を"-"に変換する関数
    const displayNum = (val, decimals = 2) => {
      if (val === 0 || val === null || val === undefined) return '-';
      return val.toFixed(decimals);
    };
    
    tr.innerHTML = `
      <td style="font-weight:700;color:#ffffff">${p.boat}</td>
      <td style="text-align:left;font-weight:600;color:#ffffff">${p.name}</td>
      <td>${p.grade}</td>
      <td>${p.branch}</td>
      <td>${p.fl}</td>
      <td style="color:#f0f4ff;font-weight:600">${displayNum(p.nation_rate)}</td>
      <td style="color:#c8d8f0">${displayNum(p.local_rate)}</td>
      <td><span style="font-size:10px;font-weight:bold">${p.m_eval}</span></td>
      <td style="color:${p.motor_color};font-weight:600">${p.motor_type}</td>
      <td style="color:#9bb2cc">${p.point}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderStatsTable(stats, headId, bodyId) {
  const thead = document.getElementById(headId); const tbody = document.getElementById(bodyId);
  thead.innerHTML = `<tr>${stats.headers.map(h => `<th>${h}</th>`).join('')}</tr>`;
  tbody.innerHTML = '';
  stats.rows.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = row.map((cell, ci) => {
      if (ci === 0) return `<td style="text-align:left;color:#d0dae8;font-weight:500">${cell}</td>`;
      
      // 0や空欄を"-"に統一
      let displayValue = cell;
      const num = parseFloat(cell);
      if (cell === '' || cell === null || cell === undefined || (cell === '0' || cell === '0.0' || num === 0)) {
        displayValue = '-';
      }
      
      let cls = 'highlight';
      if (!isNaN(num) && num > 0) {
        if (num >= 30 || cell.includes('%') && parseFloat(cell) >= 40) cls = 'val-high';
        else if (num <= 5) cls = 'val-low';
      }
      return `<td class="${cls}">${displayValue}</td>`;
    }).join('');
    tbody.appendChild(tr);
  });
}

function renderKonsetsuTable(konsetsu) {
  const thead = document.getElementById('konsetsuHead');
  const tbody = document.getElementById('konsetsuBody');
  
  // ヘッダー作成
  let headerHTML = '<tr><th>選手</th>';
  for (let day = 1; day <= 6; day++) {
    headerHTML += `<th colspan="2">${day}日目</th>`;
  }
  headerHTML += '</tr>';
  thead.innerHTML = headerHTML;
  
  // ボディ作成
  tbody.innerHTML = '';
  konsetsu.forEach(player => {
    const tr = document.createElement('tr');
    let rowHTML = `<td>${player.name}</td>`;
    for (let day = 1; day <= 6; day++) {
      const run1 = player.results[`${day}-1`] || '';
      const run2 = player.results[`${day}-2`] || '';
      const display1 = run1 && run1 !== '' && run1 !== '-' ? `<span class="waku-cell">${run1}</span>` : '-';
      const display2 = run2 && run2 !== '' && run2 !== '-' ? `<span class="waku-cell">${run2}</span>` : '-';
      rowHTML += `<td>${display1}</td>`;
      rowHTML += `<td>${display2}</td>`;
    }
    tr.innerHTML = rowHTML;
    tbody.appendChild(tr);
  });
}

function drawRingCanvas() {
  const canvas = document.getElementById('ring-canvas'); if (!canvas) return;
  const dpr = window.devicePixelRatio || 1;
  const W = canvas.parentElement.offsetWidth; const H = canvas.parentElement.offsetHeight;
  canvas.width = W * dpr; canvas.height = H * dpr;
  canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
  const ctx = canvas.getContext('2d'); ctx.scale(dpr, dpr);
  const cx = W / 2; const cy = H / 2; const R = Math.min(W, H) / 2 - 4;
  
  const grad1 = ctx.createLinearGradient(cx - R, cy, cx + R, cy);
  grad1.addColorStop(0, 'rgba(30,144,255,0.0)'); grad1.addColorStop(0.5, 'rgba(120,200,255,1.0)'); grad1.addColorStop(1, 'rgba(30,144,255,0.0)');
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.strokeStyle = grad1; ctx.lineWidth = 2.5; ctx.stroke();

  const grad2 = ctx.createLinearGradient(cx, cy - R, cx, cy + R);
  grad2.addColorStop(0, 'rgba(255,200,0,0.0)'); grad2.addColorStop(0.5, 'rgba(255,80,0,1.0)'); grad2.addColorStop(1, 'rgba(255,200,0,0.0)');
  ctx.beginPath(); ctx.arc(cx, cy, R - 6, 0, Math.PI * 2); ctx.strokeStyle = grad2; ctx.lineWidth = 3.5; ctx.stroke();
}
window.addEventListener('resize', drawRingCanvas);
"""

# ============================================================
# データパース & 出力ロジック
# ============================================================

def generate_dashboard_data(csv_path, output_dir="dist2"):
    df = pd.read_csv(csv_path)
    
    # カラム名の正規化
    df.columns = df.columns.str.strip().str.replace('‐', '-').str.replace('−', '-')
    
    grouped = df.groupby(['レース場', 'レース回'])
    
    for (place, round_no), group in grouped:
        group = group.sort_values('枠番')
        
        players_list = []
        for _, row in group.iterrows():
            # 今節成績の文字列連結ロジック
            res_list = []
            for j in range(1, 7):
                for k in range(1, 3):
                    val = row.get(f'今節成績_{j}-{k}')
                    if pd.notna(val) and str(val).strip() != '-' and str(val).strip() != '':
                        try:
                            res_list.append(str(int(float(val))))
                        except:
                            pass
            results_str = " ".join(res_list) if res_list else "-"
            
            # M総合評価のマッピング
            m_eval = safe_str(row['M総合評価'], default="-")
            m_eval_map = {'S': '超絶', 'A': '上位', 'B': '中堅上位', 'C': '中堅下位', 'D': '下位'}
            m_eval_display = m_eval_map.get(m_eval, '-')
            
            # モーター型の判定
            deashi_val = safe_float(row.get('出足'))
            nobashi_val = safe_float(row.get('伸び足'))
            
            if deashi_val == 0 and nobashi_val == 0:
                motor_type = '-'
                motor_color = '#ffffff'
            else:
                if deashi_val > nobashi_val:
                    motor_type = '出足型'
                elif nobashi_val > deashi_val:
                    motor_type = '伸び型'
                else:
                    motor_type = 'バランス型'
                motor_color = '#ff6b6b' if (deashi_val >= 4 or nobashi_val >= 4) else '#ffffff'
            
            # pointの生成
            m_shisu = safe_float(row['M指数'])
            if m_shisu >= 5:
                m_rank = 'S'
            elif m_shisu >= 4:
                m_rank = 'A'
            elif m_shisu >= 3:
                m_rank = 'B'
            elif m_shisu >= 2:
                m_rank = 'C'
            elif m_shisu >= 1:
                m_rank = 'D'
            else:
                m_rank = '-'
            
            activepoint_str = safe_str(row.get('activepoint', '-'))
            ap_map = {
                'S+': '++++', 'S': '+++',
                'A+': '++', 'A': '+',
                'B+': '+-', 'B': '-',
                'C+': '--', 'C': '--',
                'D+': '---', 'D': '---'
            }
            ap_symbol = ap_map.get(activepoint_str, '')
            point_display = f"{m_rank}{ap_symbol}" if m_rank != '-' and ap_symbol else '-'
            
            p_dict = {
                "boat": int(row['枠番']),
                "name": safe_str(row['選手名']),
                "grade": safe_str(row['級別']),
                "branch": safe_str(row['支部']),
                "fl": safe_str(row['FL'], default="-"),
                "nation_rate": safe_float(row['全国勝率']),
                "local_rate": safe_float(row['当地勝率']),
                "m_eval": m_eval_display,
                "motor_type": motor_type,
                "motor_color": motor_color,
                "point": point_display
            }
            players_list.append(p_dict)
            
        # 1枠の1着率をドーナツチャートに表示（%で）
        first_row = group.iloc[0]
        first_1chakuritsu = safe_float(first_row.get('1着率'))
        donut_val = first_1chakuritsu * 100 if first_1chakuritsu <= 1.0 else first_1chakuritsu
        
        # 1枠の1-2率、1-3率を上部ミニKPIへマッピング（%で）
        rate_1_2 = safe_float(first_row.get('1-2率'))
        rate_1_2_percent = rate_1_2 * 100 if rate_1_2 <= 1.0 else rate_1_2
        rate_1_3 = safe_float(first_row.get('1-3率'))
        rate_1_3_percent = rate_1_3 * 100 if rate_1_3 <= 1.0 else rate_1_3
        
        # 右パネル1の構築（2着がX号艇 マトリックス）
        matrix_rows = []
        for _, row in group.iterrows():
            matrix_rows.append([
                f"{int(row['枠番'])}",
                f"{safe_float(row.get('2着が1号艇')):.0f}",
                f"{safe_float(row.get('2着が2号艇')):.0f}",
                f"{safe_float(row.get('2着が3号艇')):.0f}",
                f"{safe_float(row.get('2着が4号艇')):.0f}",
                f"{safe_float(row.get('2着が5号艇')):.0f}",
                f"{safe_float(row.get('2着が6号艇')):.0f}"
            ])
            
        # 今節成績データの構築
        dot_data_list = []
        colors_by_waku = ["#FFFFFF", "#000000", "#FF3333", "#3333FF", "#FFCC00", "#00AA00"]
        
        # 1. コース平均ST
        dot1_points = []
        for idx, row in group.iterrows():
            waku = int(row['枠番'])
            val = safe_float(row.get('コース平均st'), default=0.0)
            if val > 0:  # 有効なデータのみ
                dot1_points.append({
                    "x": waku,
                    "y": val,
                    "c": colors_by_waku[waku - 1] if 1 <= waku <= 6 else colors_by_waku[0]
                })
        dot_data_list.append({"points": dot1_points})
        
        # 2. 今節平均ST
        dot2_points = []
        for idx, row in group.iterrows():
            waku = int(row['枠番'])
            val = safe_float(row.get('今節平均st'), default=0.0)
            if val > 0:  # 有効なデータのみ
                dot2_points.append({
                    "x": waku,
                    "y": val,
                    "c": colors_by_waku[waku - 1] if 1 <= waku <= 6 else colors_by_waku[0]
                })
        dot_data_list.append({"points": dot2_points})
        
        # 3. コース平均ST順位
        dot3_points = []
        for idx, row in group.iterrows():
            waku = int(row['枠番'])
            val = safe_float(row.get('コース平均st順位'), default=0.0)
            if val > 0:  # 有効なデータのみ
                dot3_points.append({
                    "x": waku,
                    "y": val,
                    "c": colors_by_waku[waku - 1] if 1 <= waku <= 6 else colors_by_waku[0]
                })
        dot_data_list.append({"points": dot3_points})
        
        # 4. 今節平均ST順位
        dot4_points = []
        for idx, row in group.iterrows():
            waku = int(row['枠番'])
            val = safe_float(row.get('今節平均st順位'), default=0.0)
            if val > 0:  # 有効なデータのみ
                dot4_points.append({
                    "x": waku,
                    "y": val,
                    "c": colors_by_waku[waku - 1] if 1 <= waku <= 6 else colors_by_waku[0]
                })
        dot_data_list.append({"points": dot4_points})
        
        # 下部バーチャート用データ（2つ）
        bottom_bar_list = []
        
        # 1. コースSTトップ率
        top_rate_values = []
        for _, row in group.iterrows():
            val = safe_float(row.get('コースstトップ率'))
            percent = val * 100 if val <= 1.0 else val
            top_rate_values.append(percent)
        
        bottom_bar_list.append({
            "labels": ["1", "2", "3", "4", "5", "6"],
            "values": top_rate_values,
            "colors": ["#1e90ff"] * 6
        })
        
        # 2. コースST最下位率
        bottom_rate_values = []
        for _, row in group.iterrows():
            val = safe_float(row.get('コースst最下位率'))
            percent = val * 100 if val <= 1.0 else val
            bottom_rate_values.append(percent)
        
        bottom_bar_list.append({
            "labels": ["1", "2", "3", "4", "5", "6"],
            "values": bottom_rate_values,
            "colors": ["#e74c3c"] * 6
        })
            
        # 今節成績データの構築
        konsetsu_data = []
        for _, row in group.iterrows():
            player_results = {"name": safe_str(row['選手名']), "results": {}}
            for day in range(1, 7):
                for run in range(1, 3):
                    col_name = f'今節成績_{day}-{run}'
                    waku_val = row.get(col_name, '')
                    if pd.notna(waku_val) and str(waku_val).strip() not in ['', '-', 'nan']:
                        try:
                            player_results["results"][f'{day}-{run}'] = str(int(float(waku_val)))
                        except:
                            player_results["results"][f'{day}-{run}'] = ''
                    else:
                        player_results["results"][f'{day}-{run}'] = ''
            konsetsu_data.append(player_results)
            
        race_payload = {
            "RACE_INFO": {"venue": place, "race": round_no},
            "PLAYERS": players_list,
            "KPI": {
                "donut": {"val": donut_val, "max": 100.0, "color": "#ffffff"},
                "miniBar1": {"val": rate_1_2_percent, "color": "#000000"},
                "miniBar2": {"val": rate_1_3_percent, "color": "#dc2626"}
            },
            "RENTAI_DATA": {
                "labels": [p['name'] for p in players_list],
                "datasets": [
                    {
                        "label": "1着", 
                        "data": [safe_float(r.get('1着率')) * 100 if safe_float(r.get('1着率')) <= 1.0 else safe_float(r.get('1着率')) for _, r in group.iterrows()], 
                        "color": "#444444"
                    },
                    {
                        "label": "2着", 
                        "data": [safe_float(r.get('2着率')) * 100 if safe_float(r.get('2着率')) <= 1.0 else safe_float(r.get('2着率')) for _, r in group.iterrows()], 
                        "color": "#888888"
                    },
                    {
                        "label": "3着", 
                        "data": [safe_float(r.get('3着率')) * 100 if safe_float(r.get('3着率')) <= 1.0 else safe_float(r.get('3着率')) for _, r in group.iterrows()], 
                        "color": "#CCCCCC"
                    }
                ]
            },
            "HBAR_DATA": {
                "labels": [p['name'] for p in players_list],
                "datasets": [
                    {
                        "label": "差し", 
                        "data": [safe_float(r.get('差し率')) * 100 if safe_float(r.get('差し率')) <= 1.0 else safe_float(r.get('差し率')) for _, r in group.iterrows()], 
                        "color": "#FFFFFF"
                    },
                    {
                        "label": "まくり", 
                        "data": [safe_float(r.get('まくり率')) * 100 if safe_float(r.get('まくり率')) <= 1.0 else safe_float(r.get('まくり率')) for _, r in group.iterrows()], 
                        "color": "#FF3333"
                    },
                    {
                        "label": "まくり差し", 
                        "data": [safe_float(r.get('まくり差し率')) * 100 if safe_float(r.get('まくり差し率')) <= 1.0 else safe_float(r.get('まくり差し率')) for _, r in group.iterrows()], 
                        "color": "#FFCC00"
                    }
                ]
            },
            "DOT_DATA": dot_data_list,
            "BOTTOM_BAR": bottom_bar_list,
            "STATS1": {
                "headers": ["選手", "1", "2", "3", "4", "5", "6"],
                "rows": [[p['name'], *row[1:]] for p, row in zip(players_list, matrix_rows)]
            },
            "KONSETSU_DATA": konsetsu_data
        }
        
        race_dir = os.path.join(output_dir, f"{place}_{round_no}")
        css_dir = os.path.join(race_dir, "css")
        js_dir = os.path.join(race_dir, "js")
        
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)
        
        with open(os.path.join(race_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(HTML_TEMPLATE)
        with open(os.path.join(css_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write(CSS_TEMPLATE)
        with open(os.path.join(js_dir, "charts.js"), "w", encoding="utf-8") as f:
            f.write(CHARTS_JS_TEMPLATE)
        with open(os.path.join(js_dir, "main.js"), "w", encoding="utf-8") as f:
            f.write(MAIN_JS_TEMPLATE)
            
        js_content = f"""const RACE_INFO = {json.dumps(race_payload['RACE_INFO'], ensure_ascii=False, indent=2)};
const PLAYERS = {json.dumps(race_payload['PLAYERS'], ensure_ascii=False, indent=2)};
const KPI = {json.dumps(race_payload['KPI'], ensure_ascii=False, indent=2)};
const RENTAI_DATA = {json.dumps(race_payload['RENTAI_DATA'], ensure_ascii=False, indent=2)};
const HBAR_DATA = {json.dumps(race_payload['HBAR_DATA'], ensure_ascii=False, indent=2)};
const DOT_DATA = {json.dumps(race_payload['DOT_DATA'], ensure_ascii=False, indent=2)};
const BOTTOM_BAR = {json.dumps(race_payload['BOTTOM_BAR'], ensure_ascii=False, indent=2)};
const STATS1 = {json.dumps(race_payload['STATS1'], ensure_ascii=False, indent=2)};
const KONSETSU_DATA = {json.dumps(race_payload['KONSETSU_DATA'], ensure_ascii=False, indent=2)};"""

        with open(os.path.join(js_dir, "data.js"), "w", encoding="utf-8") as f:
            f.write(js_content)
            
    print(f"成功: {len(grouped)} レース分のパッケージを '{output_dir}' フォルダ内に生成しました。")

if __name__ == "__main__":import pandas as pd
import json
import os

def safe_float(value, default=0.0):
    try:
        val_str = str(value).strip()
        if val_str in ['#N/A!', '#N/A', 'NaN', 'nan', 'null', '']:
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_str(value, default="-"):
    if pd.isna(value):
        return default
    val_str = str(value).strip()
    if val_str in ['#N/A!', '#N/A', 'NaN', 'nan', 'null', '', 'F0']:
        return default
    return val_str

# ============================================================
# HTML / CSS テンプレート
# ============================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ボートレース 分析ダッシュボード</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div id="phone-scene">
  <div id="phone-frame">
    <div id="phone-notch">
      <div id="notch-camera"></div>
      <div id="notch-speaker"></div>
    </div>
    <div id="phone-screen">
<div id="dashboard">
  <div id="top-row">
    <div class="card" id="logo-card">
      <div id="logo-ring-outer">
        <div id="logo-ring-inner">
          <div id="logo-text">
            <span id="venue-name">--</span>
            <span id="race-num">--</span>
          </div>
        </div>
        <canvas id="ring-canvas"></canvas>
      </div>
    </div>
    <div class="card" id="donut-card">
      <div class="card-title" id="target-player-name">In逃げ率</div>
      <div id="donut-wrap">
        <canvas id="donutChart"></canvas>
        <div id="donut-center-val">--</div>
      </div>
    </div>
    <div class="card" id="mini-bar-card">
      <div class="mini-kpi-row">
        <div class="mini-kpi">
          <div class="card-title">1-2率</div>
          <canvas id="miniBarChart1"></canvas>
          <div class="kpi-val accent-red" id="kpi-1-2">--%</div>
        </div>
        <div class="mini-kpi">
          <div class="card-title">1-3率</div>
          <canvas id="miniBarChart2"></canvas>
          <div class="kpi-val accent-yellow" id="kpi-1-3">--%</div>
        </div>
      </div>
    </div>
    <div class="card" id="hbar-card">
      <div class="card-title">決まり手データ</div>
      <canvas id="hbarChart"></canvas>
    </div>
    <div class="card" id="rentai-card">
      <div class="card-title-row">
        <span class="card-title">3連対率</span>
        <div class="legend-row">
          <span class="legend-dot" style="background:#444444"></span><span>1着</span>
          <span class="legend-dot" style="background:#888888"></span><span>2着</span>
          <span class="legend-dot" style="background:#CCCCCC"></span><span>3着</span>
        </div>
      </div>
      <canvas id="rentaiChart"></canvas>
    </div>
  </div>
  <div id="bottom-row">
    <div class="card" id="player-table-card">
      <table id="player-table">
        <thead>
          <tr>
            <th>艇</th>
            <th>選手名</th>
            <th>級別</th>
            <th>支部</th>
            <th>FL</th>
            <th>全国勝率</th>
            <th>当地勝率</th>
            <th>評価</th>
            <th>モーター</th>
            <th>point</th>
          </tr>
        </thead>
        <tbody id="player-tbody"></tbody>
      </table>
    </div>
    <div id="center-charts">
      <div class="dot-row">
        <div class="card dot-card">
          <div class="card-title">コース平均ST</div>
          <canvas id="dot1"></canvas>
        </div>
        <div class="card dot-card">
          <div class="card-title">今節平均ST</div>
          <canvas id="dot2"></canvas>
        </div>
      </div>
      <div class="dot-row">
        <div class="card dot-card">
          <div class="card-title">コース平均ST順位</div>
          <canvas id="dot3"></canvas>
        </div>
        <div class="card dot-card">
          <div class="card-title">今節平均ST順位</div>
          <canvas id="dot4"></canvas>
        </div>
      </div>
      <div class="bottom-bar-row">
        <div class="card bottom-bar-card">
          <div class="card-title">コースSTトップ率</div>
          <canvas id="bottomBar1"></canvas>
        </div>
        <div class="card bottom-bar-card">
          <div class="card-title">コースST最下位率</div>
          <canvas id="bottomBar2"></canvas>
        </div>
      </div>
    </div>
    <div id="right-panels">
      <div class="card right-panel" id="right-panel-top">
        <div class="panel-header">枠番進入・1着時2着傾向</div>
        <table class="data-table" id="statsTable1">
          <thead id="statsHead1"></thead>
          <tbody id="statsBody1"></tbody>
        </table>
      </div>
      <div class="card right-panel" id="right-panel-bottom">
        <div class="panel-header">今節成績</div>
        <table class="konsetsu-table" id="konsetsuTable">
          <thead id="konsetsuHead"></thead>
          <tbody id="konsetsuBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>
    </div>
  </div>
</div>
<script src="js/data.js"></script>
<script src="js/charts.js"></script>
<script src="js/main.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('donut-center-val').textContent = KPI.donut.val.toFixed(0) + '%';
    document.getElementById('kpi-1-2').textContent = (KPI.miniBar1.val).toFixed(0) + '%';
    document.getElementById('kpi-1-3').textContent = (KPI.miniBar2.val).toFixed(0) + '%';
    if(PLAYERS && PLAYERS.length > 0) {
      const playerNameDiv = document.createElement('div');
      playerNameDiv.style.cssText = 'position:absolute;top:37%;left:50%;transform:translate(-50%,-50%);font-size:10px;color:#ffffff;font-weight:600;';
      playerNameDiv.textContent = PLAYERS[0].name;
      document.getElementById('donut-wrap').appendChild(playerNameDiv);
    }
  });
</script>
</body>
</html>"""

CSS_TEMPLATE = """*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
#phone-scene {
  width: 100vw; height: 100vh;
  background: radial-gradient(ellipse at 50% 50%, #1a2035 0%, #080c14 100%);
  display: flex; align-items: center; justify-content: center; overflow: hidden;
}
#phone-frame {
  position: relative; width: min(96vw, 170vh); aspect-ratio: 16 / 7.5;
  background: linear-gradient(145deg, #2a2f3d 0%, #1a1d28 40%, #0f1118 100%);
  border-radius: 40px;
  box-shadow: 0 50px 100px rgba(0,0,0,0.7), inset 0 2px 4px rgba(255,255,255,0.05);
}
#phone-notch {
  position: absolute; top: 0; left: 50%; transform: translateX(-50%);
  width: 180px; height: 30px; background: #0a0c10; border-radius: 0 0 18px 18px; z-index: 100;
  display: flex; align-items: center; justify-content: center; gap: 10px;
}
#notch-camera { width: 12px; height: 12px; border-radius: 50%; background: #1a1d24; box-shadow: inset 0 1px 2px rgba(0,0,0,0.4); }
#notch-speaker { width: 50px; height: 4px; border-radius: 2px; background: #0e1014; }
#phone-screen {
  position: absolute; inset: 14px; border-radius: 30px; overflow: hidden;
  background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
}
#dashboard {
  width: 100%; height: 100%; display: flex; flex-direction: column; gap: 6px; padding: 12px 10px;
  overflow-y: auto; overflow-x: hidden;
  scrollbar-width: thin; scrollbar-color: #3498db #1a1f2e;
}
#dashboard::-webkit-scrollbar { width: 4px; }
#dashboard::-webkit-scrollbar-track { background: #1a1f2e; border-radius: 2px; }
#dashboard::-webkit-scrollbar-thumb { background: #3498db; border-radius: 2px; }
#top-row, #bottom-row { display: grid; gap: 6px; }
#top-row { grid-template-columns: 1fr 0.7fr 0.7fr 1.3fr 1.3fr; height: 160px; }
#bottom-row { grid-template-columns: 1.7fr 1.5fr 0.7fr; max-height: 480px; overflow: hidden; }

.card {
  background: linear-gradient(135deg, #1e2538 0%, #151823 100%);
  border: 1px solid rgba(52, 152, 219, 0.2);
  border-radius: 6px; padding: 6px; overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
}
.card-title {
  font-size: 9px; font-weight: 600; color: #9bb2cc; margin-bottom: 4px;
  text-align: center; text-transform: uppercase; letter-spacing: 0.2px;
}
.card-title-row {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 6px; font-size: 10px; font-weight: 600; color: #9bb2cc;
}
.legend-row { display: flex; gap: 6px; align-items: center; font-size: 8px; }
.legend-dot { width: 8px; height: 8px; border-radius: 2px; display: inline-block; }

#logo-card {
  display: flex; align-items: center; justify-content: center;
  background: radial-gradient(circle, #1e3a5f 0%, #0d1b2e 100%);
  border: 2px solid #3498db;
}
#logo-ring-outer { position: relative; width: 100%; height: 100%; }
#logo-ring-inner {
  position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
}
#logo-text {
  display: flex; flex-direction: column; align-items: center; z-index: 10;
}
#venue-name { font-size: 14px; font-weight: 700; color: #ffffff; }
#race-num { font-size: 24px; font-weight: 900; color: #3498db; }
#ring-canvas { position: absolute; inset: 0; pointer-events: none; }

#donut-card { display: flex; flex-direction: column; }
#donut-wrap { position: relative; flex: 1; display: flex; align-items: center; justify-content: center; }
#donutChart { max-width: 100%; max-height: 100%; }
#donut-center-val {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
  font-size: 20px; font-weight: 900; color: #ffffff; pointer-events: none;
}

#mini-bar-card { display: flex; flex-direction: column; justify-content: center; padding: 6px 8px; }
.mini-kpi-row { display: flex; flex-direction: row; gap: 8px; height: 100%; align-items: center; justify-content: center; }
.mini-kpi { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.mini-kpi .card-title { font-size: 9px; margin-bottom: 4px; }
.mini-kpi canvas { max-height: 50px; width: 95%; margin: 0 auto; display: block; }
.kpi-val { font-size: 16px; font-weight: 800; margin-top: 4px; }
.accent-red { color: #e74c3c; }
.accent-yellow { color: #f39c12; }

#player-table-card {
  overflow: auto; padding: 4px 4px 0px 4px; display: flex; flex-direction: column;
  scrollbar-width: thin; scrollbar-color: #3498db #1a1f2e;
}
#player-table {
  width: 100%; border-collapse: collapse; font-size: 8px; color: #d0dae8;
}
#player-table thead th {
  background: #2563eb; color: white; padding: 2px 1px; text-align: center;
  position: sticky; top: 0; z-index: 10; font-size: 7px; font-weight: 700;
}
#player-table tbody td {
  padding: 9px 1px; text-align: center; border-bottom: 1px solid #2a3349; font-size: 8px;
}
#player-table tbody td:nth-child(2) {
  text-align: left; font-weight: 600; color: #ffffff;
}

#center-charts { display: flex; flex-direction: column; gap: 4px; overflow: hidden; max-height: 100%; }
.dot-row { display: flex; gap: 4px; flex: 1; min-height: 0; }
.dot-card { flex: 1; padding: 4px; display: flex; flex-direction: column; min-height: 0; }
.dot-card .card-title { font-size: 8px; margin-bottom: 2px; }
.dot-card canvas { width: 100% !important; height: 100% !important; }
.bottom-bar-row { display: flex; gap: 4px; flex: 1.1; min-height: 0; }
.bottom-bar-card { flex: 1; padding: 4px; display: flex; flex-direction: column; min-height: 0; }
.bottom-bar-card .card-title { font-size: 8px; margin-bottom: 2px; }
.bottom-bar-card canvas { width: 100% !important; height: 100% !important; }

#right-panels { display: flex; flex-direction: column; gap: 3px; max-height: 100%; overflow: hidden; }
.right-panel { padding: 3px; overflow: auto; flex: 1; min-height: 0; display: flex; flex-direction: column; }
.panel-header {
  font-size: 7px; font-weight: 700; color: #ffffff; margin-bottom: 3px;
  border-bottom: 1px solid #3498db; padding-bottom: 1px;
}
.data-table { width: 100%; border-collapse: collapse; font-size: 6px; }
.data-table th {
  background: #2563eb; color: white; padding: 1px; text-align: center; font-size: 6px;
}
.data-table td {
  padding: 2px 1px; text-align: center; border-bottom: 1px solid #2a3349; color: #d0dae8; font-size: 6px;
}
.data-table td:first-child { text-align: left; font-weight: 600; color: #ffffff; }
.konsetsu-table { 
  width: 100%; 
  border-collapse: collapse; 
  font-size: 5px;
  background: #1a1f2e;
}
.konsetsu-table th {
  background: #2563eb; 
  color: white; 
  padding: 1px; 
  text-align: center; 
  font-size: 5px;
  border-right: 1px solid rgba(255,255,255,0.1);
}
.konsetsu-table td {
  padding: 2px 1px; 
  text-align: center; 
  border-bottom: 1px solid #2a3349;
  border-right: 1px solid #2a3349;
  color: #d0dae8;
  font-size: 5px;
}
.konsetsu-table td:first-child {
  text-align: left;
  font-weight: 600;
  color: #ffffff;
  background: rgba(37, 99, 235, 0.2);
  font-size: 6px;
  padding-left: 2px;
}
.waku-cell {
  font-weight: 700;
  font-size: 6px;
  color: #fff;
}
.highlight { color: #ffffff; font-weight: 600; }
.val-high { color: #44ff88; font-weight: 700; }
.val-low { color: #ff6666; font-weight: 700; }

#konsetsu-container { overflow: auto; max-height: 100%; }
.konsetsu-grid {
  display: grid;
  grid-template-columns: 60px repeat(12, 1fr);
  font-size: 7px;
  color: #d0dae8;
  gap: 1px;
  background: #2a3349;
}
.ks-header {
  background: #2563eb;
  color: white;
  padding: 3px 2px;
  text-align: center;
  font-weight: 700;
  font-size: 7px;
}
.ks-header.name-col { grid-column: 1; }
.ks-header.day-col { grid-column: span 2; border-left: 1px solid rgba(255,255,255,0.2); }
.ks-subheader {
  background: #1e40af;
  color: white;
  padding: 2px;
  text-align: center;
  font-size: 6px;
}
.ks-name-cell {
  background: #1a1f2e;
  padding: 3px 4px;
  font-weight: 600;
  font-size: 7px;
  color: #ffffff;
  display: flex;
  align-items: center;
}
.ks-data-cell {
  background: #1a1f2e;
  padding: 2px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
.ks-waku {
  font-size: 9px;
  font-weight: 800;
  padding: 2px 4px;
  border-radius: 3px;
}
.waku-bg-1 { background: #ffffff; color: #000; }
.waku-bg-2 { background: #000000; color: #fff; }
.waku-bg-3 { background: #ff3333; color: #fff; }
.waku-bg-4 { background: #3333ff; color: #fff; }
.waku-bg-5 { background: #ffcc00; color: #000; }
.waku-bg-6 { background: #00aa00; color: #fff; }
"""

CHARTS_JS_TEMPLATE = """function createDonutChart(canvasId, val, maxVal, color) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['達成', '残り'],
      datasets: [{
        data: [val, Math.max(0, maxVal - val)],
        backgroundColor: [color, 'rgba(50,50,50,0.3)'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: true, cutout: '72%',
      plugins: { legend: { display: false }, tooltip: { enabled: false } }
    }
  });
}

function createMiniBarChart(canvasId, val, color) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [''],
      datasets: [{
        data: [val],
        backgroundColor: color,
        borderWidth: 0,
        barThickness: 50
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      layout: {
        padding: 0
      },
      scales: {
        x: { display: false },
        y: { display: false, max: 100 }
      },
      plugins: { legend: { display: false }, tooltip: { enabled: false } }
    }
  });
}

function createRentaiChart(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: datasets.map(ds => ({
        label: ds.label,
        data: ds.data,
        backgroundColor: ds.color,
        borderWidth: 0
      }))
    },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: false,
      scales: {
        x: { 
          stacked: true,
          max: 100,
          ticks: { color: '#9bb2cc', font: { size: 7 } }, 
          grid: { color: '#333' } 
        },
        y: { 
          stacked: true,
          ticks: { color: '#ffffff', font: { size: 7 } }, 
          grid: { display: false } 
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true, callbacks: { label: (ctx) => ctx.dataset.label + ': ' + ctx.parsed.x.toFixed(1) + '%' } }
      }
    }
  });
}

function createHBarChart(canvasId, labels, datasets) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: datasets.map(ds => ({
        label: ds.label,
        data: ds.data,
        backgroundColor: ds.color,
        borderWidth: 0
      }))
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      layout: {
        padding: {
          bottom: 20
        }
      },
      scales: {
        x: { ticks: { color: '#ffffff', font: { size: 6 } }, grid: { display: false } },
        y: { 
          max: 50,
          ticks: { color: '#9bb2cc', font: { size: 7 }, callback: (val) => val + '%' }, 
          grid: { color: '#333' } 
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true, callbacks: { label: (ctx) => ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(1) + '%' } }
      }
    }
  });
}

function createDotChart(canvasId, points, isSTData = false) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  
  // データが空の場合は何も描画しない
  if (!points || points.length === 0) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.fillStyle = '#666';
    ctx.font = '8px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('データなし', ctx.canvas.width / 2, ctx.canvas.height / 2);
    return;
  }

  new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        data: points.map(p => ({ x: p.x, y: p.y })),
        backgroundColor: points.map(p => p.c),
        borderColor: '#ffffff',
        borderWidth: 0.5,
        pointRadius: 3
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        x: {
          type: 'linear',
          min: 0.5, max: 6.5,
          ticks: { 
            stepSize: 1, 
            color: '#9bb2cc', 
            font: { size: 8 },
            callback: function(value) {
              return Number.isInteger(value) ? value : '';
            }
          },
          grid: { color: '#333' },
          display: true
        },
        y: {
          type: 'linear',
          reverse: isSTData ? false : true,
          min: isSTData ? 0 : 0.5,
          max: isSTData ? 0.3 : 6.5,
          ticks: {
            stepSize: isSTData ? 0.05 : 1,
            color: '#9bb2cc',
            font: { size: 8 },
            callback: function(value) {
              if (isSTData) {
                return value.toFixed(2);
              } else {
                return Number.isInteger(value) ? value : '';
              }
            }
          },
          grid: { color: '#333' },
          display: true
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          enabled: true,
          callbacks: {
            label: (ctx) => {
              const p = ctx.raw;
              return isSTData ? `ST: ${p.y.toFixed(2)}` : `順位: ${p.y}`;
            }
          }
        }
      }
    }
  });
}

function createBarChart(canvasId, labels, values, colors) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: colors,
        borderWidth: 0
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      layout: {
        padding: {
          left: 5,
          right: 5,
          top: 5,
          bottom: 5
        }
      },
      scales: {
        x: { ticks: { color: '#ffffff', font: { size: 6 } }, grid: { display: false } },
        y: { 
          max: 50,
          ticks: { color: '#9bb2cc', font: { size: 7 }, callback: (val) => val + '%' }, 
          grid: { color: '#333' } 
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true, callbacks: { label: (ctx) => ctx.parsed.y.toFixed(1) + '%' } }
      }
    }
  });
}
"""

MAIN_JS_TEMPLATE = """document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('venue-name').textContent = RACE_INFO.venue;
  const raceNum = String(RACE_INFO.race).replace(/R$/i, '');
  document.getElementById('race-num').textContent = raceNum + 'R';
  
  createDonutChart('donutChart', KPI.donut.val, KPI.donut.max, KPI.donut.color);
  createMiniBarChart('miniBarChart1', KPI.miniBar1.val, KPI.miniBar1.color);
  createMiniBarChart('miniBarChart2', KPI.miniBar2.val, KPI.miniBar2.color);
  
  createHBarChart('hbarChart', HBAR_DATA.labels, HBAR_DATA.datasets);
  createRentaiChart('rentaiChart', RENTAI_DATA.labels, RENTAI_DATA.datasets);
  
  // ドットチャート（STデータと順位データを区別）
  if (DOT_DATA[0] && DOT_DATA[0].points.length > 0) {
    createDotChart('dot1', DOT_DATA[0].points, true);  // コース平均ST（数値）
  }
  if (DOT_DATA[1] && DOT_DATA[1].points.length > 0) {
    createDotChart('dot2', DOT_DATA[1].points, true);  // 今節平均ST（数値）
  }
  if (DOT_DATA[2] && DOT_DATA[2].points.length > 0) {
    createDotChart('dot3', DOT_DATA[2].points, false); // コース平均ST順位
  }
  if (DOT_DATA[3] && DOT_DATA[3].points.length > 0) {
    createDotChart('dot4', DOT_DATA[3].points, false); // 今節平均ST順位
  }
  
  createBarChart('bottomBar1', BOTTOM_BAR[0].labels, BOTTOM_BAR[0].values, BOTTOM_BAR[0].colors);
  createBarChart('bottomBar2', BOTTOM_BAR[1].labels, BOTTOM_BAR[1].values, BOTTOM_BAR[1].colors);
  
  renderPlayerTable(PLAYERS);
  renderStatsTable(STATS1, 'statsHead1', 'statsBody1');
  renderKonsetsuTable(KONSETSU_DATA);
  
  drawRingCanvas();
});

function renderPlayerTable(players) {
  const tbody = document.getElementById('player-tbody');
  tbody.innerHTML = '';
  players.forEach(p => {
    const tr = document.createElement('tr');
    
    // 0を"-"に変換する関数
    const displayNum = (val, decimals = 2) => {
      if (val === 0 || val === null || val === undefined) return '-';
      return val.toFixed(decimals);
    };
    
    tr.innerHTML = `
      <td style="font-weight:700;color:#ffffff">${p.boat}</td>
      <td style="text-align:left;font-weight:600;color:#ffffff">${p.name}</td>
      <td>${p.grade}</td>
      <td>${p.branch}</td>
      <td>${p.fl}</td>
      <td style="color:#f0f4ff;font-weight:600">${displayNum(p.nation_rate)}</td>
      <td style="color:#c8d8f0">${displayNum(p.local_rate)}</td>
      <td><span style="font-size:10px;font-weight:bold">${p.m_eval}</span></td>
      <td style="color:${p.motor_color};font-weight:600">${p.motor_type}</td>
      <td style="color:#9bb2cc">${p.point}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderStatsTable(stats, headId, bodyId) {
  const thead = document.getElementById(headId); const tbody = document.getElementById(bodyId);
  thead.innerHTML = `<tr>${stats.headers.map(h => `<th>${h}</th>`).join('')}</tr>`;
  tbody.innerHTML = '';
  stats.rows.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = row.map((cell, ci) => {
      if (ci === 0) return `<td style="text-align:left;color:#d0dae8;font-weight:500">${cell}</td>`;
      
      // 0や空欄を"-"に統一
      let displayValue = cell;
      const num = parseFloat(cell);
      if (cell === '' || cell === null || cell === undefined || (cell === '0' || cell === '0.0' || num === 0)) {
        displayValue = '-';
      }
      
      let cls = 'highlight';
      if (!isNaN(num) && num > 0) {
        if (num >= 30 || cell.includes('%') && parseFloat(cell) >= 40) cls = 'val-high';
        else if (num <= 5) cls = 'val-low';
      }
      return `<td class="${cls}">${displayValue}</td>`;
    }).join('');
    tbody.appendChild(tr);
  });
}

function renderKonsetsuTable(konsetsu) {
  const thead = document.getElementById('konsetsuHead');
  const tbody = document.getElementById('konsetsuBody');
  
  // ヘッダー作成
  let headerHTML = '<tr><th>選手</th>';
  for (let day = 1; day <= 6; day++) {
    headerHTML += `<th colspan="2">${day}日目</th>`;
  }
  headerHTML += '</tr>';
  thead.innerHTML = headerHTML;
  
  // ボディ作成
  tbody.innerHTML = '';
  konsetsu.forEach(player => {
    const tr = document.createElement('tr');
    let rowHTML = `<td>${player.name}</td>`;
    for (let day = 1; day <= 6; day++) {
      const run1 = player.results[`${day}-1`] || '';
      const run2 = player.results[`${day}-2`] || '';
      const display1 = run1 && run1 !== '' && run1 !== '-' ? `<span class="waku-cell">${run1}</span>` : '-';
      const display2 = run2 && run2 !== '' && run2 !== '-' ? `<span class="waku-cell">${run2}</span>` : '-';
      rowHTML += `<td>${display1}</td>`;
      rowHTML += `<td>${display2}</td>`;
    }
    tr.innerHTML = rowHTML;
    tbody.appendChild(tr);
  });
}

function drawRingCanvas() {
  const canvas = document.getElementById('ring-canvas'); if (!canvas) return;
  const dpr = window.devicePixelRatio || 1;
  const W = canvas.parentElement.offsetWidth; const H = canvas.parentElement.offsetHeight;
  canvas.width = W * dpr; canvas.height = H * dpr;
  canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
  const ctx = canvas.getContext('2d'); ctx.scale(dpr, dpr);
  const cx = W / 2; const cy = H / 2; const R = Math.min(W, H) / 2 - 4;
  
  const grad1 = ctx.createLinearGradient(cx - R, cy, cx + R, cy);
  grad1.addColorStop(0, 'rgba(30,144,255,0.0)'); grad1.addColorStop(0.5, 'rgba(120,200,255,1.0)'); grad1.addColorStop(1, 'rgba(30,144,255,0.0)');
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.strokeStyle = grad1; ctx.lineWidth = 2.5; ctx.stroke();

  const grad2 = ctx.createLinearGradient(cx, cy - R, cx, cy + R);
  grad2.addColorStop(0, 'rgba(255,200,0,0.0)'); grad2.addColorStop(0.5, 'rgba(255,80,0,1.0)'); grad2.addColorStop(1, 'rgba(255,200,0,0.0)');
  ctx.beginPath(); ctx.arc(cx, cy, R - 6, 0, Math.PI * 2); ctx.strokeStyle = grad2; ctx.lineWidth = 3.5; ctx.stroke();
}
window.addEventListener('resize', drawRingCanvas);
"""

# ============================================================
# データパース & 出力ロジック
# ============================================================

def generate_dashboard_data(csv_path, output_dir="dist2"):
    df = pd.read_csv(csv_path)
    
    # カラム名の正規化
    df.columns = df.columns.str.strip().str.replace('‐', '-').str.replace('−', '-')
    
    grouped = df.groupby(['レース場', 'レース回'])
    
    for (place, round_no), group in grouped:
        group = group.sort_values('枠番')
        
        players_list = []
        for _, row in group.iterrows():
            # 今節成績の文字列連結ロジック
            res_list = []
            for j in range(1, 7):
                for k in range(1, 3):
                    val = row.get(f'今節成績_{j}-{k}')
                    if pd.notna(val) and str(val).strip() != '-' and str(val).strip() != '':
                        try:
                            res_list.append(str(int(float(val))))
                        except:
                            pass
            results_str = " ".join(res_list) if res_list else "-"
            
            # M総合評価のマッピング
            m_eval = safe_str(row['M総合評価'], default="-")
            m_eval_map = {'S': '超絶', 'A': '上位', 'B': '中堅上位', 'C': '中堅下位', 'D': '下位'}
            m_eval_display = m_eval_map.get(m_eval, '-')
            
            # モーター型の判定
            deashi_val = safe_float(row.get('出足'))
            nobashi_val = safe_float(row.get('伸び足'))
            
            if deashi_val == 0 and nobashi_val == 0:
                motor_type = '-'
                motor_color = '#ffffff'
            else:
                if deashi_val > nobashi_val:
                    motor_type = '出足型'
                elif nobashi_val > deashi_val:
                    motor_type = '伸び型'
                else:
                    motor_type = 'バランス型'
                motor_color = '#ff6b6b' if (deashi_val >= 4 or nobashi_val >= 4) else '#ffffff'
            
            # pointの生成
            m_shisu = safe_float(row['M指数'])
            if m_shisu >= 5:
                m_rank = 'S'
            elif m_shisu >= 4:
                m_rank = 'A'
            elif m_shisu >= 3:
                m_rank = 'B'
            elif m_shisu >= 2:
                m_rank = 'C'
            elif m_shisu >= 1:
                m_rank = 'D'
            else:
                m_rank = '-'
            
            activepoint_str = safe_str(row.get('activepoint', '-'))
            ap_map = {
                'S+': '++++', 'S': '+++',
                'A+': '++', 'A': '+',
                'B+': '+-', 'B': '-',
                'C+': '--', 'C': '--',
                'D+': '---', 'D': '---'
            }
            ap_symbol = ap_map.get(activepoint_str, '')
            point_display = f"{m_rank}{ap_symbol}" if m_rank != '-' and ap_symbol else '-'
            
            p_dict = {
                "boat": int(row['枠番']),
                "name": safe_str(row['選手名']),
                "grade": safe_str(row['級別']),
                "branch": safe_str(row['支部']),
                "fl": safe_str(row['FL'], default="-"),
                "nation_rate": safe_float(row['全国勝率']),
                "local_rate": safe_float(row['当地勝率']),
                "m_eval": m_eval_display,
                "motor_type": motor_type,
                "motor_color": motor_color,
                "point": point_display
            }
            players_list.append(p_dict)
            
        # 1枠の1着率をドーナツチャートに表示（%で）
        first_row = group.iloc[0]
        first_1chakuritsu = safe_float(first_row.get('1着率'))
        donut_val = first_1chakuritsu * 100 if first_1chakuritsu <= 1.0 else first_1chakuritsu
        
        # 1枠の1-2率、1-3率を上部ミニKPIへマッピング（%で）
        rate_1_2 = safe_float(first_row.get('1-2率'))
        rate_1_2_percent = rate_1_2 * 100 if rate_1_2 <= 1.0 else rate_1_2
        rate_1_3 = safe_float(first_row.get('1-3率'))
        rate_1_3_percent = rate_1_3 * 100 if rate_1_3 <= 1.0 else rate_1_3
        
        # 右パネル1の構築（2着がX号艇 マトリックス）
        matrix_rows = []
        for _, row in group.iterrows():
            matrix_rows.append([
                f"{int(row['枠番'])}",
                f"{safe_float(row.get('2着が1号艇')):.0f}",
                f"{safe_float(row.get('2着が2号艇')):.0f}",
                f"{safe_float(row.get('2着が3号艇')):.0f}",
                f"{safe_float(row.get('2着が4号艇')):.0f}",
                f"{safe_float(row.get('2着が5号艇')):.0f}",
                f"{safe_float(row.get('2着が6号艇')):.0f}"
            ])
            
        # 今節成績データの構築
        dot_data_list = []
        colors_by_waku = ["#FFFFFF", "#000000", "#FF3333", "#3333FF", "#FFCC00", "#00AA00"]
        
        # 1. コース平均ST
        dot1_points = []
        for idx, row in group.iterrows():
            waku = int(row['枠番'])
            val = safe_float(row.get('コース平均st'), default=0.0)
            if val > 0:  # 有効なデータのみ
                dot1_points.append({
                    "x": waku,
                    "y": val,
                    "c": colors_by_waku[waku - 1] if 1 <= waku <= 6 else colors_by_waku[0]
                })
        dot_data_list.append({"points": dot1_points})
        
        # 2. 今節平均ST
        dot2_points = []
        for idx, row in group.iterrows():
            waku = int(row['枠番'])
            val = safe_float(row.get('今節平均st'), default=0.0)
            if val > 0:  # 有効なデータのみ
                dot2_points.append({
                    "x": waku,
                    "y": val,
                    "c": colors_by_waku[waku - 1] if 1 <= waku <= 6 else colors_by_waku[0]
                })
        dot_data_list.append({"points": dot2_points})
        
        # 3. コース平均ST順位
        dot3_points = []
        for idx, row in group.iterrows():
            waku = int(row['枠番'])
            val = safe_float(row.get('コース平均st順位'), default=0.0)
            if val > 0:  # 有効なデータのみ
                dot3_points.append({
                    "x": waku,
                    "y": val,
                    "c": colors_by_waku[waku - 1] if 1 <= waku <= 6 else colors_by_waku[0]
                })
        dot_data_list.append({"points": dot3_points})
        
        # 4. 今節平均ST順位
        dot4_points = []
        for idx, row in group.iterrows():
            waku = int(row['枠番'])
            val = safe_float(row.get('今節平均st順位'), default=0.0)
            if val > 0:  # 有効なデータのみ
                dot4_points.append({
                    "x": waku,
                    "y": val,
                    "c": colors_by_waku[waku - 1] if 1 <= waku <= 6 else colors_by_waku[0]
                })
        dot_data_list.append({"points": dot4_points})
        
        # 下部バーチャート用データ（2つ）
        bottom_bar_list = []
        
        # 1. コースSTトップ率
        top_rate_values = []
        for _, row in group.iterrows():
            val = safe_float(row.get('コースstトップ率'))
            percent = val * 100 if val <= 1.0 else val
            top_rate_values.append(percent)
        
        bottom_bar_list.append({
            "labels": ["1", "2", "3", "4", "5", "6"],
            "values": top_rate_values,
            "colors": ["#1e90ff"] * 6
        })
        
        # 2. コースST最下位率
        bottom_rate_values = []
        for _, row in group.iterrows():
            val = safe_float(row.get('コースst最下位率'))
            percent = val * 100 if val <= 1.0 else val
            bottom_rate_values.append(percent)
        
        bottom_bar_list.append({
            "labels": ["1", "2", "3", "4", "5", "6"],
            "values": bottom_rate_values,
            "colors": ["#e74c3c"] * 6
        })
            
        # 今節成績データの構築
        konsetsu_data = []
        for _, row in group.iterrows():
            player_results = {"name": safe_str(row['選手名']), "results": {}}
            for day in range(1, 7):
                for run in range(1, 3):
                    col_name = f'今節成績_{day}-{run}'
                    waku_val = row.get(col_name, '')
                    if pd.notna(waku_val) and str(waku_val).strip() not in ['', '-', 'nan']:
                        try:
                            player_results["results"][f'{day}-{run}'] = str(int(float(waku_val)))
                        except:
                            player_results["results"][f'{day}-{run}'] = ''
                    else:
                        player_results["results"][f'{day}-{run}'] = ''
            konsetsu_data.append(player_results)
            
        race_payload = {
            "RACE_INFO": {"venue": place, "race": round_no},
            "PLAYERS": players_list,
            "KPI": {
                "donut": {"val": donut_val, "max": 100.0, "color": "#ffffff"},
                "miniBar1": {"val": rate_1_2_percent, "color": "#000000"},
                "miniBar2": {"val": rate_1_3_percent, "color": "#dc2626"}
            },
            "RENTAI_DATA": {
                "labels": [p['name'] for p in players_list],
                "datasets": [
                    {
                        "label": "1着", 
                        "data": [safe_float(r.get('1着率')) * 100 if safe_float(r.get('1着率')) <= 1.0 else safe_float(r.get('1着率')) for _, r in group.iterrows()], 
                        "color": "#444444"
                    },
                    {
                        "label": "2着", 
                        "data": [safe_float(r.get('2着率')) * 100 if safe_float(r.get('2着率')) <= 1.0 else safe_float(r.get('2着率')) for _, r in group.iterrows()], 
                        "color": "#888888"
                    },
                    {
                        "label": "3着", 
                        "data": [safe_float(r.get('3着率')) * 100 if safe_float(r.get('3着率')) <= 1.0 else safe_float(r.get('3着率')) for _, r in group.iterrows()], 
                        "color": "#CCCCCC"
                    }
                ]
            },
            "HBAR_DATA": {
                "labels": [p['name'] for p in players_list],
                "datasets": [
                    {
                        "label": "差し", 
                        "data": [safe_float(r.get('差し率')) * 100 if safe_float(r.get('差し率')) <= 1.0 else safe_float(r.get('差し率')) for _, r in group.iterrows()], 
                        "color": "#FFFFFF"
                    },
                    {
                        "label": "まくり", 
                        "data": [safe_float(r.get('まくり率')) * 100 if safe_float(r.get('まくり率')) <= 1.0 else safe_float(r.get('まくり率')) for _, r in group.iterrows()], 
                        "color": "#FF3333"
                    },
                    {
                        "label": "まくり差し", 
                        "data": [safe_float(r.get('まくり差し率')) * 100 if safe_float(r.get('まくり差し率')) <= 1.0 else safe_float(r.get('まくり差し率')) for _, r in group.iterrows()], 
                        "color": "#FFCC00"
                    }
                ]
            },
            "DOT_DATA": dot_data_list,
            "BOTTOM_BAR": bottom_bar_list,
            "STATS1": {
                "headers": ["選手", "1", "2", "3", "4", "5", "6"],
                "rows": [[p['name'], *row[1:]] for p, row in zip(players_list, matrix_rows)]
            },
            "KONSETSU_DATA": konsetsu_data
        }
        
        race_dir = os.path.join(output_dir, f"{place}_{round_no}")
        css_dir = os.path.join(race_dir, "css")
        js_dir = os.path.join(race_dir, "js")
        
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)
        
        with open(os.path.join(race_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(HTML_TEMPLATE)
        with open(os.path.join(css_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write(CSS_TEMPLATE)
        with open(os.path.join(js_dir, "charts.js"), "w", encoding="utf-8") as f:
            f.write(CHARTS_JS_TEMPLATE)
        with open(os.path.join(js_dir, "main.js"), "w", encoding="utf-8") as f:
            f.write(MAIN_JS_TEMPLATE)
            
        js_content = f"""const RACE_INFO = {json.dumps(race_payload['RACE_INFO'], ensure_ascii=False, indent=2)};
const PLAYERS = {json.dumps(race_payload['PLAYERS'], ensure_ascii=False, indent=2)};
const KPI = {json.dumps(race_payload['KPI'], ensure_ascii=False, indent=2)};
const RENTAI_DATA = {json.dumps(race_payload['RENTAI_DATA'], ensure_ascii=False, indent=2)};
const HBAR_DATA = {json.dumps(race_payload['HBAR_DATA'], ensure_ascii=False, indent=2)};
const DOT_DATA = {json.dumps(race_payload['DOT_DATA'], ensure_ascii=False, indent=2)};
const BOTTOM_BAR = {json.dumps(race_payload['BOTTOM_BAR'], ensure_ascii=False, indent=2)};
const STATS1 = {json.dumps(race_payload['STATS1'], ensure_ascii=False, indent=2)};
const KONSETSU_DATA = {json.dumps(race_payload['KONSETSU_DATA'], ensure_ascii=False, indent=2)};"""

        with open(os.path.join(js_dir, "data.js"), "w", encoding="utf-8") as f:
            f.write(js_content)
            
    print(f"成功: {len(grouped)} レース分のパッケージを '{output_dir}' フォルダ内に生成しました。")

if __name__ == "__main__":
    generate_dashboard_data('merged_results.csv')