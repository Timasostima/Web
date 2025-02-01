export function hover_on_center(cards, isSingleColumn){
  cards.forEach(cart => {
    const rect = cart.getBoundingClientRect();
    const topInCenter = rect.top >= window.innerHeight / 2 - rect.height * 1.3
    const bottomInCenter = rect.bottom <= window.innerHeight / 2 + rect.height * 1.3
    const isInCenter = topInCenter && bottomInCenter
    const isInMobileMode = window.innerWidth <= 800

    if (isInCenter && isSingleColumn && isInMobileMode) {
      cart.classList.add('hover');
    } else {
      cart.classList.remove('hover');
    }
  });
}