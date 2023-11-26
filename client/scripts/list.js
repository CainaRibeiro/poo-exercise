 const apiUrl = 'http://localhost:8000/api/v1';
    let data;
    document.addEventListener('DOMContentLoaded', async function () {
        const response = await fetch(`${apiUrl}/fornecedores`)
        let properties;

        data = await response.json()

        const tableBody = document.getElementById('table-body');

        if (response.ok) {
            data.forEach((item) => {
                const row = document.createElement('tr');

                properties = ['Nome', 'Estado', 'Preco_km', 'Email', 'Telefone', 'Avaliacao'];
                properties.forEach((prop) => {
                    const cell = document.createElement('td');
                    cell.textContent = item[prop];
                    row.appendChild(cell);
                });
                const removeButtonCell = document.createElement('td');
                const removeButton = document.createElement('button');
                removeButton.id = 'reset'
                removeButtonCell.style.textAlign = 'center';
                removeButton.textContent = 'Remover';
                removeButton.addEventListener('click', async () => {
                    const body = {
                        nome: item.Nome
                    }
                    const param = {
                        method: 'POST',
                        body: JSON.stringify(body)
                    }
                    const resp = confirm('Tem certeza que deseja remover a transportadora?')
                    if (resp) {
                        await fetch(`${apiUrl}/remover_fornecedor`, param)
                        alert('Transportadora removida com sucesso!')
                        tableBody.removeChild(row);
                    }
                });
                removeButtonCell.appendChild(removeButton);
                row.appendChild(removeButtonCell);

                tableBody.appendChild(row);
            })
        } else {
            const emptyRow = document.createElement('tr');
            const emptyCell = document.createElement('td');
            emptyCell.colSpan = properties.length;
            emptyCell.textContent = 'Tabela vazia';
            emptyRow.appendChild(emptyCell);
            tableBody.appendChild(emptyRow);
        }
    })
    const searchIcon = document.querySelector('#searchImg')
    const searchInput = document.querySelector('#search')

    async function search() {
        const searchInputValue = searchInput.value;
        const errorMsg = document.querySelector('.error')
        let filteredData;
        const body = {
            nome: searchInputValue.length !== 2 ? searchInputValue : "",
            estado: searchInputValue.length === 2 ? searchInputValue : ""
        };
        const param = {
            method: 'POST',
            body: JSON.stringify(body)
        };
        try {
            const response = await fetch(`${apiUrl}/fornecedor`, param);
            filteredData = await response.json();

            const filteredDiv = document.querySelector('.filtered-data');
            filteredDiv.innerHTML = '';

            const table = document.createElement('table');

            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            if (response.ok) {
                const headerProperties = ['Nome', 'Estado', 'Preco por km', 'Email', 'Telefone', 'Avaliação'];
                headerProperties.forEach(prop => {
                    const th = document.createElement('th');
                    th.textContent = prop;
                    headerRow.appendChild(th);
                });
                thead.appendChild(headerRow);

                table.appendChild(thead);
                filteredDiv.appendChild(table);
            }
            const tbody = document.createElement('tbody');
            filteredData.forEach(item => {
                const row = document.createElement('tr');
                const properties = ['Nome', 'Estado', 'Preco_km', 'Email', 'Telefone', 'Avaliacao'];
                properties.forEach(prop => {
                    const cell = document.createElement('td');
                    cell.textContent = item[prop];
                    row.appendChild(cell);
                });
                tbody.appendChild(row);
            });
            errorMsg.textContent = ''
            table.appendChild(tbody);
        } catch (error) {
            errorMsg.textContent = `${filteredData.Error}`
        }
    }

    searchIcon.addEventListener('click', search);
    searchInput.addEventListener('keyup', function (event) {
    if (event.key === 'Enter') {
        search();
    }
});