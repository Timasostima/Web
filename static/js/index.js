const dialog = document.querySelector("#dialog-form");
const showButton = document.querySelector("#calculate-shipment");
const toPrices = document.querySelector('#submit-cities');
const toLast = document.querySelector('#submit-prices');


showButton.addEventListener("click", () => {
    dialog.showModal()
    const prices = document.getElementById("part2")
    prices.style.display = "none"
    const lastForm = document.getElementById("part3")
    lastForm.style.display = "none"
})

toPrices.addEventListener("click", () => {
    const dests = document.getElementById("part1")
    dests.style.display = "none"
    const prices = document.getElementById("part2")
    prices.style.display = "block"
    dialog.style.width = "40%"

    const selectedDestinations = Array.from(destList).map(dest => dest.innerText);
    const params = new URLSearchParams({destinations: selectedDestinations.join(',')});
    fetch(`/api/calculate_travel_route?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            const thead = prices.querySelector("thead");
            const tbody = prices.querySelector("tbody");
            thead.innerHTML = "";
            tbody.innerHTML = "";

            const headerRow = document.createElement("tr");
            headerRow.innerHTML = `
                <td></td>
                ${data.map(plan => `<th style="background-color: rgba(250,171,81,0.82);">${plan.name}</th>`).join('')}
            `;
            thead.appendChild(headerRow);

            const attributes = ['price', 'estimated_date', 'insurance_type', 'tracking'];
            attributes.forEach(attr => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${attr.charAt(0).toUpperCase() + attr.slice(1).replace('_', ' ')}</td>
                    ${data.map(plan => `<td>${plan[attr]}</td>`).join('')}
                `;
                tbody.appendChild(row);
            });

            const subscriptionSelect = document.getElementById("suscription_plan");
            subscriptionSelect.innerHTML = "";
            data.forEach(plan => {
                const option = document.createElement("option");
                option.value = plan.name;
                option.textContent = plan.name;
                subscriptionSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
})

toLast.addEventListener("click", () => {
    const prices = document.getElementById("part2")
    prices.style.display = "none"
    const lastForm = document.getElementById("part3")
    lastForm.style.display = "block"
    dialog.style.width = "30%"

    const selectedDestinations = Array.from(destList).map(dest => dest.innerText);
    const selectedPlan = document.getElementById("suscription_plan").value;
    const params = new URLSearchParams({destinations: selectedDestinations.join(','), plan: selectedPlan});

    fetch(`/api/calculate_distance_price?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("distance_form").textContent = `Total Distance: ${data.distance} km`;
            document.getElementById("price_form").textContent = `Total Price: ${data.price} €`;
        })
        .catch(error => console.error('Error:', error));
})

document.querySelector('#travel').onsubmit = e => {
    e.preventDefault();

    let data = [];
    for (let i = 1; i < destList.length; i++) {
        data.push(destList[i].innerText);
    }

    let plan = document.getElementById('suscription_plan').value;
    let email = document.getElementById('email_input');
    let comment = document.getElementById('comment_input').value;

    let payload = {
        comment_input: comment, suscription_plan: plan, destinations: data, path: trajectory.getAttribute('points'),
    };

    if (email) {
        payload.email_input = email.value;
    }


    fetch('/api/save_travel_route', {
        method: 'POST', headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            alert("Done");
        })
        .catch(error => console.error('Error:', error));

    e.target.reset();
    dialog.close();
    return false;
}

const areas = document.querySelectorAll('[id^="pr_"], [id^="is_"]')
const color = document.querySelector('[id^="pr_"]').style.fill
const bboxRect = document.getElementById('try')
const trajectory = document.getElementById('trajectory')
const currentArea = document.getElementById('current-area-name')
const destinations = document.getElementById('destinations')
let destList = destinations.children


let dgOver = event => {
    event.preventDefault()
}

let clickFun = function () {
    let name = convertToName(this.id)
    const box = this.getBBox()

    if (this.parentElement.id === 'gcanarias') {
        bboxRect.setAttribute('x', box.x - 130 + 403) //g provinces offset
        bboxRect.setAttribute('y', box.y - 31 - 43.6)
    } else {
        bboxRect.setAttribute('x', box.x - 130) //g provinces offset
        bboxRect.setAttribute('y', box.y - 31.6)
    }
    bboxRect.setAttribute('width', box.width)
    bboxRect.setAttribute('height', box.height)

    let Xcenter = bboxRect.getAttribute("width") / 2 + Number(bboxRect.getAttribute('x'))
    let Ycenter = bboxRect.getAttribute("height") / 2 + Number(bboxRect.getAttribute('y'))

    newPoint = ` ${Xcenter},${Ycenter}`
    let point = trajectory.getAttribute("points")

    if (!point.includes(newPoint)) {
        point += newPoint

        const newElement = document.createElement('p')
        newElement.innerHTML = name
        newElement.setAttribute("draggable", true)
        newElement.setAttribute("id", name)
        destinations.appendChild(newElement)
    } else {
        const chToRem = document.getElementById(name)
        point = point.replace(newPoint, '')
        chToRem.remove()
    }

    this.classList.toggle("ac");
    trajectory.setAttributeNS(null, "points", point);
}

let mouseOn = function () {
    let name = convertToName(this.id)
    currentArea.innerText = name
}

function convertToName(id) {
    return id.split("_").map(word => word.charAt(0).toUpperCase() + word.slice(1)).slice(1).join(" ")
}

for (let i = 0; i < areas.length; i++) {
    areas[i].addEventListener('click', clickFun)
    areas[i].addEventListener('mouseenter', mouseOn)
}
destinations.addEventListener('dragover', dgOver)