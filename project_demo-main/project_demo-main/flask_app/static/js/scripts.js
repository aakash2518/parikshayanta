document.getElementById('question_paper').addEventListener('change', function(event) {
    let file = event.target.files[0];
    if (file) {
        document.getElementById('qp-name').innerText = "📄 " + file.name;
    }
});

document.getElementById('answer_sheets').addEventListener('change', function(event) {
    let files = event.target.files;
    let fileList = document.getElementById('as-names');
    fileList.innerHTML = "";  

    for (let i = 0; i < files.length; i++) {
        let li = document.createElement('li');
        li.innerText = "📝 " + files[i].name;

        let removeBtn = document.createElement('span');
        removeBtn.innerHTML = " ❌";
        removeBtn.classList.add("remove-file");
        removeBtn.onclick = function() {
            li.remove();
        };

        li.appendChild(removeBtn);
        fileList.appendChild(li);
    }
});

function uploadFiles() {
    document.getElementById("uploading-animation").style.display = "block";

    setTimeout(() => {
        document.getElementById("uploading-animation").style.display = "none";
        document.getElementById("upload-success").style.display = "block";
    }, 2000);
}

function closePopup() {
    document.getElementById("upload-success").style.display = "none";
}

function startProcessing() {
    document.getElementById("progress").style.display = "block";
    document.getElementById("loading-animation").style.display = "block";

    setTimeout(() => {
        document.getElementById("progress").style.display = "none";
        document.getElementById("loading-animation").style.display = "none";
        alert("OCR & Evaluation completed!");
    }, 3000);
}
