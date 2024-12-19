// Função para fazer a busca dinamicamente
function performSearch() {
    const input = document.getElementById('searchInput').value.trim();
    const currentPage = document.querySelector('.pagination .active').textContent.trim() || 1;  // Pega a página atual ou 1 por padrão

    // Se o input estiver vazio, busca sem filtro (mantém a página atual)
    const queryParam = input ? `?query=${encodeURIComponent(input)}&page=${currentPage}` : `?page=${currentPage}`;

    fetch(`/search_books/${queryParam}`)
        .then(response => response.json())
        .then(data => {
            const bookGrid = document.getElementById('bookGrid');
            bookGrid.innerHTML = ''; // Limpa o grid atual

            // Adiciona dinamicamente os livros no grid
            data.books.forEach(book => {
                bookGrid.innerHTML += `
                    <div class="col">
                        <div class="card card-transition mx-auto">
                            <a style="color: inherit" href="/book_detail/${book.id}/">
                                ${book.cover_image ? 
                                    `<img src="${book.cover_image}" class="card-img-top" alt="Capa de ${book.title}">` : 
                                    `<img src="https://dummyimage.com/200x250/787878/fff&text=No+image" class="card-img-top" alt="Capa de ${book.title}">`}
                                <div class="card-body">
                                    <p class="card-title padding-card">${book.title}</p>
                                    <div>
                                        <span class="card-bold margin-card-body">Author: </span>
                                        <span class="card-text">${book.author}</span>                    
                                    </div>
                                    <div>
                                        <span class="card-bold margin-card-body">Publicação: </span>
                                        <span class="card-text">${book.year}</span>
                                    </div>
                                    <div>
                                        <span class="card-bold margin-card-body">ISBN: </span>
                                        <span class="card-text">${book.isbn}</span>
                                    </div>
                                </div>
                            </a>
                        </div>
                    </div>`;
            });

            // Atualiza os controles de paginação
            updatePagination(data);
        })
        .catch(error => console.error('Erro ao buscar livros:', error));
}

// Função para atualizar a paginação dinamicamente
function updatePagination(data) {
    const pagination = document.getElementById('paginationControls');
    if (pagination) {
        pagination.innerHTML = ''; // Limpa a paginação atual

        if (data.has_previous) {
            pagination.innerHTML += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="changePage(${data.current_page - 1})">Anterior</a>
                </li>`;
        }

        for (let i = 1; i <= data.total_pages; i++) {
            pagination.innerHTML += `
                <li class="page-item ${i === data.current_page ? 'active' : ''}">
                    <a class="page-link" href="#" onclick="changePage(${i})">${i}</a>
                </li>`;
        }

        if (data.has_next) {
            pagination.innerHTML += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="changePage(${data.current_page + 1})">Próxima</a>
                </li>`;
        }
    }
}

function changePage(page) {
    const input = document.getElementById('searchInput').value.trim();

    const queryParam = input ? `?query=${encodeURIComponent(input)}&page=${page}` : `?page=${page}`;

    fetch(`/search_books/${queryParam}`)
        .then(response => response.json())
        .then(data => {
            const bookGrid = document.getElementById('bookGrid');
            bookGrid.innerHTML = ''; // Limpa o grid atual

            data.books.forEach(book => {
                bookGrid.innerHTML += `
                    <div class="col">
                        <div class="card card-transition mx-auto">
                            <a style="color: inherit" href="/book_detail/${book.id}/">
                                ${book.cover_image ? 
                                    `<img src="${book.cover_image}" class="card-img-top" alt="Capa de ${book.title}">` : 
                                    `<img src="https://dummyimage.com/200x250/787878/fff&text=No+image" class="card-img-top" alt="Capa de ${book.title}">`}
                                <div class="card-body">
                                    <p class="card-title padding-card">${book.title}</p>
                                    <div>
                                        <span class="card-bold margin-card-body">Author: </span>
                                        <span class="card-text">${book.author}</span>                    
                                    </div>
                                    <div>
                                        <span class="card-bold margin-card-body">Publicação: </span>
                                        <span class="card-text">${book.year}</span>
                                    </div>
                                    <div>
                                        <span class="card-bold margin-card-body">ISBN: </span>
                                        <span class="card-text">${book.isbn}</span>
                                    </div>
                                </div>
                            </a>
                        </div>
                    </div>`;
            });

            updatePagination(data);
        })
        .catch(error => console.error('Erro ao mudar de página:', error));
}