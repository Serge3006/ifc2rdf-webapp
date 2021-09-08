let selectDomainElem = document.getElementById("domain");
let inputFileElem = document.getElementById("file");
let convertBtnElem = document.getElementById("convert");
let messageElem = document.getElementById("success");

let response = null;
let fileLoaded = false;


function sendFile(file){
    var uri = "http://192.168.1.192:5000/";
    var xhr = new XMLHttpRequest();
    var fd = new FormData();

    xhr.open("POST", uri);

    xhr.onreadystatechange = function(e){
        e.preventDefault();
        if(this.readyState == XMLHttpRequest.DONE && this.status == 200){
            response = xhr.responseText;
            messageElem.style.display = "block";
            inputFileElem.value = null;
        }
    }
    console.log(file)
    fd.append("data", file);
    xhr.send(fd);
}


inputFileElem.addEventListener("change", handleFiles);

function handleFiles(e){
    e.preventDefault();
    console.log("File(s) selected");
    file = this.files[0];
    fileLoaded = true;
}

inputFileElem.addEventListener("click", ()=>{
    inputFileElem.value = null;
    messageElem.style.display = "none";
})

convertBtnElem.addEventListener("click", function(e){
    e.preventDefault();
    let domain = selectDomainElem.options[selectDomainElem.selectedIndex].text;
    if (fileLoaded){
        sendFile(file);
        fileLoaded = false;
    } else{
        console.log("File not uploaded");
    }
})