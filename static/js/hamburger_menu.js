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
    window.addEventListener('resize', function () {
        if (window.innerWidth > 800) {
            navMenu.close();
        }
    });
});

document.querySelector('.login_toggle_menu').addEventListener('click', function () {
    document.querySelector('.list').classList.toggle('hidden');
    document.getElementById('login_img').classList.toggle('active');
});
