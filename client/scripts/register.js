    const apiUrl = 'http://localhost:8000/api/v1';

    document.querySelector('#myForm').addEventListener('submit', async (event) => {
        event.preventDefault()
        const nome = document.querySelector('#nome').value;
        const estado = document.querySelector('#istate').value;
        const preco = document.querySelector('#preco').value
        const email = document.querySelector('#email').value
        const telefone = document.querySelector('#telefone').value

        const body = {
            nome,
            estado,
            preco_km: preco,
            email,
            telefone
        }

        const param = {
            method: 'POST',
            body: JSON.stringify(body)
        }
        await fetch(`${apiUrl}/add_fornecedor`, param)
            .then(async (response) => {
                if (response.ok) {
                    alert(`${body.nome} cadastrado com sucesso!`);
                    document.querySelector('#nome').value = '';
                    document.querySelector('#istate').value = '';
                    document.querySelector('#preco').value = '';
                    document.querySelector('#email').value = '';
                    document.querySelector('#telefone').value = '';
                } else {
                    throw new Error(`${response.mensagem}`);
                }
            })
            .catch((error) => {
                alert(`Erro: ${error.message}`);
            });
    })