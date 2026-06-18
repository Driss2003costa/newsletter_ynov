/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Museum gallery palette — warm neutrals, ink, a single oxblood accent.
        canvas: '#F4F1EA', // gallery wall
        paper: '#FBF9F4', // label / card
        ink: '#1B1714', // near-black, warm
        muted: '#6B6258', // captions
        line: '#E2DACB', // hairline rules / borders
        accent: {
          DEFAULT: '#7A2E2E', // oxblood
          soft: '#9A4A40',
          50: '#F6ECE9',
        },
        gold: '#A9853E',
      },
      fontFamily: {
        serif: ['Fraunces', 'Georgia', 'Times New Roman', 'serif'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      letterSpacing: {
        eyebrow: '0.22em',
      },
      boxShadow: {
        frame: '0 1px 0 0 #E2DACB, 0 24px 48px -32px rgba(27,23,20,0.35)',
      },
    },
  },
  plugins: [],
}
