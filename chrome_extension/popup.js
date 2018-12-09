const FILLINDBLANKS = "https://fillindblanks.herokuapp.com";

const getCaptionOptions = async () => {
    let captionOptions;

    const yt_link_input = document.getElementById("yt_link");
    const yt_link = yt_link_input.value;
    if (!yt_link) {
        return [];
    }

    const loadingMsg = document.createElement("span");
    loadingMsg.innerText = "Loading captions..."
    yt_link_input.insertAdjacentElement("beforebegin", loadingMsg);
    yt_link_input.disabled = true;

    try {
        const captionResponse = await fetch(`${FILLINDBLANKS}/get_available_captions`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ yt_link })
        });

        captionOptions = await captionResponse.json();
    } finally {
        yt_link_input.disabled = false;
        loadingMsg.remove();
    }
    return captionOptions.captions;
}

const clearChildren = (el) => {
    while (el.firstChild) {
        el.removeChild(el.firstChild);
    }
}

const toggleShowCaptionsFields = (show) => {
    const captionFields = document.getElementsByClassName("captionsFields");
    for (let i = 0; i < captionFields.length; i++) {
        captionFields[i].style=`display: ${show ? 'grid' : 'none'};`;
    }
}

const handleError = (errorText) => {
    const errors = document.getElementById("errors");
    clearChildren(errors);

    toggleShowCaptionsFields(false);
    const error = document.createElement("span");
    error.innerText = errorText.toString();
    errors.appendChild(error);
}

const addCaptionOptions = async () => {
    try {
        const captions = await getCaptionOptions();

        const captionSelect = document.getElementById("captions");
        clearChildren(captionSelect);

        if (!captions || captions.length <= 0) {
            handleError("Oh no! Please submit a video with (non automatic) captions.");
        } else {
            const errors = document.getElementById("errors");
            clearChildren(errors);
            toggleShowCaptionsFields(true);
            //Create and append the options
            for (let i = 0; i < captions.length; i++) {
                const caption = captions[i];
                if (!caption || caption.length != 2) {
                    clearChildren(captionSelect);
                    handleError("Error in caption response.");
                    break;
                }
                const option = document.createElement("option");
                option.text = caption[0];
                option.value = caption[1];
                captionSelect.appendChild(option);
            }
        }
    } catch (err) {
        handleError(err);
        throw err;
    }
}


document.getElementById("addCaptionOptions").addEventListener('click', addCaptionOptions);


// const getWorksheet = async () => {
//     const formData = new FormData(document.getElementById("form"));
//     console.log("formData", formData);
//     const captionResponse = await fetch(`${FILLINDBLANKS}/get_worksheet`, {
//         body: formData,
//         headers: {
//             "Content-Type": "multipart/form-data",
//             'Accept': 'application/json'
//         },
//         method: "post",
//     });
//     return captionResponse;
// }

document.getElementById("submit").addEventListener('click', () => alert("Preparing the worksheet (this may take a few seconds)..."));
