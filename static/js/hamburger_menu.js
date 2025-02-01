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


let logout_btns = document.getElementsByClassName('logout_button')
if (logout_btns.length > 0) {
    for (let i = 0; i < logout_btns.length; i++) {
        logout_btns[i].addEventListener('click', function () {
            if (confirm("Are you sure?") === true) {
                window.location.href = "/logout";
            }
        })
    }
}

