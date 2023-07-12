const uploadForm = document.getElementById('upload-form');
const uploadButton = document.getElementById('upload-button');
const fileInput = document.querySelector('input[type="file"]');
const footer = document.querySelector('.footer_section');
const copy = document.querySelector('.copyright_section');
const statusMessage = document.getElementById('status-message');
const loadingSpinner = document.getElementById('loading-spinner');
const bodyElement = document.body;

uploadForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        uploadForm.style.display = 'none';
        loadingSpinner.classList.remove('hidden');
        bodyElement.classList.add('overflow');
        footer.classList.add('hidden')
        copy.classList.add('hidden')
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Error uploading file');
                }
            })
            .then(result => {
                const message = extractMessage(result);
                window.location.href = `/result?message=${encodeURIComponent(message)}`;
            })
            .catch(error => {
                console.error(error);
                statusMessage.innerText = error.message;
                uploadForm.style.display = 'block';
            })
            .finally(() => {
                loadingSpinner.classList.add('hidden');
            });
    }
});

function extractMessage(html) {
    const tempElement = document.createElement('div');
    tempElement.innerHTML = html;

    const titleElement = tempElement.querySelector('h1');
    const headerElement = tempElement.querySelector('h2');
    const messageElement = tempElement.querySelector('p');

    let message = '';
    if (messageElement) {
        message = messageElement.textContent.trim();
    } else {
        const allTextNodes = getAllTextNodes(tempElement);
        message = allTextNodes.join(' ').trim();
    }

    return message;
}

function getAllTextNodes(element) {
    const textNodes = [];

    function traverse(element) {
        const childNodes = element.childNodes;
        for (let i = 0; i < childNodes.length; i++) {
            const node = childNodes[i];
            if (node.nodeType === Node.TEXT_NODE && node.textContent.trim() !== '') {
                textNodes.push(node.textContent.trim());
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                traverse(node);
            }
        }
    }

    traverse(element);

    return textNodes;
}


// upload section 
//selecting all required elements
const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button"),
input = dropArea.querySelector("input");
let file; //this is a global variable and we'll use it inside multiple functions

button.onclick = ()=>{
  input.click(); //if user click on the button then the input also clicked
}

input.addEventListener("change", function(){
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); //calling function
});


//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});

//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});

//If user drop File on DropArea
dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile(); //calling function
});

function showFile() {
  let fileType = file.type; //getting selected file type
  let validExtensions = ["image/jpeg", "image/jpg", "image/png", "video/mp4", "video/x-msvideo", "video/quicktime", "video/x-ms-wmv", "video/x-flv", "video/webm", "video/mpeg"];

  if (validExtensions.includes(fileType)) {
    let fileReader = new FileReader(); //creating new FileReader object
    fileReader.onload = () => {
      let fileURL = fileReader.result; //passing user file source in fileURL variable
      let mediaTag = "";
      if (fileType.startsWith("image/")) {
        // Create an <img> tag if the file is an image
        mediaTag = `<img src="${fileURL}" alt="">`;
      } else if (fileType.startsWith("video/")) {
        // Create a <video> tag if the file is a video
        mediaTag = `<video src="${fileURL}" controls></video>`;
      }
      dropArea.innerHTML = mediaTag; //adding that created media tag inside dropArea container
    };
    fileReader.readAsDataURL(file);
  } else {
    alert("This is not an Image or Video File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}