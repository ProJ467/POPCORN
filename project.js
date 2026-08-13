document.addEventListener('DOMContentLoaded', () => {
  const projectList = document.getElementById('project-list');
  if (!projectList) return;

  const sampleProjects = [
    { title: 'Sample Project', owner: 'demo_user', description: 'A short example project description.' },
    { title: 'Another Project', owner: 'creator_2', description: 'A second project used for layout testing.' },
  ];

  projectList.innerHTML = sampleProjects
    .map(
      (project) => `
        <article class="project-item">
          <h3>${project.title}</h3>
          <small>by ${project.owner}</small>
          <p>${project.description}</p>
        </article>
      `
    )
    .join('');
});
