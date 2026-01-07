/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../index.html",
    "./Src/**/*.{svelte,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        mono: ['"Courier New"', 'Courier', 'monospace'],
        display: ['"Courier New"', 'Courier', 'monospace'],
      },
      colors: {
        dubious: {
          red: '#ff003c',
          dark: '#050505',
          gray: '#1a1a1a',
          light: '#e0e0e0',
        }
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [
    require("tailwindcss-animate")
  ],
}
