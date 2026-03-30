let allProjects = [];

fetch('projects.json?v=' + new Date().getTime())
  .then(res => res.json())
  .then(data => {
    allProjects = data;
    render(data);
  });

// Fungsi pembantu untuk memberikan ikon yang relevan berdasarkan nama proyek
function getProjectIcon(projectName) {
  const name = projectName.toLowerCase();
  if (name.includes('bio')) return 'fa-user-circle';
  if (name.includes('music') || name.includes('playlist')) return 'fa-music';
  if (name.includes('font')) return 'fa-font';
  if (name.includes('tool') || name.includes('dev')) return 'fa-tools';
  return 'fa-code'; // Ikon default
}

function render(data) {
  const container = document.getElementById('project-list');
  container.innerHTML = "";

  if (data.length === 0) {
    container.innerHTML = `<div class="no-results"><i class="fas fa-search"></i> Tidak ada proyek yang cocok.</div>`;
    return;
  }

  data.forEach((project, index) => {
    const card = document.createElement('div');
    card.className = 'card';

    const projectIcon = getProjectIcon(project.name);

    card.innerHTML = `
      <div class="card-title">
        <i class="fas ${projectIcon}"></i>
        ${project.name}
      </div>
      <div class="card-desc">${project.description || "-"}</div>

      <div class="card-footer">
        <div class="buttons">
          <a href="${project.source}" target="_blank" class="btn btn-secondary">
            <i class="fab fa-github"></i> Source
          </a>
          <a href="${project.preview}" target="_blank" class="btn btn-primary">
            <i class="fas fa-external-link-alt"></i> Preview
          </a>
        </div>
        <span class="tag">#${index + 1}</span>
      </div>
    `;

    container.appendChild(card);
  });
}

function searchProject() {
  const keyword = document.getElementById("search").value.toLowerCase();

  const filtered = allProjects.filter(p =>
    p.name.toLowerCase().includes(keyword) ||
    (p.description && p.description.toLowerCase().includes(keyword))
  );

  render(filtered);
}