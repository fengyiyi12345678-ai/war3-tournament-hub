import Link from 'next/link';
import { matches } from '@/data/mock';

export default function MatchesPage({ searchParams }: { searchParams?: { status?: string } }) {
  const status = searchParams?.status;
  const filtered = status ? matches.filter((m) => m.status === status) : matches;
  const tabs = ['未开始', '进行中', '已结束'];
  return <div className="container-page space-y-4"><h2 className="text-2xl font-bold text-gold">赛事列表</h2><div className="flex gap-2">{tabs.map((t)=><Link key={t} href={`/matches?status=${t}`} className="card px-3 py-2">{t}</Link>)}</div><div className="space-y-3">{filtered.map((m)=><Link href={`/matches/${m.id}`} key={m.id} className="card block"><p>{m.tournament} · {m.status}</p><p>{m.playerA} ({m.raceA}) vs {m.playerB} ({m.raceB})</p><p>{m.score} · {m.startTime}</p></Link>)}</div></div>;
}
