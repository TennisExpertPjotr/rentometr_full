/*
document.querySelector('.room-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = {
        room_type: document.querySelector('.room-btn.active').textContent,
        total_meters: document.querySelector('input[name="total_meters"]').value,
        district: document.querySelector('select[name="district"]').value,
        street: document.querySelector('input[name="street"]').value,
        house_number: document.querySelector('input[name="house_number"]').value,
        floor: document.querySelector('input[name="floor"]').value,
        total_floors: document.querySelector('input[name="total_floors"]').value,
        house_material: document.querySelector('select[name="house_material"]').value,
        balcony: document.querySelector('input[name="balcony"]:checked').value,
        metro_station: document.querySelector('#metro_station').value,
        ml_model: document.querySelector('#ml_model').value
    };

    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Оцениваем...';

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.status === 'success') {
            //const formattedPrice = new Intl.NumberFormat('ru-RU').format(result.predicted_price);
            const predicted = result.predicted_price;
            const formattedPrice = (typeof predicted === 'string')
                ? predicted
                : new Intl.NumberFormat('ru-RU').format(predicted);

            const resultContainer = document.getElementById('resultContainer');
            const priceElement = document.getElementById('predictedPrice');
            const homeInfo = document.getElementById('homeInfo');

            priceElement.textContent = formattedPrice;
            resultContainer.style.display = 'block';
            homeInfo.style.marginBottom = '15px';

            resultContainer.style.opacity = 0;
            setTimeout(() => {
                resultContainer.style.transition = 'opacity 0.5s ease';
                resultContainer.style.opacity = 1;
            }, 10);
        } else {
            console.error('Error:', result.message);
            alert('Error occurs: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error occurs');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Оценить';
    }
});
*/


document.querySelector('.room-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = {
        room_type: document.querySelector('.room-btn.active').textContent,
        total_meters: document.querySelector('input[name="total_meters"]').value,
        district: document.querySelector('select[name="district"]').value,
        street: document.querySelector('input[name="street"]').value,
        house_number: document.querySelector('input[name="house_number"]').value,
        floor: document.querySelector('input[name="floor"]').value,
        total_floors: document.querySelector('input[name="total_floors"]').value,
        house_material: document.querySelector('select[name="house_material"]').value,
        balcony: document.querySelector('input[name="balcony"]:checked').value,
        metro_station: document.querySelector('#metro_station').value,
        ml_model: document.querySelector('#ml_model').value
    };

    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Оцениваем...';

    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (result.status === 'success') {
            const predicted = result.predicted_price;
            const formattedPrice = (typeof predicted === 'string')
                ? predicted
                : new Intl.NumberFormat('ru-RU').format(predicted);

            const resultContainer = document.getElementById('resultContainer');
            const priceElement = document.getElementById('predictedPrice');
            const homeInfo = document.getElementById('homeInfo');

            priceElement.textContent = formattedPrice;
            resultContainer.style.display = 'block';
            homeInfo.style.marginBottom = '15px';

            resultContainer.style.opacity = 0;
            setTimeout(() => {
                resultContainer.style.transition = 'opacity 0.5s ease';
                resultContainer.style.opacity = 1;
            }, 10);
        } else {
            console.error('Error:', result.message);
            alert('Error occurs: ' + result.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error occurs');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Оценить';
    }
});
