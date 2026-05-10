// ============================================================
//  War3 Tournament Hub — front-end data & interactions
//  Static demo data. Wire to a real API by replacing the
//  loadX() functions below.
// ============================================================

const RACE_LABEL = { HUM: "人", ORC: "兽", UD: "亡", NE: "暗" };
const RACE_NAME  = { HUM: "人族", ORC: "兽族", UD: "不死", NE: "暗夜" };

// ---------- LIVE MATCHES ----------
const liveMatches = [
  {
    id: "m-001",
    tournament: "WCG 2026 春季赛 · 季后赛",
    stage: "半决赛 · BO5",
    p1: { name: "Moon",  country: "🇰🇷", race: "NE" },
    p2: { name: "Lyn",   country: "🇰🇷", race: "ORC" },
    score: [2, 1],
    map: "Twisted Meadows",
    viewers: 18420,
    live: true,
    streamUrl: "#",
  },
  {
    id: "m-002",
    tournament: "Gold Series Heroes League S14",
    stage: "小组赛 · BO3",
    p1: { name: "Infi",  country: "🇨🇳", race: "HUM" },
    p2: { name: "TH000", country: "🇨🇳", race: "HUM" },
    score: [1, 1],
    map: "Echo Isles",
    viewers: 9120,
    live: true,
    streamUrl: "#",
  },
  {
    id: "m-003",
    tournament: "ESL Pro Tour · Frozen Cup",
    stage: "1/4 决赛 · BO5",
    p1: { name: "Happy", country: "🇷🇺", race: "UD" },
    p2: { name: "Colorful", country: "🇨🇳", race: "HUM" },
    score: [3, 0],
    map: "Concealed Hill",
    viewers: 6480,
    live: false,
    finished: true,
    streamUrl: "#",
  },
];

function renderLive() {
  const grid = document.getElementById("liveGrid");
  grid.innerHTML = liveMatches.map(m => `
    <article class="card match-card">
      <div class="row" style="justify-content: space-between;">
        <span class="tag">${m.tournament}</span>
        ${m.live
          ? `<span class="live-badge"><span class="dot dot-live"></span>LIVE</span>`
          : `<span class="tag" style="background:rgba(116,225,160,0.12);color:#74e1a0;border-color:rgba(116,225,160,0.3)">已结束</span>`}
      </div>
      <div style="color:var(--muted);font-size:13px;margin-top:6px">${m.stage} · ${m.map}</div>

      <div class="versus">
        <div class="player">
          <div class="race-badge race-${m.p1.race}">${RACE_LABEL[m.p1.race]}</div>
          <strong>${m.p1.country} ${m.p1.name}</strong>
          <span style="color:var(--muted);font-size:12px">${RACE_NAME[m.p1.race]}</span>
        </div>
        <div class="score">
          ${m.score[0]} : ${m.score[1]}
          <small>${m.live ? "进行中" : "终"}</small>
        </div>
        <div class="player">
          <div class="race-badge race-${m.p2.race}">${RACE_LABEL[m.p2.race]}</div>
          <strong>${m.p2.country} ${m.p2.name}</strong>
          <span style="color:var(--muted);font-size:12px">${RACE_NAME[m.p2.race]}</span>
        </div>
      </div>

      <div class="meta">
        <span>👁 ${m.viewers.toLocaleString()} 观众</span>
        <a href="${m.streamUrl}" class="live-link">${m.live ? "进入直播 →" : "观看回放 →"}</a>
      </div>
    </article>
  `).join("");
}

// ---------- SCHEDULE ----------
const schedule = [
  { date: "05/11 19:00", event: "WCG 2026 春季赛", players: "Moon vs Sok", format: "BO5", url: "#" },
  { date: "05/12 20:00", event: "Gold Series S14",  players: "Infi vs Fly100%", format: "BO3", url: "#" },
  { date: "05/12 21:30", event: "Gold Series S14",  players: "120 vs Romantic", format: "BO3", url: "#" },
  { date: "05/13 18:00", event: "ESL Frozen Cup",   players: "Happy vs FoCuS", format: "BO5", url: "#" },
  { date: "05/14 19:00", event: "Back2Warcraft Cup",players: "Lyn vs ReMinD",  format: "BO3", url: "#" },
  { date: "05/15 20:00", event: "WCG 2026 决赛",     players: "TBD vs TBD",      format: "BO7", url: "#" },
  { date: "05/16 19:30", event: "中国战队联赛 CWL",   players: "WE vs IG",        format: "BO5", url: "#" },
];

function renderSchedule() {
  const tbody = document.querySelector("#scheduleTable tbody");
  tbody.innerHTML = schedule.map(s => `
    <tr>
      <td class="when">${s.date}</td>
      <td>${s.event}</td>
      <td>${s.players}</td>
      <td>${s.format}</td>
      <td><a class="live-link" href="${s.url}">观看 →</a></td>
    </tr>
  `).join("");
}

// ---------- REPLAYS ----------
const replays = [
  {
    title: "Moon vs Lyn — 上古祭坛的较量",
    map: "Twisted Meadows",
    races: ["NE", "ORC"],
    duration: "32:14",
    apm: "412",
    date: "2026-05-08",
    size: "1.8 MB",
    file: "#",
  },
  {
    title: "Infi 的飞机海复刻经典",
    map: "Echo Isles",
    races: ["HUM", "ORC"],
    duration: "28:47",
    apm: "385",
    date: "2026-05-07",
    size: "1.4 MB",
    file: "#",
  },
  {
    title: "Happy vs FoCuS — 蜘蛛流极致打压",
    map: "Concealed Hill",
    races: ["UD", "UD"],
    duration: "24:03",
    apm: "344",
    date: "2026-05-06",
    size: "1.1 MB",
    file: "#",
  },
  {
    title: "TH000 大法师骚扰教科书",
    map: "Last Refuge",
    races: ["HUM", "NE"],
    duration: "36:52",
    apm: "402",
    date: "2026-05-05",
    size: "2.0 MB",
    file: "#",
  },
  {
    title: "Sok 速矿牛头打闪电链",
    map: "Terenas Stand",
    races: ["ORC", "UD"],
    duration: "21:08",
    apm: "367",
    date: "2026-05-04",
    size: "0.9 MB",
    file: "#",
  },
  {
    title: "120 三本毁灭者翻盘局",
    map: "Northern Isles",
    races: ["UD", "HUM"],
    duration: "44:20",
    apm: "298",
    date: "2026-05-03",
    size: "2.4 MB",
    file: "#",
  },
];

function renderReplays(filter = "all") {
  const grid = document.getElementById("replayGrid");
  const items = filter === "all"
    ? replays
    : replays.filter(r => r.races.includes(filter));
  grid.innerHTML = items.map(r => `
    <article class="card replay-card">
      <div class="head">
        <div>
          <h3>${r.title}</h3>
          <div class="map">🗺 ${r.map} · ${r.date}</div>
        </div>
        <div style="display:flex;gap:6px">
          ${r.races.map(rc => `<div class="race-badge race-${rc}" style="width:32px;height:32px;font-size:12px">${RACE_LABEL[rc]}</div>`).join("")}
        </div>
      </div>
      <div class="stats">
        <div><span>时长</span><strong>${r.duration}</strong></div>
        <div><span>平均 APM</span><strong>${r.apm}</strong></div>
        <div><span>文件</span><strong>${r.size}</strong></div>
      </div>
      <div class="actions">
        <a href="${r.file}" class="primary" download>⬇ 下载 .w3g</a>
        <a href="${r.file}">在线观看</a>
      </div>
    </article>
  `).join("") || `<p class="muted">暂无符合该种族的录像。</p>`;
}

// ---------- VIDEOS ----------
// Note: thumbnails reference YouTube standard CDN paths.
const videos = [
  {
    id: "dQw4w9WgXcQ",
    title: "Moon vs Grubby — 史诗级 NE vs ORC 对决",
    caster: "Back2Warcraft",
    duration: "42:18",
    views: "1.2M",
    thumb: "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
  },
  {
    id: "9bZkp7q19f0",
    title: "Infi 教科书级人族开局拆解",
    caster: "Neo TV",
    duration: "18:45",
    views: "342K",
    thumb: "https://i.ytimg.com/vi/9bZkp7q19f0/hqdefault.jpg",
  },
  {
    id: "kJQP7kiw5Fk",
    title: "Happy 不死流派演变 · 战术复盘",
    caster: "WCG Official",
    duration: "27:33",
    views: "586K",
    thumb: "https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg",
  },
  {
    id: "hT_nvWreIhg",
    title: "TH000 vs Lyn — 中国 vs 韩国巅峰对决",
    caster: "ESL",
    duration: "55:21",
    views: "2.1M",
    thumb: "https://i.ytimg.com/vi/hT_nvWreIhg/hqdefault.jpg",
  },
  {
    id: "OPf0YbXqDm0",
    title: "Sok 兽族暴力流 · 一炮一个山头",
    caster: "Back2Warcraft",
    duration: "31:09",
    views: "418K",
    thumb: "https://i.ytimg.com/vi/OPf0YbXqDm0/hqdefault.jpg",
  },
  {
    id: "RgKAFK5djSk",
    title: "暗夜精灵英雄出场顺序详解",
    caster: "Tactics Lab",
    duration: "14:52",
    views: "229K",
    thumb: "https://i.ytimg.com/vi/RgKAFK5djSk/hqdefault.jpg",
  },
];

function renderVideos() {
  const grid = document.getElementById("videoGrid");
  grid.innerHTML = videos.map(v => `
    <article class="card video-card" data-id="${v.id}" data-title="${v.title}">
      <div class="thumb">
        <img src="${v.thumb}" alt="${v.title}" loading="lazy" onerror="this.style.display='none'" />
        <div class="play"></div>
        <span class="duration">${v.duration}</span>
      </div>
      <div class="info">
        <h3>${v.title}</h3>
        <div class="info-meta">
          <span>${v.caster}</span>
          <span>👁 ${v.views}</span>
        </div>
      </div>
    </article>
  `).join("");
}

// ---------- RANKINGS ----------
const rankings = [
  { name: "Moon",   country: "🇰🇷 South Korea", race: "NE", elo: 2387, change: +24 },
  { name: "Happy",  country: "🇷🇺 Russia",      race: "UD", elo: 2351, change: +12 },
  { name: "Lyn",    country: "🇰🇷 South Korea", race: "ORC", elo: 2334, change: -8 },
  { name: "Infi",   country: "🇨🇳 China",       race: "HUM", elo: 2318, change: +6 },
  { name: "TH000",  country: "🇨🇳 China",       race: "HUM", elo: 2295, change: -3 },
  { name: "Fly100%",country: "🇨🇳 China",       race: "ORC", elo: 2271, change: +18 },
  { name: "Sok",    country: "🇰🇷 South Korea", race: "ORC", elo: 2253, change: +4 },
  { name: "FoCuS",  country: "🇰🇷 South Korea", race: "UD", elo: 2240, change: -11 },
  { name: "120",    country: "🇨🇳 China",       race: "UD", elo: 2218, change: 0 },
  { name: "Colorful",country:"🇨🇳 China",       race: "HUM", elo: 2204, change: +9 },
];

function renderRankings() {
  const ol = document.getElementById("rankList");
  ol.innerHTML = rankings.map((p, i) => {
    const cls = p.change > 0 ? "up" : p.change < 0 ? "down" : "";
    const sign = p.change > 0 ? "▲" : p.change < 0 ? "▼" : "—";
    return `
      <li>
        <div class="pos">#${i + 1}</div>
        <div>
          <div class="name">${p.name}</div>
          <div class="country">${p.country}</div>
        </div>
        <div class="race-badge race-${p.race}" style="width:36px;height:36px;font-size:13px">${RACE_LABEL[p.race]}</div>
        <div class="elo">${p.elo}</div>
        <div class="change ${cls}">${sign} ${Math.abs(p.change)}</div>
      </li>
    `;
  }).join("");
}

// ---------- FILTERS ----------
function bindFilters() {
  document.querySelectorAll(".filters .chip").forEach(chip => {
    chip.addEventListener("click", () => {
      document.querySelectorAll(".filters .chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      renderReplays(chip.dataset.filter);
    });
  });
}

// ---------- VIDEO MODAL ----------
function bindVideoModal() {
  const modal = document.getElementById("videoModal");
  const frame = document.getElementById("videoFrame");

  document.getElementById("videoGrid").addEventListener("click", e => {
    const card = e.target.closest(".video-card");
    if (!card) return;
    const id = card.dataset.id;
    frame.innerHTML = `<iframe src="https://www.youtube.com/embed/${id}?autoplay=1" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>`;
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
  });

  modal.addEventListener("click", e => {
    if (e.target.dataset.close !== undefined) {
      modal.setAttribute("aria-hidden", "true");
      frame.innerHTML = "";
      document.body.style.overflow = "";
    }
  });

  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && modal.getAttribute("aria-hidden") === "false") {
      modal.setAttribute("aria-hidden", "true");
      frame.innerHTML = "";
      document.body.style.overflow = "";
    }
  });
}

// ---------- THEME TOGGLE ----------
function bindTheme() {
  const btn = document.getElementById("themeToggle");
  const saved = localStorage.getItem("war3-theme");
  if (saved) document.documentElement.setAttribute("data-theme", saved);
  btn.textContent = saved === "light" ? "☀" : "🌙";
  btn.addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme");
    const next = cur === "light" ? "" : "light";
    if (next) document.documentElement.setAttribute("data-theme", next);
    else document.documentElement.removeAttribute("data-theme");
    localStorage.setItem("war3-theme", next);
    btn.textContent = next === "light" ? "☀" : "🌙";
  });
}

// ---------- LIVE COUNTERS (small heartbeat) ----------
function bindHeartbeat() {
  const elV = liveMatches.filter(m => m.live);
  setInterval(() => {
    elV.forEach(m => {
      m.viewers += Math.floor(Math.random() * 30 - 10);
      if (m.viewers < 100) m.viewers = 100;
    });
    document.querySelectorAll("#liveGrid .meta span:first-child").forEach((el, i) => {
      if (liveMatches[i] && liveMatches[i].live) {
        el.textContent = `👁 ${liveMatches[i].viewers.toLocaleString()} 观众`;
      }
    });
  }, 5000);
}

// ---------- INIT ----------
document.addEventListener("DOMContentLoaded", () => {
  renderLive();
  renderSchedule();
  renderReplays();
  renderVideos();
  renderRankings();
  bindFilters();
  bindVideoModal();
  bindTheme();
  bindHeartbeat();
});
