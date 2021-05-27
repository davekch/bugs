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

function make_status_dropdown(issueid, status) {
	var dropdown = document.createElement('div');
	dropdown.className = 'dropdown';
	var btn = document.createElement('button');
	btn.className = 'btn btn-sm dropdown-toggle';
	btn.type = 'button';
	btn.id = `status-dropdown-menu-${issueid}`;
	btn.data_toggle = 'dropdown';
	btn.innerHTML = status;
	dropdown.appendChild(btn);
	var dropdownitems = document.createElement('div');
	dropdownitems.className = 'dropdown-menu';
	dropdownitems.id = `status-dropdown-items-${issueid}`;
	dropdown.append(dropdownitems);
	return dropdown;
}

function sort_issues_by_prioriry(tablebody) {
	$(tablebody).find('tr').sort(function (a, b) {
		return $('td:nth-child(2)', b).text().localeCompare($('td:nth-child(2)', a).text());
	}).appendTo(tablebody);
}

function create_tag_badges(tagstring) {
	var tags = tagstring.split(',');
	var badges = [];
	for (let i=0; i<tags.length; i++) {
		let span = document.createElement('span');
		span.className = 'badge badge-info';
		span.innerHTML = tags[i];
		badges.push(span);
	}
	return badges;
}
