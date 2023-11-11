// Get search form and PAGE links
let searchForm = document.getElementById("searchForm");
let pageLinks = document.getElementsByClassName("page-link");

// Ensure search form exist
if (searchForm) {
  for (let index = 0; pageLinks.length > index; index++) {
    pageLinks[index].addEventListener("click", function (event) {
      event.preventDefault();
      console.log("Button clicked");
      // Get the data atrr
      let page = this.dataset.page;

      if (page) {
        searchForm.innerHTML += `<input value=${page} name = "page" hidden />`;
        searchForm.submit();
      }
    });
  }
}

let tags = document.getElementsByClassName("project-tag");
for (let i = 0; tags.length > i; i++) {
  tags[i].addEventListener("click", (e) => {
    let tagId = e.target.dataset.tag;
    let projectId = e.target.dataset.project;
    let url = `http://127.0.0.1:8000/api/projects/${projectId}/remove/tag`;
    fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ tag: tagId }),
    })
      .then((response) => response.json())
      .then((data) => {
        e.target.remove();
      });
  });
}
