// Appointments

document.addEventListener('DOMContentLoaded', function() {
    let btnAdd = document.querySelector('#ap_button');
    let table = document.querySelector('#ap_table');
    let specialtyInput = document.querySelector('#specialty');
    let dateInput = document.querySelector('#ap_date');
    let hourInput = document.querySelector('#hour');

    btnAdd.addEventListener('click', () => {
        let specialty = specialtyInput.value;
        let date = dateInput.value;
        let hour = hourInput.value;

        let template = `
                    <tr>
                        <td>${specialty}</td>
                        <td>${date}</td>
                        <td>${hour}</td>
                    </tr>`;

    table.innerHTML += template;
    });
});

// Vaccination

document.addEventListener('DOMContentLoaded', function() {
    let btnAdd = document.querySelector('#va_button');
    let table = document.querySelector('#va_table');
    let vaccineInput = document.querySelector('#vaccine');
    let doseInput = document.querySelector('#dose');
    let dateInput = document.querySelector('#va_date');

    btnAdd.addEventListener('click', () => {
        let vaccine = vaccineInput.value;
        let dose = doseInput.value;
        let date = dateInput.value;

        let template = `
                    <tr>
                        <td>${vaccine}</td>
                        <td>${dose}</td>
                        <td>${date}</td>
                    </tr>`;

    table.innerHTML += template;
    });
});