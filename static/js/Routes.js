window.onload = function () {
    console.log(`api/get_routes/${userId}`)
    // JsBarcode("#barcode", "Hi!");
    fetch(`api/get_routes/${userId}`)
        .then(response => response.json())
        .then(routes => {
            for (let route in routes) {
                createRouteCard(routes[route]);
            }

        })
        .catch(error => console.error(error));
}

function createRouteCard(route) {
    let card = document.createElement('div');
    card.className = 'route_card';

    let ref = document.createElement('h3');
    ref.className = 'ref';
    ref.textContent = `ref #${route['id'].toString().padStart(8, '0')}`;
    card.appendChild(ref);

    let leftSide = document.createElement('div');

    let startDateParts = route['date_of_start'].split('/');
    let endDateParts = route['date_of_end'].split('/');
    let start_date = new Date(startDateParts[2], startDateParts[1] - 1, startDateParts[0])
    let end_date = new Date(endDateParts[2], endDateParts[1] - 1, endDateParts[0])
    let readableDate1 = start_date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' });
    let readableDate2 = end_date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' });
    let duration = Math.ceil((end_date - start_date) / (1000 * 60 * 60 * 24));

    leftSide.className = 'left_side';
    leftSide.innerHTML = `
        <h3>${route['price']}$</h3>
        <h3>${route['distance']}km</h3>
        <h3>${readableDate1} - ${readableDate2}</h3>
    `;
    card.appendChild(leftSide);

    let rightSide = document.createElement('div');

    destinations = route['destinations'];
    console.log(destinations)

    startDest = destinations[0]
    endDest = destinations[destinations.length - 1]
    startImagePath = `../static/img/cities/${startDest.split(" ").join("_")}.jpg`
    endImagePath = `../static/img/cities/${endDest}.jpg`
    rightSide.className = 'right_side';
    rightSide.innerHTML = `
        <div class="route_destination">
            <img src="${startImagePath}" alt="">
            <h2>${startDest}</h2>
        </div>
        <div class="meta_info">
            <span>${duration} days</span>
            <img src="static/img/icons/arrow.svg" alt="">
        </div>
        <div class="route_destination">
            <img src="${endImagePath}" alt="">
            <h2>${endDest}</h2>
        </div>
        <span class="coupontooltip">${destinations.join(', ')}</span>
    `;
    card.appendChild(rightSide);

    let idDiv = document.createElement('div');
    idDiv.className = 'id';
    let barcodeImg = document.createElement('img');
    barcodeImg.src = 'static/img/barcode.png';
    barcodeImg.alt = '';
    idDiv.appendChild(barcodeImg);
    card.appendChild(idDiv);

    document.querySelector('.route_container').appendChild(card);
}