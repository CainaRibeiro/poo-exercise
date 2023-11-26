    const apiUrl = 'http://localhost:8000/api/v1';
    const sendButton = document.querySelector('#send');
    let data;
    let sendedData;
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

    sendButton.addEventListener('click', async () => {
        const errorMsg = document.querySelector('#error')
        try {
            const transportadora = document.querySelector('#ichoice').value
            const nota = document.querySelector('#igrade').value
            const result = document.querySelector('#result')
            const body = {
                nome: transportadora,
                avaliacao: nota
            }
            const param = {
                method: 'POST',
                body: JSON.stringify(body)
            }

            const response = await fetch(`${apiUrl}/add_avaliacao`, param)
            sendedData = await response.json()

            if (response.ok && (nota <= 10 || nota >= 0) ) {
                errorMsg.textContent = ''
                result.textContent = `${sendedData.mensagem}`;
            } else {
                errorMsg.textContent = `${sendedData.Error}`
            }
        } catch (error) {
            errorMsg.textContent = `${error}`
        }
    })