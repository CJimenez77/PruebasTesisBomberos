/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        bomberos: {
          bg: '#211E1A',
          surface: '#2B2824',
          card: '#33302B',
          border: '#48433B',
          sidebar: '#B81313',
          'sidebar-dark': '#8B0D0D',
          red: '#E71506',
          'red-hover': '#C71205',
          gold: '#D97706',
          muted: '#9CA3AF',
        }
      }
    },
  },
  plugins: [],
}
