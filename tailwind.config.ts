import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: '#0B0B0F',
        surface: '#14141C',
        gold: '#D4AF37',
        accent: '#7A5C00',
      },
      boxShadow: {
        glow: '0 0 24px rgba(212, 175, 55, 0.2)',
      },
    },
  },
  plugins: [],
};

export default config;
