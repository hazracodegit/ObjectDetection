const form = document.getElementById("uploadForm");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const file =
        document.getElementById("imageInput").files[0];

    const formData = new FormData();

    formData.append("image", file);

    const response = await fetch("/detect", {

        method: "POST",
        body: formData

    });

    const data = await response.json();

    document.getElementById("resultImage").src =
        data.image;

    let html =
        `<h3>Objects Found (${data.count})</h3>`;

    data.objects.forEach(obj => {

        html += `
        <div>
            ${obj.name}
            (${obj.confidence}%)
        </div>
        `;

    });

    document.getElementById("objects").innerHTML =
        html;
});

function toggleTheme() {

    document.body.classList.toggle("light");

}