/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/*.html',
   './script/main.js' 
  ],
  theme: {
    extend: {
      colors: {
        sand: '#E0C097',
        desert: '#D88A48',
        sunset: '#C64924',
        'black-dark':'#00000050',
        'white-light':'#FFFFFF30',
        'white-light':'#FFFFFF30',
        'white-medium':'#FFFFFF40',
      },
    },
  },
  plugins: [],
}

