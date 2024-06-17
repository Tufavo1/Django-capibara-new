document.getElementById('saveBtn').addEventListener('click', function () {
    const nombre = document.getElementById('nombreInput').value;
    const email = document.getElementById('emailInput').value;
    const direccion = document.getElementById('direccionInput').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmNewPassword = document.getElementById('confirmNewPassword').value;

    if (newPassword !== confirmNewPassword) {
        alert('Las contraseñas no coinciden.');
        return;
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/perfil/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            nombre: nombre,
            email: email,
            direccion: direccion,
            newPassword: newPassword,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('nombre').textContent = nombre;
            document.getElementById('email').textContent = email;
            document.getElementById('direccion').textContent = direccion;

            document.querySelectorAll('span').forEach(span => span.style.display = 'block');
            document.querySelectorAll('input').forEach(input => input.style.display = 'none');
            document.getElementById('editBtn').style.display = 'inline-block';
            document.getElementById('cancelBtn').style.display = 'none';
            document.getElementById('saveBtn').style.display = 'none';
        } else {
            alert('Error al actualizar los datos.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('editBtn').addEventListener('click', function () {
    document.querySelectorAll('span').forEach(span => span.style.display = 'none');
    document.querySelectorAll('input').forEach(input => input.style.display = 'block');
    document.getElementById('editBtn').style.display = 'none';
    document.getElementById('cancelBtn').style.display = 'inline-block';
    document.getElementById('saveBtn').style.display = 'inline-block';
});

document.getElementById('cancelBtn').addEventListener('click', function () {
    document.querySelectorAll('span').forEach(span => span.style.display = 'block');
    document.querySelectorAll('input').forEach(input => input.style.display = 'none');
    document.getElementById('editBtn').style.display = 'inline-block';
    document.getElementById('cancelBtn').style.display = 'none';
    document.getElementById('saveBtn').style.display = 'none';
});

document.getElementById('saveBtn').addEventListener('click', function () {
    const nombre = document.getElementById('nombreInput').value;
    const email = document.getElementById('emailInput').value;
    const direccion = document.getElementById('direccionInput').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmNewPassword = document.getElementById('confirmNewPassword').value;

    if (newPassword !== confirmNewPassword) {
        alert('Las contraseñas no coinciden.');
        return;
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/perfil/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            nombre: nombre,
            email: email,
            direccion: direccion,
            newPassword: newPassword,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('nombre').textContent = nombre;
            document.getElementById('email').textContent = email;
            document.getElementById('direccion').textContent = direccion;

            document.querySelectorAll('span').forEach(span => span.style.display = 'block');
            document.querySelectorAll('input').forEach(input => input.style.display = 'none');
            document.getElementById('editBtn').style.display = 'inline-block';
            document.getElementById('cancelBtn').style.display = 'none';
            document.getElementById('saveBtn').style.display = 'none';
        } else {
            alert('Error al actualizar los datos.');
        }
    })
    .catch(error => console.error('Error:', error));
});
