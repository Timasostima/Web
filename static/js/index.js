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
})

toLast.addEventListener("click", () => {
    const prices = document.getElementById("part2")
    prices.style.display = "none"
    const lastForm = document.getElementById("part3")
    lastForm.style.display = "block"
    dialog.style.width = "30%"
})

document.querySelector('#travel').onsubmit = e => {
    e.preventDefault();

    let data = [];
    for (let i = 1; i < destList.length; i++) {
        data.push(destList[i].innerText);
    }

    let plan = document.getElementById('suscription_plan').value;


    const payload = {
        email_input: document.getElementById('email_input').value,
        comment_input: document.getElementById('comment_input').value,
        suscription_plan: plan,
        destinations: data,
        path: trajectory.getAttribute('points'),
    };

    fetch('/api/save_travel_route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
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
    let name = id.split("_").map(word => word.charAt(0).toUpperCase() + word.slice(1)).slice(1).join(" ")
    return name
}

for (let i = 0; i < areas.length; i++) {
    areas[i].addEventListener('click', clickFun)
    areas[i].addEventListener('mouseenter', mouseOn)
}
destinations.addEventListener('dragover', dgOver)