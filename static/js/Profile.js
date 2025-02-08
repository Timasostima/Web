document.getElementById('edit').addEventListener('click', () => {
    const form = document.getElementsByTagName('form')[0];
    form.hasAttribute('inert') ? form.removeAttribute('inert') : form.setAttribute('inert', '');
    document.getElementById('contact_info').classList.toggle('active');
})

document.getElementById('save').addEventListener('click', () => {
    const form = document.getElementsByTagName('form')[0];
    form.setAttribute('inert', '');
})

window.onload = () => {
    fetch(`/api/get_route_data/${userId}`)
        .then(response => response.json())
        .then(metadata => {
            console.log(metadata)
            let routes_info = document.getElementById('routes_info')
            routes_info.innerHTML = `<h3><span>${metadata['total_distance']}</span> km in total</h3>` + routes_info.innerHTML
            routes_info.innerHTML = `<h3><span>${metadata['in_progress']}</span> Active routes</h3>` + routes_info.innerHTML
            routes_info.innerHTML = `<h3><span>${metadata['total_routes']}</span> Total Routes</h3>` + routes_info.innerHTML

            let plans = metadata['suscription_data']
            const ctx = document.getElementById('chartsCanvas').getContext('2d')
            const data = {
                labels: Object.keys(plans), datasets: [{
                    label: 'My First Dataset',
                    data: Object.values(plans),
                    backgroundColor: ['rgb(225,133,40)', 'rgb(178,13,13)', 'rgb(24,201,154)'],
                    hoverOffset: 4
                }]
            };

            new Chart(ctx, {
                type: 'doughnut',
                data: data,
                options: {
                    responsive: true, maintainAspectRatio: false, plugins: {
                        legend: {position: 'top', labels: {color: 'rgb(196,136,76)'}},
                        tooltip: {callbacks: {label: context => `${context.label}: ${context.raw}`}},
                    },
                    borderColor: 'black',
                    borderWidth: 0
                },
            });
        })
}


document.getElementById('delete_account').addEventListener('click', function () {
    if (confirm("Are you sure?") === true) {
        window.location.href = "/delete_account";
    }
})
