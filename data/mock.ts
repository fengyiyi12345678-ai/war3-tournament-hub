export type MatchStatus = '未开始' | '进行中' | '已结束';

export const tournaments = [
  { id: 't1', name: '黄金联赛 S4' },
  { id: 't2', name: '斗鱼大师杯' },
];

export const players = [
  { id: 'p1', name: '120', race: 'Undead', country: '中国' },
  { id: 'p2', name: 'Moon', race: 'Night Elf', country: '韩国' },
  { id: 'p3', name: 'Lyn', race: 'Orc', country: '韩国' },
  { id: 'p4', name: 'Happy', race: 'Undead', country: '俄罗斯' },
];

export const matches = [
  {
    id: 'm1',
    tournament: '黄金联赛 S4',
    status: '进行中' as MatchStatus,
    playerA: '120',
    raceA: 'Undead',
    playerB: 'Moon',
    raceB: 'Night Elf',
    score: '1:1',
    mapScore: ['EI 1:0', 'TS 0:1'],
    startTime: '2026-05-09 19:00',
    streamUrl: 'https://www.douyu.com/',
    replayUrl: '#',
  },
  {
    id: 'm2',
    tournament: '斗鱼大师杯',
    status: '未开始' as MatchStatus,
    playerA: 'Lyn',
    raceA: 'Orc',
    playerB: 'Happy',
    raceB: 'Undead',
    score: '0:0',
    mapScore: [],
    startTime: '2026-05-09 21:30',
    streamUrl: 'https://live.bilibili.com/',
    replayUrl: '#',
  },
  {
    id: 'm3',
    tournament: '黄金联赛 S4',
    status: '已结束' as MatchStatus,
    playerA: '120',
    raceA: 'Undead',
    playerB: 'Happy',
    raceB: 'Undead',
    score: '2:3',
    mapScore: ['CH 1:0', 'AZ 0:1', 'LR 0:1', 'TS 1:0', 'TM 0:1'],
    startTime: '2026-05-08 20:00',
    streamUrl: 'https://www.huya.com/',
    replayUrl: '#',
  },
];

export const replays = [
  { id: 'r1', title: '120 vs Moon BO3', playerA: '120', playerB: 'Moon', map: 'TS', version: '1.36', source: 'NGA', downloadUrl: '#' },
  { id: 'r2', title: 'Lyn vs Happy BO5', playerA: 'Lyn', playerB: 'Happy', map: 'TM', version: '1.36', source: 'CC直播', downloadUrl: '#' },
];

export const videos = [
  { id: 'v1', title: '黄金联赛半决赛集锦', platform: 'Bilibili', channel: 'War3赛事中心', cover: 'https://picsum.photos/seed/war3a/640/360', url: 'https://www.bilibili.com/', publishedAt: '2026-05-08' },
  { id: 'v2', title: 'Moon 精彩翻盘局', platform: 'YouTube', channel: 'WC3 Highlights', cover: 'https://picsum.photos/seed/war3b/640/360', url: 'https://www.youtube.com/', publishedAt: '2026-05-07' },
];
