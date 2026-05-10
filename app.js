(function () {
  const state = {
    league: "all",
    date: "all",
    sort: "time",
  };

  const el = (sel, parent = document) => parent.querySelector(sel);
  const els = (sel, parent = document) => Array.from(parent.querySelectorAll(sel));

  const fmtTime = (iso) => {
    const d = new Date(iso);
    const pad = (x) => String(x).padStart(2, "0");
    return `${pad(d.getHours())}:${pad(d.getMinutes())}`;
  };
  const fmtDay = (iso) => {
    const d = new Date(iso);
    const pad = (x) => String(x).padStart(2, "0");
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  };
  const weekday = (iso) => "周" + "日一二三四五六"[new Date(iso).getDay()];

  function teamHTML(code, side = "home") {
    const t = TEAMS[code] || { short: code, full: code, emoji: "⚽" };
    return `
      <div class="team ${side}">
        ${side === "away" ? `<span class="team-name">${t.short}</span><div class="team-logo" title="${t.full}">${t.emoji}</div>`
                          : `<div class="team-logo" title="${t.full}">${t.emoji}</div><span class="team-name">${t.short}</span>`}
      </div>`;
  }

  function matchCard(m) {
    return `
      <article class="match-card" data-id="${m.id}">
        <div class="match-meta">
          <span class="league-tag">${LEAGUES[m.league].name}</span>
          <span>${fmtDay(m.date)} ${weekday(m.date)} · ${fmtTime(m.date)}</span>
        </div>
        <div class="match-teams">
          ${teamHTML(m.home, "home")}
          <div class="vs">VS</div>
          ${teamHTML(m.away, "away")}
        </div>
        <div class="odds-row">
          <div class="odd home"><span class="odd-label">主胜</span><span class="odd-value">${m.odds.home.toFixed(2)}</span></div>
          <div class="odd draw"><span class="odd-label">平局</span><span class="odd-value">${m.odds.draw.toFixed(2)}</span></div>
          <div class="odd away"><span class="odd-label">客胜</span><span class="odd-value">${m.odds.away.toFixed(2)}</span></div>
        </div>
      </article>`;
  }

  function applyFilters() {
    let list = MATCHES.slice();
    if (state.league !== "all") list = list.filter((m) => m.league === state.league);
    if (state.date !== "all") list = list.filter((m) => fmtDay(m.date) === state.date);
    if (state.sort === "time") list.sort((a, b) => new Date(a.date) - new Date(b.date));
    else list.sort((a, b) => a.odds.home - b.odds.home);
    return list;
  }

  function renderMatches() {
    const container = el("#match-list");
    const empty = el("#empty-msg");
    const list = applyFilters();
    container.innerHTML = list.map(matchCard).join("");
    empty.classList.toggle("hidden", list.length > 0);

    // Click → modal
    els(".match-card", container).forEach((card) => {
      card.addEventListener("click", () => openModal(card.dataset.id));
    });
  }

  function renderSchedule() {
    const list = applyFilters();
    const groups = {};
    list.forEach((m) => {
      const key = fmtDay(m.date);
      (groups[key] = groups[key] || []).push(m);
    });
    const days = Object.keys(groups).sort();
    el("#schedule-list").innerHTML = days
      .map((day) => {
        const rows = groups[day]
          .sort((a, b) => new Date(a.date) - new Date(b.date))
          .map((m) => `
            <div class="schedule-row">
              <span class="time">${fmtTime(m.date)}</span>
              <span class="home">${TEAMS[m.home]?.short || m.home}</span>
              <span class="vs">VS</span>
              <span class="away">${TEAMS[m.away]?.short || m.away}</span>
              <span class="league">${LEAGUES[m.league].name.split(" ")[0]} · ${m.round}</span>
            </div>`)
          .join("");
        return `
          <div class="schedule-day">
            <h4>${day} <small>${weekday(day)} · ${groups[day].length} 场</small></h4>
            ${rows}
          </div>`;
      })
      .join("");
  }

  function renderStandings() {
    const lid = el("#standing-league").value;
    const rows = (STANDINGS[lid] || [])
      .map((r) => ({ ...r, GD: r.GF - r.GA, Pts: r.W * 3 + r.D }))
      .sort((a, b) => b.Pts - a.Pts || b.GD - a.GD || b.GF - a.GF);

    const tbody = el("#standings-table tbody");
    tbody.innerHTML = rows
      .map((r, i) => {
        const cls = i < 3 ? "top" : i >= rows.length - 1 && rows.length > 6 ? "relegation" : "";
        return `
          <tr class="${cls}">
            <td>${i + 1}</td>
            <td>${TEAMS[r.team]?.emoji || "⚽"} ${TEAMS[r.team]?.short || r.team}</td>
            <td>${r.P}</td><td>${r.W}</td><td>${r.D}</td><td>${r.L}</td>
            <td>${r.GF}</td><td>${r.GA}</td><td>${r.GD > 0 ? "+" + r.GD : r.GD}</td>
            <td><strong>${r.Pts}</strong></td>
          </tr>`;
      })
      .join("");
  }

  function populateDateFilter() {
    const dates = Array.from(new Set(MATCHES.map((m) => fmtDay(m.date)))).sort();
    const sel = el("#date-filter");
    dates.forEach((d) => {
      const opt = document.createElement("option");
      opt.value = d;
      opt.textContent = `${d} (${weekday(d)})`;
      sel.appendChild(opt);
    });
  }

  function updateStats() {
    const now = new Date();
    const weekEnd = new Date();
    weekEnd.setDate(now.getDate() + 7);
    const thisWeek = MATCHES.filter((m) => {
      const d = new Date(m.date);
      return d >= now && d <= weekEnd;
    });
    el("#stat-matches").textContent = thisWeek.length;
    const teams = new Set();
    MATCHES.forEach((m) => { teams.add(m.home); teams.add(m.away); });
    el("#stat-teams").textContent = teams.size;
  }

  // ---- Modal ----
  function openModal(id) {
    const m = MATCHES.find((x) => x.id === id);
    if (!m) return;
    const home = TEAMS[m.home], away = TEAMS[m.away];
    const formHTML = (code) =>
      (FORM[code] || []).map((r) => `<span class="${r}">${r}</span>`).join("");

    // Implied probability from odds
    const inv = (o) => 1 / o;
    const total = inv(m.odds.home) + inv(m.odds.draw) + inv(m.odds.away);
    const prob = (o) => Math.round((inv(o) / total) * 100);

    el("#modal-content").innerHTML = `
      <h3>${LEAGUES[m.league].name} · ${m.round}</h3>
      <p style="color:var(--muted);margin:0;font-size:13px;">
        ${fmtDay(m.date)} ${weekday(m.date)} ${fmtTime(m.date)} · ${m.venue}
      </p>
      <div class="matchup">
        <div class="team">
          <div style="text-align:center">
            <div class="team-logo" style="margin:0 auto 6px;width:44px;height:44px;font-size:20px;">${home.emoji}</div>
            <div>${home.short}</div>
            <div class="form">${formHTML(m.home)}</div>
          </div>
        </div>
        <div class="vs">VS</div>
        <div class="team">
          <div style="text-align:center">
            <div class="team-logo" style="margin:0 auto 6px;width:44px;height:44px;font-size:20px;">${away.emoji}</div>
            <div>${away.short}</div>
            <div class="form">${formHTML(m.away)}</div>
          </div>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat"><label>主胜赔率</label><strong style="color:var(--accent)">${m.odds.home.toFixed(2)}</strong></div>
        <div class="stat"><label>平局赔率</label><strong style="color:var(--warn)">${m.odds.draw.toFixed(2)}</strong></div>
        <div class="stat"><label>客胜赔率</label><strong style="color:var(--accent-2)">${m.odds.away.toFixed(2)}</strong></div>
        <div class="stat"><label>赔率隐含概率</label>
          <strong>主 ${prob(m.odds.home)}% · 平 ${prob(m.odds.draw)}% · 客 ${prob(m.odds.away)}%</strong>
        </div>
      </div>
    `;
    el("#modal").classList.remove("hidden");
  }

  function closeModal() { el("#modal").classList.add("hidden"); }

  // ---- Bind ----
  function bind() {
    els(".league-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        els(".league-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.league = btn.dataset.league;
        renderMatches();
        renderSchedule();
      });
    });
    el("#date-filter").addEventListener("change", (e) => {
      state.date = e.target.value;
      renderMatches();
      renderSchedule();
    });
    el("#sort-filter").addEventListener("change", (e) => {
      state.sort = e.target.value;
      renderMatches();
    });
    el("#standing-league").addEventListener("change", renderStandings);

    els("[data-close]", el("#modal")).forEach((n) => n.addEventListener("click", closeModal));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });

    // Smooth scroll + active nav on click
    els(".top-nav a").forEach((a) => {
      a.addEventListener("click", () => {
        els(".top-nav a").forEach((x) => x.classList.remove("active"));
        a.classList.add("active");
      });
    });
  }

  // ---- Init ----
  function init() {
    populateDateFilter();
    updateStats();
    renderMatches();
    renderSchedule();
    renderStandings();
    bind();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
