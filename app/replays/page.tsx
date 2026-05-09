import { replays } from '@/data/mock';
export default function ReplaysPage(){return <div className="container-page space-y-3"><h2 className="text-2xl font-bold text-gold">比赛录像</h2>{replays.map((r)=><div key={r.id} className="card"><p>{r.title}</p><p>{r.playerA} vs {r.playerB} · {r.map} · {r.version}</p><p>来源：{r.source}</p><a className="underline" href={r.downloadUrl}>下载链接</a></div>)}</div>}
