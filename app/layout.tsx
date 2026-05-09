import type { Metadata } from 'next';
import './globals.css';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'War3 Tournament Hub',
  description: 'Warcraft III 冰封王座中文赛事资讯聚合站',
};

const nav = [
  ['首页', '/'],
  ['赛事', '/matches'],
  ['录像', '/replays'],
  ['视频', '/videos'],
  ['选手', '/players'],
  ['后台', '/admin'],
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <header className="sticky top-0 z-50 border-b border-gold/20 bg-bg/90 backdrop-blur">
          <div className="container-page flex items-center justify-between py-4">
            <h1 className="text-lg font-semibold text-gold">War3 Tournament Hub</h1>
            <nav className="flex flex-wrap gap-3 text-sm">
              {nav.map(([label, href]) => (
                <Link className="rounded px-2 py-1 hover:bg-gold/10" href={href} key={href}>
                  {label}
                </Link>
              ))}
            </nav>
          </div>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
