// 主流联赛对阵 / 赔率 / 赛程模拟数据
// Date format: ISO local (YYYY-MM-DDTHH:mm)
// Odds format: { home, draw, away } 1x2 odds

const LEAGUES = {
  EPL:        { name: "英超 Premier League",    color: "#3d1a78" },
  LaLiga:     { name: "西甲 La Liga",            color: "#ee2027" },
  Bundesliga: { name: "德甲 Bundesliga",         color: "#d20515" },
  SerieA:     { name: "意甲 Serie A",            color: "#0a4595" },
  Ligue1:     { name: "法甲 Ligue 1",            color: "#091c3e" },
  UCL:        { name: "欧冠 Champions League",   color: "#0a3469" },
};

const TEAMS = {
  // EPL
  MCI: { short: "曼城",   full: "Manchester City",     emoji: "🩵" },
  ARS: { short: "阿森纳", full: "Arsenal",             emoji: "🔴" },
  LIV: { short: "利物浦", full: "Liverpool",           emoji: "❤️" },
  MUN: { short: "曼联",   full: "Manchester United",   emoji: "🟥" },
  CHE: { short: "切尔西", full: "Chelsea",             emoji: "🔵" },
  TOT: { short: "热刺",   full: "Tottenham",           emoji: "⚪" },
  NEW: { short: "纽卡斯尔", full: "Newcastle",         emoji: "⚫" },
  AVL: { short: "维拉",   full: "Aston Villa",         emoji: "🟣" },
  // La Liga
  RMA: { short: "皇马",   full: "Real Madrid",         emoji: "⚪" },
  BAR: { short: "巴萨",   full: "Barcelona",           emoji: "🔵" },
  ATM: { short: "马竞",   full: "Atlético Madrid",     emoji: "🔴" },
  GIR: { short: "赫罗纳", full: "Girona",              emoji: "🟥" },
  SEV: { short: "塞维利亚", full: "Sevilla",           emoji: "⚪" },
  RBE: { short: "皇家贝蒂斯", full: "Real Betis",      emoji: "🟢" },
  // Bundesliga
  BAY: { short: "拜仁",   full: "Bayern Munich",       emoji: "🔴" },
  BVB: { short: "多特",   full: "Borussia Dortmund",   emoji: "🟡" },
  RBL: { short: "莱比锡", full: "RB Leipzig",          emoji: "⚪" },
  LEV: { short: "勒沃库森", full: "Bayer Leverkusen",  emoji: "⚫" },
  // Serie A
  INT: { short: "国米",   full: "Inter Milan",         emoji: "🔵" },
  JUV: { short: "尤文",   full: "Juventus",            emoji: "⚪" },
  MIL: { short: "AC米兰", full: "AC Milan",            emoji: "🔴" },
  NAP: { short: "那不勒斯", full: "Napoli",            emoji: "🔵" },
  ROM: { short: "罗马",   full: "AS Roma",             emoji: "🟡" },
  // Ligue 1
  PSG: { short: "巴黎",   full: "Paris Saint-Germain", emoji: "🔵" },
  MAR: { short: "马赛",   full: "Marseille",           emoji: "⚪" },
  MON: { short: "摩纳哥", full: "Monaco",              emoji: "🔴" },
  LYO: { short: "里昂",   full: "Lyon",                emoji: "🔵" },
};

// Generate a span of dates starting from "today"
function daysFromNow(n, hour = 19, minute = 30) {
  const d = new Date();
  d.setDate(d.getDate() + n);
  d.setHours(hour, minute, 0, 0);
  const pad = (x) => String(x).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(hour)}:${pad(minute)}`;
}

const MATCHES = [
  // === This week ===
  { id: "m01", league: "EPL", home: "MCI", away: "ARS", date: daysFromNow(0, 22, 0), venue: "Etihad Stadium", round: "第34轮",
    odds: { home: 2.05, draw: 3.40, away: 3.60 } },
  { id: "m02", league: "EPL", home: "LIV", away: "CHE", date: daysFromNow(0, 19, 30), venue: "Anfield", round: "第34轮",
    odds: { home: 1.78, draw: 3.80, away: 4.50 } },
  { id: "m03", league: "EPL", home: "MUN", away: "TOT", date: daysFromNow(1, 21, 0), venue: "Old Trafford", round: "第34轮",
    odds: { home: 2.40, draw: 3.30, away: 2.90 } },
  { id: "m04", league: "EPL", home: "NEW", away: "AVL", date: daysFromNow(2, 20, 0), venue: "St James' Park", round: "第34轮",
    odds: { home: 2.15, draw: 3.40, away: 3.30 } },

  { id: "m05", league: "LaLiga", home: "RMA", away: "BAR", date: daysFromNow(0, 21, 0), venue: "Santiago Bernabéu", round: "第34轮",
    odds: { home: 2.10, draw: 3.60, away: 3.20 } },
  { id: "m06", league: "LaLiga", home: "ATM", away: "GIR", date: daysFromNow(1, 22, 0), venue: "Metropolitano", round: "第34轮",
    odds: { home: 1.65, draw: 4.00, away: 5.00 } },
  { id: "m07", league: "LaLiga", home: "SEV", away: "RBE", date: daysFromNow(2, 21, 30), venue: "Sánchez-Pizjuán", round: "第34轮",
    odds: { home: 2.20, draw: 3.20, away: 3.40 } },

  { id: "m08", league: "Bundesliga", home: "BAY", away: "BVB", date: daysFromNow(1, 18, 30), venue: "Allianz Arena", round: "第31轮",
    odds: { home: 1.70, draw: 4.10, away: 4.60 } },
  { id: "m09", league: "Bundesliga", home: "LEV", away: "RBL", date: daysFromNow(2, 19, 30), venue: "BayArena", round: "第31轮",
    odds: { home: 1.95, draw: 3.70, away: 3.80 } },

  { id: "m10", league: "SerieA", home: "INT", away: "JUV", date: daysFromNow(0, 20, 45), venue: "San Siro", round: "第34轮",
    odds: { home: 1.90, draw: 3.50, away: 4.20 } },
  { id: "m11", league: "SerieA", home: "MIL", away: "NAP", date: daysFromNow(1, 22, 0), venue: "San Siro", round: "第34轮",
    odds: { home: 2.30, draw: 3.30, away: 3.10 } },
  { id: "m12", league: "SerieA", home: "ROM", away: "INT", date: daysFromNow(3, 21, 0), venue: "Stadio Olimpico", round: "第35轮",
    odds: { home: 3.10, draw: 3.40, away: 2.30 } },

  { id: "m13", league: "Ligue1", home: "PSG", away: "MAR", date: daysFromNow(0, 22, 0), venue: "Parc des Princes", round: "第32轮",
    odds: { home: 1.40, draw: 4.80, away: 7.00 } },
  { id: "m14", league: "Ligue1", home: "MON", away: "LYO", date: daysFromNow(2, 21, 0), venue: "Stade Louis II", round: "第32轮",
    odds: { home: 1.85, draw: 3.60, away: 4.20 } },

  { id: "m15", league: "UCL", home: "MCI", away: "RMA", date: daysFromNow(2, 22, 30), venue: "Etihad Stadium", round: "半决赛 (次回合)",
    odds: { home: 1.75, draw: 4.00, away: 4.50 } },
  { id: "m16", league: "UCL", home: "BAY", away: "PSG", date: daysFromNow(3, 22, 30), venue: "Allianz Arena", round: "半决赛 (次回合)",
    odds: { home: 1.95, draw: 3.80, away: 3.70 } },

  // === Next week ===
  { id: "m17", league: "EPL", home: "ARS", away: "LIV", date: daysFromNow(7, 21, 0), venue: "Emirates Stadium", round: "第35轮",
    odds: { home: 2.40, draw: 3.50, away: 2.80 } },
  { id: "m18", league: "EPL", home: "CHE", away: "MCI", date: daysFromNow(8, 20, 0), venue: "Stamford Bridge", round: "第35轮",
    odds: { home: 4.00, draw: 3.70, away: 1.85 } },
  { id: "m19", league: "LaLiga", home: "BAR", away: "ATM", date: daysFromNow(7, 22, 0), venue: "Camp Nou", round: "第35轮",
    odds: { home: 1.95, draw: 3.60, away: 3.80 } },
  { id: "m20", league: "Bundesliga", home: "BVB", away: "LEV", date: daysFromNow(8, 19, 30), venue: "Signal Iduna Park", round: "第32轮",
    odds: { home: 2.50, draw: 3.50, away: 2.70 } },
  { id: "m21", league: "SerieA", home: "JUV", away: "MIL", date: daysFromNow(9, 21, 45), venue: "Allianz Stadium", round: "第35轮",
    odds: { home: 2.20, draw: 3.20, away: 3.30 } },
  { id: "m22", league: "Ligue1", home: "MAR", away: "PSG", date: daysFromNow(9, 22, 0), venue: "Stade Vélodrome", round: "第33轮",
    odds: { home: 4.20, draw: 3.80, away: 1.78 } },
];

// Recent form (W/D/L last 5)
const FORM = {
  MCI: ["W","W","D","W","W"], ARS: ["W","D","W","W","L"], LIV: ["W","W","W","D","W"],
  MUN: ["L","W","D","W","L"], CHE: ["D","W","L","W","D"], TOT: ["W","L","W","D","L"],
  NEW: ["W","W","L","D","W"], AVL: ["D","W","W","L","D"],
  RMA: ["W","W","W","W","D"], BAR: ["W","D","W","L","W"], ATM: ["W","W","D","W","W"],
  GIR: ["W","L","D","W","W"], SEV: ["L","D","W","D","L"], RBE: ["D","W","L","D","W"],
  BAY: ["W","W","W","D","L"], BVB: ["W","D","W","L","D"], RBL: ["L","W","W","D","W"], LEV: ["W","W","W","W","W"],
  INT: ["W","W","W","D","W"], JUV: ["D","W","D","W","L"], MIL: ["W","L","W","D","W"], NAP: ["L","D","W","L","D"], ROM: ["W","W","D","W","L"],
  PSG: ["W","W","W","W","D"], MAR: ["W","D","L","W","W"], MON: ["W","D","W","D","W"], LYO: ["L","W","D","L","W"],
};

// League standings (mocked)
const STANDINGS = {
  EPL: [
    { team: "MCI", P: 33, W: 24, D: 6, L: 3, GF: 78, GA: 30 },
    { team: "ARS", P: 33, W: 23, D: 6, L: 4, GF: 72, GA: 26 },
    { team: "LIV", P: 33, W: 22, D: 7, L: 4, GF: 70, GA: 31 },
    { team: "TOT", P: 33, W: 18, D: 6, L: 9, GF: 65, GA: 51 },
    { team: "NEW", P: 33, W: 17, D: 8, L: 8, GF: 60, GA: 42 },
    { team: "AVL", P: 33, W: 16, D: 7, L: 10, GF: 58, GA: 49 },
    { team: "MUN", P: 33, W: 15, D: 6, L: 12, GF: 50, GA: 48 },
    { team: "CHE", P: 33, W: 13, D: 9, L: 11, GF: 56, GA: 53 },
  ],
  LaLiga: [
    { team: "RMA", P: 33, W: 26, D: 5, L: 2, GF: 75, GA: 22 },
    { team: "BAR", P: 33, W: 22, D: 5, L: 6, GF: 65, GA: 35 },
    { team: "GIR", P: 33, W: 21, D: 5, L: 7, GF: 70, GA: 41 },
    { team: "ATM", P: 33, W: 19, D: 7, L: 7, GF: 62, GA: 36 },
    { team: "RBE", P: 33, W: 13, D: 12, L: 8, GF: 45, GA: 40 },
    { team: "SEV", P: 33, W: 10, D: 12, L: 11, GF: 42, GA: 46 },
  ],
  Bundesliga: [
    { team: "LEV", P: 30, W: 25, D: 5, L: 0, GF: 78, GA: 22 },
    { team: "BAY", P: 30, W: 21, D: 4, L: 5, GF: 80, GA: 35 },
    { team: "RBL", P: 30, W: 16, D: 8, L: 6, GF: 60, GA: 38 },
    { team: "BVB", P: 30, W: 16, D: 8, L: 6, GF: 58, GA: 40 },
  ],
  SerieA: [
    { team: "INT", P: 33, W: 26, D: 6, L: 1, GF: 75, GA: 18 },
    { team: "MIL", P: 33, W: 21, D: 6, L: 6, GF: 65, GA: 35 },
    { team: "JUV", P: 33, W: 18, D: 10, L: 5, GF: 50, GA: 28 },
    { team: "ROM", P: 33, W: 16, D: 9, L: 8, GF: 55, GA: 38 },
    { team: "NAP", P: 33, W: 14, D: 11, L: 8, GF: 52, GA: 42 },
  ],
  Ligue1: [
    { team: "PSG", P: 31, W: 21, D: 8, L: 2, GF: 72, GA: 28 },
    { team: "MON", P: 31, W: 18, D: 7, L: 6, GF: 60, GA: 38 },
    { team: "MAR", P: 31, W: 14, D: 10, L: 7, GF: 50, GA: 38 },
    { team: "LYO", P: 31, W: 13, D: 8, L: 10, GF: 52, GA: 47 },
  ],
};
