const addButton = document.getElementById('task-submit');
const editButton = document.getElementById("edit-task-submit");
const deleteButton = document.getElementById("delete-task-submit");

const inputField = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');

const loginForm = document.getElementById('login-form');

const loginButton = document.getElementById('login-btn');

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
	return null;
}

function openTaskModal(task) {
	document.getElementById('edit-task-id').value = task[0];
	document.getElementById('edit-task-name').value = task[1];
	document.getElementById('edit-task-description').value = task[2];
	document.getElementById('edit-task-status').value = task[4] ? "completa" : "incompleta";

	const taskModal = new bootstrap.Modal(document.getElementById('edit-taskModal'));
	taskModal.show();
}


addButton.addEventListener('click', () => {

	const taskName = document.getElementById('task-name').value;
	const taskDescription = document.getElementById('task-description').value;
	const taskStatus = document.getElementById('task-status').value;
	const token = getCookie("access_token");

	const completed = taskStatus === "completa" ? true : false

	if (taskName !== "") {

		fetch("http://127.0.0.1:8000/task", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"Authorization": `Bearer ${token}`

			},
			credentials: "include",
			body: JSON.stringify({
				name: String(taskName),
				desc: String(taskDescription),
				completed: completed,

			})
		})
			.then(response => {
				if (!response.ok) {
					throw new Error("Erro na requisição: " + response.statusText);
				}
				return response.json();
			})
			.then(data => console.log(data))
			.catch(error => console.error("Erro:", error));

	}

});


editButton.addEventListener('click', () => {

	const taskId = document.getElementById('edit-task-id').value;
	const taskName = document.getElementById('edit-task-name').value;
	const taskDescription = document.getElementById('edit-task-description').value;
	const taskStatus = document.getElementById('edit-task-status').value;
	const token = getCookie("access_token");

	const completed = taskStatus === "completa" ? true : false

	if (taskName !== "") {

		fetch("http://127.0.0.1:8000/task", {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
				"Authorization": `Bearer ${token}`

			},
			credentials: "include",
			body: JSON.stringify({
				id: String(taskId),
				name: String(taskName),
				desc: String(taskDescription),
				completed: completed,

			})
		})
			.then(response => {
				if (!response.ok) {
					throw new Error("Erro na requisição: " + response.statusText);
				}
				return response.json();
			})
			.then(data => console.log(data))
			.catch(error => console.error("Erro:", error));

	}

});


deleteButton.addEventListener('click', () => {

	const taskId = document.getElementById('edit-task-id').value;
	const taskName = document.getElementById('edit-task-name').value;
	const token = getCookie("access_token");


	if (taskName !== "") {

		fetch(`http://127.0.0.1:8000/task?id=${taskId}`, {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
				"Authorization": `Bearer ${token}`

			},
			credentials: "include"
		})
			.then(response => {
				if (!response.ok) {
					throw new Error("Erro na requisição: " + response.statusText);
				}
				return response.json();
			})
			.then(data => console.log(data))
			.catch(error => console.error("Erro:", error));

	}

});


loginForm.addEventListener('submit', (e) => {
	e.preventDefault();

	const username = document.getElementById('username').value;
	const password = document.getElementById('password').value;

	fetch("http://127.0.0.1:8000/user/login", {
		method: "POST",
		headers: {
			"Content-Type": "application/x-www-form-urlencoded"
		},
		body: `grant_type=password&username=${username}&password=${password}&scope=string&client_id=string&client_secret=string`
	})
		.then(response => {
			if (!response.ok) {
				throw new Error("Erro na requisição: " + response.statusText);
			}
			return response.json();
		})
		.then(data => {

			console.log(data);

			if (data.access_token) {
				const token = data.access_token;

				document.cookie = `access_token=${token}; path=/; secure; SameSite=Strict`;

			}
			window.location.reload()
		})
		.catch(error => {
			console.error("Erro:", error)
			document.getElementById("username").classList.add('is-invalid');
			document.getElementById("password").classList.add('is-invalid');
		});
});

window.onload = () => {
	const token = getCookie("access_token");

	if (!token) {
		document.getElementById("open-task-modal-btn").remove()
		return;
	}
	document.getElementById("create-user-btn").remove()
	document.getElementById("login-btn").remove()
	document.getElementById("login-alert").remove()


	fetch("http://127.0.0.1:8000/task/all", {
		method: "GET",
		headers: {
			"Authorization": `Bearer ${token}`,
			"Content-Type": "application/json"
		},
		credentials: "include"
	})
		.then(response => {
			if (!response.ok) {
				throw new Error("Erro ao buscar tarefas");
			}
			return response.json();
		})
		.then(tasks => {
			const taskList = document.getElementById("todo-list");
			taskList.innerHTML = "";

			tasks.forEach(task => {
				const listItem = document.createElement('li');
				listItem.classList.add('todo-item');
				listItem.innerText = `${task[1]} - ${task[2]} - ${task[4] ? "Completa" : "Incompleta"}`;
				listItem.dataset.id = task[0];


				listItem.addEventListener('click', () => {
					openTaskModal(task);
				});

				taskList.appendChild(listItem);
			});
		})
		.catch(error => console.error("Erro:", error));
};
