document.addEventListener('DOMContentLoaded', function () {
    const hamburger1 = document.getElementById('hamburger_closed');
    const hamburger2 = document.getElementById('hamburger_opened');
    const navMenu = document.getElementById('navbar_dialog');

    hamburger1.addEventListener('click', function () {
        navMenu.showModal()
    });
    hamburger2.addEventListener('click', function () {
        navMenu.close()
    });
});