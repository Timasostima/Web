import {hover_on_center} from './hover_on_center.js';

document.addEventListener('scroll', function () {
    const services = document.querySelectorAll('.service-text');
    const servicesContainer = document.getElementById('service-motto');
    const isSingleColumn1 = window.getComputedStyle(servicesContainer).gridTemplateColumns.split(' ').length === 1;

    const vacancies = document.querySelectorAll('.vacancy');
    const vacanciesContainer = document.getElementById('vacancies');
    const isSingleColumn2 = window.getComputedStyle(vacanciesContainer).gridTemplateColumns.split(' ').length === 1;

    hover_on_center(services, isSingleColumn1);
    hover_on_center(vacancies, isSingleColumn2);
});
