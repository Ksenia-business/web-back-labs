function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';  
              
        for(let i = 0; i<films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            let titleContainer = document.createElement('div');
            titleContainer.className = 'film-title-container';

            let russianTitle = document.createElement('div');
            russianTitle.className = 'film-russian-title';
            russianTitle.innerText = films[i].title_ru;
            russianTitle.style.fontWeight = '600';
            russianTitle.style.fontSize = '16px';
            russianTitle.style.color = '#5d4037';
            russianTitle.style.marginBottom = '5px';
            
            titleContainer.append(russianTitle);

            let originalTitle = films[i].title;
            if (originalTitle) {
                let originalTitleElement = document.createElement('div');
                originalTitleElement.className = 'film-original-title';
                originalTitleElement.innerHTML = `<i>(${originalTitle})</i>`;
                originalTitleElement.style.fontStyle = 'italic';
                originalTitleElement.style.fontSize = '14px';
                originalTitleElement.style.color = '#78909c';
                
                titleContainer.append(originalTitleElement);
            }

            tdTitle.append(titleContainer);
            tdYear.innerText = films[i].year;
            tdYear.className = 'film-year';

            let editButton = document.createElement('button');
            editButton.className = 'btn-edit';
            editButton.innerText = 'редактировать';
             editButton.onclick = function() {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.className = 'btn-delete';
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);
            };

            let actionsDiv = document.createElement('div');
            actionsDiv.className = 'action-buttons';
            actionsDiv.append(editButton);
            actionsDiv.append(delButton);
            
            tdActions.append(actionsDiv);

            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        });
}

function showModal() {
    document.getElementById('description-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';

    document.querySelector('div.modal').style.display = 'block';
    document.querySelector('.modal-overlay').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
    document.querySelector('.modal-overlay').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    
    clearErrorMessages();
    
    showModal();
}

function clearErrorMessages() {
    document.getElementById('description-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('title-error').innerText = '';
    document.getElementById('year-error').innerText = '';
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    }

    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST': 'PUT';

    clearErrorMessages();

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return resp.json();
    })
    .then(function(errors) {
        if(errors.description) {
            document.getElementById('description-error').innerText = errors.description;
        }
        if(errors.title_ru) {
            document.getElementById('title-ru-error').innerText = errors.title_ru;
        }
        if(errors.title) {
            document.getElementById('title-error').innerText = errors.title;
        }
        if(errors.year) {
            document.getElementById('year-error').innerText = errors.year;
        }
    });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = film.id;
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;

        showModal();
    });
}