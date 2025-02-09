const steps = document.querySelectorAll('.form-step');
const stepIndicators = document.querySelectorAll('.step');
const dialogForm = document.getElementById('dialog-form');
const travelForm = document.getElementById('travel');
let currentStep = 0;
const totalSteps = steps.length;

const btnNextCities = document.getElementById('submit-cities');
const btnNextPrices = document.getElementById('submit-prices');


document.getElementById('calculate-shipment').addEventListener('click', () => {
    dialogForm.showModal();
})

function goToNextStep() {
    steps[currentStep].classList.remove('active');
    stepIndicators[currentStep].classList.remove('active');
    currentStep++;
    if (currentStep >= totalSteps) {
        currentStep = 0;
    }
    steps[currentStep].classList.add('active');
    stepIndicators[currentStep].classList.add('active');
}

function goToFirstStep() {
    steps[currentStep].classList.remove('active');
    stepIndicators[currentStep].classList.remove('active');
    currentStep = 0;
    steps[currentStep].classList.add('active');
    stepIndicators[currentStep].classList.add('active');
}

btnNextCities.addEventListener('click', () => {
    const prices = document.getElementById("part2")
    const selectedDestinations = Array.from(destList).map(dest => dest.innerText);
    const params = new URLSearchParams({destinations: selectedDestinations.join(',')});

    if (selectedDestinations.length < 3) {
        alert("Please select at least two destinations.");
        return;
    }

    fetch(`/api/calculate_travel_route?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const thead = prices.querySelector("thead");
            const tbody = prices.querySelector("tbody");
            thead.innerHTML = "";
            tbody.innerHTML = "";

            const headerRow = document.createElement("tr");
            headerRow.innerHTML = `
                <td></td>
                ${data.map(plan => `<th>${plan.name}</th>`).join('')}
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

            const subscriptionSelect = document.getElementById("subscription_plan");
            subscriptionSelect.innerHTML = "";
            data.forEach(plan => {
                const option = document.createElement("option");
                option.value = plan.name;
                option.textContent = plan.name;
                subscriptionSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
    goToNextStep();
});

btnNextPrices.addEventListener('click', () => {
    const selectedDestinations = Array.from(destList).map(dest => dest.innerText);
    const selectedPlan = document.getElementById("subscription_plan").value;
    const params = new URLSearchParams({destinations: selectedDestinations.join(','), plan: selectedPlan});

    fetch(`/api/calculate_distance_price?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("distance_form").textContent = `Total Distance: ${data.distance} km`;
            document.getElementById("price_form").textContent = `Total Price: ${data.price} €`;
        })
        .catch(error => console.error('Error:', error));
    goToNextStep();
});

function resetForm() {
    let points = trajectory.getAttribute("points")
    points.replace(points, '')
    trajectory.setAttributeNS(null, "points", points)
    let destList = document.getElementById('destinations').children
    for (let i = 1; i < destList.length; i++) {
        destList[i].remove()
    }
    travelForm.reset()
    dialogForm.close()
}

travelForm.addEventListener('submit', (event) => {
    event.preventDefault();

    let data = [];
    for (let i = 1; i < destList.length; i++) {
        data.push(destList[i].innerText);
    }

    let plan = document.getElementById('subscription_plan').value;
    let email = document.getElementById('email_input');
    let comment = document.getElementById('comment_input').value;
    let points = trajectory.getAttribute('points');

    let payload = {
        comment_input: comment, subscription_plan: plan, destinations: data, path: points,
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
            alert("Form submitted successfully!")
        })
        .catch(error => console.error('Error:', error));

    resetForm()
    goToNextStep()
});

dialogForm.addEventListener('cancel', (e) => {
    e.preventDefault();
    if (confirm("Are you sure you want to close the form? Unsaved changes will be lost.")) {
        resetForm();
        goToFirstStep();
    }
});

stepIndicators.forEach((indicator, index) => {
    indicator.addEventListener('click', () => {
        if (index <= currentStep) {
            steps[currentStep].classList.remove('active');
            stepIndicators[currentStep].classList.remove('active');
            currentStep = index;
            steps[currentStep].classList.add('active');
            stepIndicators[currentStep].classList.add('active');
        }
    });
});

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

    let newPoint = ` ${Xcenter},${Ycenter}`
    let points = trajectory.getAttribute("points")

    if (!points.includes(newPoint)) {
        points += newPoint

        const newElement = document.createElement('p')
        newElement.innerHTML = name
        newElement.setAttribute("draggable", true)
        newElement.setAttribute("id", name)
        destinations.appendChild(newElement)
    } else {
        const chToRem = document.getElementById(name)
        points = points.replace(newPoint, '')
        chToRem.remove()
    }

    this.classList.toggle("ac");
    trajectory.setAttributeNS(null, "points", points);
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