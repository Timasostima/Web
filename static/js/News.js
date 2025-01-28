const slider = document.querySelector('#news-container');
let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener('mousedown', (e) => {
    isDown = true;
    slider.classList.add('active');
    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
});
slider.addEventListener('mouseleave', () => {
    isDown = false;
    slider.classList.remove('active');
});
slider.addEventListener('mouseup', () => {
    isDown = false;
    slider.classList.remove('active');
});
slider.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - slider.offsetLeft;
    const walk = (x - startX);
    slider.scrollLeft = scrollLeft - walk;
});

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('news-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalDescription = document.getElementById('modal-description');
    const modalImage = document.getElementById('modal-image');
    const closeModal = document.querySelector('.modal .close');

    document.querySelectorAll('.read-more').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            modalTitle.textContent = e.target.getAttribute('data-title');
            modalDescription.textContent = e.target.getAttribute('data-description');
            modalImage.src = e.target.getAttribute('data-image');
            modal.showModal();
        });
    });

    closeModal.addEventListener('click', () => {
        modal.close();
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.close();
        }
    });
});