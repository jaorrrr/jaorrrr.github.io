/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        rosetti: {
          white: '#FAFAFA',
          red: '#C8102E',
          redDark: '#9E0B22',
          black: '#1A1A1A',
          green: '#008C45',
        },
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'serif'],
        sans: ['Inter', 'sans-serif'],
      },
      backgroundImage: {
        kraft:
          "linear-gradient(rgba(250,250,250,0.94), rgba(250,250,250,0.94)), repeating-linear-gradient(45deg, rgba(26,26,26,0.03) 0, rgba(26,26,26,0.03) 1px, transparent 1px, transparent 12px)",
      },
    },
  },
  plugins: [],
};
