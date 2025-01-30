import {hover_on_center} from './hover_on_center.js';

const photos = document.getElementsByClassName("behind-image")

let clicked = function () {
    const actualPhoto = this.nextElementSibling
    actualPhoto.classList.toggle("clicked")
}
let mouseleave = function () {
    const actualPhoto = this.nextElementSibling
    actualPhoto.classList.remove("clicked")
}
for (let i = 0; i < photos.length; i++) {
    photos[i].addEventListener('click', clicked)
    photos[i].addEventListener('mouseleave', mouseleave)
}


document.addEventListener('scroll', function () {
    const valueCarts = document.querySelectorAll('.value-cart');
    const corporateValuesEnum = document.getElementById('corporate-values-enum');
    const isSingleColumn1 = window.getComputedStyle(corporateValuesEnum).gridTemplateColumns.split(' ').length === 1;

    const managers = document.querySelectorAll('.manager-photo');
    const managerContainer = document.getElementById('manager-list');
    const isSingleColumn2 = window.getComputedStyle(managerContainer).gridTemplateColumns.split(' ').length === 1;


    hover_on_center(valueCarts, isSingleColumn1);
    hover_on_center(managers, isSingleColumn2);
});