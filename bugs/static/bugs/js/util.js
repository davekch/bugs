function update_statusbutton(projectname, issueid, status) {
	const statusstyles = {
		"Pending": "btn-danger",
		"Wip": "btn-warning",
		"Done": "btn-success",
		"Wontfix": "btn-secondary"
	};
	var button = document.getElementById(`status-dropdown-menu-${issueid}`);
	var dropdown = document.getElementById(`status-dropdown-items-${issueid}`);
	// remove dropdown items
	while (dropdown.hasChildNodes()) {
		dropdown.removeChild(dropdown.lastChild);
	}
	// remove current style and add updated dropdown items
	for (const [stat, style] of Object.entries(statusstyles)) {
		button.classList.remove(style);
		if (status !== stat) {
			let item = document.createElement('a');
			item.classList.add("dropdown-item");
			item.onclick = function() { set_status(projectname, issueid, stat); };
			item.innerHTML = stat;
			dropdown.appendChild(item);
		}
	}
	// set new style
	button.classList.add(statusstyles[status]);
	button.innerHTML = status;
}

function set_status(projectname, issueid, status) {
	$.ajax({
		url: `/bugs/api/${projectname}/issues/${issueid}/`,
		type: 'PUT',
		data: {
			status: status
		},
		success: function(data) {
			update_statusbutton(projectname, issueid, status);
		}
	})
}
