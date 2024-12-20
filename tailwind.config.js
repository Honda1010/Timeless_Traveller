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
      backgroundImage: {
        'Temple': "url('./static/Images/Abu_Smibel.jpg')",
        'Dream-Park': "url('./static/Images/Dream_park.jpg')",
        'Restaurant_img': "url('./static/Images/Restaurant_image.png')",
        'Hotel': "url('./static/Images/Sunrise_or_Sunset.jpg')",
        'Four_photos': "url('./static/Images/Blank_4_Grids_Collage.png')"
        
      },

    },
  },
  plugins: [],
}

