function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


const totalConIva = parseFloat(document.querySelector('.total').dataset.totalConIva);

const mp = new MercadoPago('TEST-4c5e69e7-803c-4ae4-8843-03f15285fdc9', {
    locale: 'es'
});
const bricksBuilder = mp.bricks();
const renderPaymentBrick = async (bricksBuilder) => {
    // Obtener el preferenceId del backend
    fetch('/crear_preferencia/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken // Incluye el token CSRF
        },
        body: new URLSearchParams({
            'transaction_amount': totalConIva
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al crear la preferencia de pago');
            }
            return response.json();
        })
        .then(data => {
            const preferenceId = data.preference_id;

            const settings = {
                initialization: {
                    preferenceId: preferenceId,
                    amount: totalConIva, // Usar el valor calculado
                    payer: {
                        // Aquí puedes incluir datos del pagador si los tienes disponibles en el frontend
                        name: "",
                        surname: "",
                        email: "",
                    },
                },
                customization: {
                    visual: {
                        style: {
                            theme: "default",
                        },
                    },
                    paymentMethods: {
                        ticket: "all",
                        atm: "all",
                        onboarding_credits: "all",
                        debitCard: "all",
                        creditCard: "all",
                        maxInstallments: 12
                    },
                },
                callbacks: {
                    onReady: () => {
                        // Callback llamado cuando el Brick está listo.
                    },
                    onSubmit: ({ selectedPaymentMethod, formData }) => {
                        // callback llamado al hacer clic en el botón de envío de datos
                        return new Promise((resolve, reject) => {
                            fetch("/process_payment/", { // Asegúrate de usar la ruta correcta
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json",
                                    "X-CSRFToken": csrftoken // Incluye el token CSRF
                                },
                                body: JSON.stringify(formData),
                            })
                                .then((response) => {
                                    if (!response.ok) {
                                        throw new Error('Error al procesar el pago');
                                    }
                                    return response.json();
                                })
                                .then((response) => {
                                    // Redirigir a la página de éxito del pago
                                    window.location.href = "/pago_exitoso/"; // Asegúrate de tener esta ruta definida en Django
                                })
                                .catch((error) => {
                                    // manejar la respuesta de error al intentar crear el pago
                                    console.error('Error:', error);
                                    reject(error);
                                });
                        });
                    },
                    onError: (error) => {
                        // callback llamado para todos los casos de error de Brick
                        console.error(error);
                    },
                },
            };

            window.paymentBrickController = bricksBuilder.create(
                "payment",
                "paymentBrick_container",
                settings
            );
        })
        .catch(error => {
            console.error('Error:', error);
            // Mostrar un mensaje de error al usuario
        });
};

renderPaymentBrick(bricksBuilder);
