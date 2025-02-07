import {hover_on_center} from './hover_on_center.js';

document.addEventListener('scroll', function () {
    const valueCarts = document.querySelectorAll('.service');
    const corporateValuesEnum = document.getElementById('services');
    const isSingleColumn = window.getComputedStyle(corporateValuesEnum).gridTemplateColumns.split(' ').length === 1;

    hover_on_center(valueCarts, isSingleColumn);
});

let services = document.getElementsByClassName('service');
for (let service of services) {
    service.addEventListener('click', function () {
        const img = service.querySelector('img');
        if (img) {
             if (img.src.includes('star.svg')) {
                img.src = '../static/img/icons/star_filled.svg'; // Change to the filled star image URL
            } else {
                img.src = '../static/img/icons/star.svg'; // Change back to the original star image URL
            }
        }
    });
}

