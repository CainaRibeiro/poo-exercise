    const apiUrl = 'http://localhost:8000/api/v1';
    const calcButton = document.querySelector('#send');
    let data;
    document.addEventListener('DOMContentLoaded', async () => {
        const response = await fetch(`${apiUrl}/fornecedores`)
        data = await response.json()

        const select = document.querySelector('#ichoice')

        data.forEach((item) => {
            const newOption = document.createElement('option');

            select.append(newOption);
            newOption.textContent = `${item.Nome}`
        });
    })

    calcButton.addEventListener('click', async () => {
        const transportadora = document.querySelector('#ichoice').value
        const distancia = document.querySelector('#idistance').value
        const result = document.querySelector('#result')
        const errorMsg = document.querySelector('#error')
        const body = {
            nome: transportadora,
            distancia
        }
        const param = {
            method: 'POST',
            body: JSON.stringify(body)
        }

        const response = await fetch(`${apiUrl}/calcula-frete`, param)
        const sendedData = await response.json()

        if (response.ok) {
            errorMsg.textContent = ''
            result.textContent = `${sendedData.mensagem}`;
        } else {
            result.textContent = ''
            errorMsg.textContent = `${sendedData.Error}`
        }

    })