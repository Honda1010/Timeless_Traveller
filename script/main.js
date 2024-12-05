
const bar_xmark_toggle = document.getElementById('bar_xmark_toggle');
const BarIcon = document.getElementById('bar_icon');
const XamrkIcon = document.getElementById('xmark_icon');
const menuToggle = document.getElementById('mobile-menu');
XamrkIcon.classList.add('hidden');
bar_xmark_toggle.addEventListener('click', function() {
    menuToggle.classList.toggle('hidden');
    BarIcon.classList.toggle('hidden');
    XamrkIcon.classList.toggle('hidden');
});

