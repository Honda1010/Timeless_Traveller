function toggle(cardNumber) {

    var content = document.getElementById(`p_${cardNumber}`);
    var arrow_icon = document.getElementById(`arrow_icon_${cardNumber}`);

    // Toggle visibility of the content
    content.classList.toggle('hidden');

    // Toggle the rotation class on the arrow
    arrow_icon.classList.toggle('rotate-180');
}

function toggle_dashboard(menu_number){
    // var option = document.getElementById(`Option_${menu_number}`);
    var option;
    var section;
    // for remove active class from all options
    for(let i=1 ; i<=5;i++){
        option = document.getElementById(`Option_${i}`);
        option.classList.remove('active');
    }
    for(let i=1 ; i<=2;i++){
        section= document.getElementById(`main_${i}`);
        section.classList.add('hidden');
    }
    option= document.getElementById(`Option_${menu_number}`);
    section= document.getElementById(`main_${menu_number}`);
    option.classList.add('active');
    section.classList.remove('hidden');
}
document.addEventListener('DOMContentLoaded', () => {
    const emailField = document.getElementById('email');
    const passwordField = document.getElementById('password');
    const editButton = document.getElementById('edit-btn');
    const saveButton = document.getElementById('save-btn');
    editButton.addEventListener('click', () => {
        emailField.removeAttribute('readonly');
        passwordField.removeAttribute('readonly');
        emailField.classList.remove('cursor-not-allowed', 'bg-gray-200');
        passwordField.classList.remove('cursor-not-allowed', 'bg-gray-200');
        editButton.classList.add('hidden');
        saveButton.classList.remove('hidden');
    });

    saveButton.addEventListener('click', () => {
        emailField.setAttribute('readonly', true);
        passwordField.setAttribute('readonly', true);

        emailField.classList.add('cursor-not-allowed', 'bg-gray-200');
        passwordField.classList.add('cursor-not-allowed', 'bg-gray-200');

        saveButton.classList.add('hidden');
        editButton.classList.remove('hidden');

        // alert('Changes saved!');
    });
});
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
