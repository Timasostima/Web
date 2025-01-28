import {hover_on_center} from './hover_on_center.js';

document.addEventListener('scroll', function () {
    const valueCarts = document.querySelectorAll('.service');
    const corporateValuesEnum = document.getElementById('services');
    const isSingleColumn = window.getComputedStyle(corporateValuesEnum).gridTemplateColumns.split(' ').length === 1;

    hover_on_center(valueCarts, isSingleColumn);
});

