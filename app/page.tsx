import Link from 'next/link';
import { matches, replays, videos } from '@/data/mock';

export default function HomePage() {
  const live = matches.filter((m) => m.status === '进行中');
  const upcoming = matches.filter((m) => m.status === '未开始');
  const today = matches.slice(0, 3);

  return (
    <div className="container-page space-y-6">
      <section className="card"><h2 className="mb-3 text-xl font-bold text-gold">今日赛事</h2>{today.map((m) => <p key={m.id}>{m.startTime} · {m.playerA} vs {m.playerB} · {m.tournament}</p>)}</section>
      <section className="card"><h2 className="mb-3 text-xl font-bold text-gold">即将开赛</h2>{upcoming.map((m) => <p key={m.id}>{m.startTime} · {m.playerA} vs {m.playerB}</p>)}</section>
      <section className="card"><h2 className="mb-3 text-xl font-bold text-gold">正在直播</h2>{live.map((m) => <p key={m.id}><a className="underline" href={m.streamUrl} target="_blank">{m.playerA} vs {m.playerB}</a></p>)}</section>
      <section className="grid gap-4 md:grid-cols-2">
        <div className="card"><h2 className="mb-3 text-xl font-bold text-gold">最新比赛录像</h2>{replays.map((r) => <p key={r.id}>{r.title}</p>)}</div>
        <div className="card"><h2 className="mb-3 text-xl font-bold text-gold">最新比赛视频</h2>{videos.map((v) => <p key={v.id}>{v.title}</p>)}</div>
      </section>
      <Link className="inline-block rounded bg-gold px-4 py-2 font-semibold text-black" href="/matches">查看全部赛事</Link>
    </div>
  );
}
