
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


function toggle(cardNumber) {

    var p = document.getElementById(`p_${cardNumber}`);
    var up_icon = document.getElementById(`up_${cardNumber}`);
    var down_icon = document.getElementById(`down_${cardNumber}`);

    if(getComputedStyle(p).display === "none") {
        p.style.display = "block";
        down_icon.style.display = "none";
        up_icon.style.display = "block";
    }
    else {
        p.style.display = "none";
        down_icon.style.display = "block";
        up_icon.style.display = "none";
    }
}

