import { matches, replays } from '@/data/mock';

export default function MatchDetail({ params }: { params: { id: string } }) {
  const match = matches.find((m) => m.id === params.id);
  if (!match) return <div className="container-page">比赛不存在</div>;
  return <div className="container-page"><div className="card space-y-2"><h2 className="text-2xl font-bold text-gold">{match.playerA} vs {match.playerB}</h2><p>种族：{match.raceA} vs {match.raceB}</p><p>比分：{match.score}</p><p>地图比分：{match.mapScore.join(' / ') || '待更新'}</p><p><a className="underline" href={match.streamUrl} target="_blank">直播链接</a></p><p><a className="underline" href={match.replayUrl}>回放链接</a></p><div><h3 className="font-semibold">相关 replay</h3>{replays.map((r)=><p key={r.id}>{r.title}</p>)}</div></div></div>;
}
