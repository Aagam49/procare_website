/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0f766e',
        'primary-dark': '#115e59',
        accent: '#f59e0b',
        warm: '#f8fafc'
      },
      boxShadow: {
        soft: '0 18px 45px rgba(15, 118, 110, 0.08)'
      }
    }
  },
  plugins: [],
}
