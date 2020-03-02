import React from "react";
import {LinkForm} from "../LinkForm/LinkForm";
import OptionsForm from "../OptionsForm/OptionsForm";

class InputWrapper extends React.Component {
    state = {
        showLanguageOptions: false,
        error: null,
        video_id: null,
        url: null,
        languageOptions: null
    };

    showFile = (blob) => {
        // It is necessary to create a new blob object with mime-type explicitly set
        // otherwise only Chrome works like it should
        const newBlob = new Blob([blob], {type: "application/pdf"});

        // IE doesn't allow using a blob object directly as link href
        // instead it is necessary to use msSaveOrOpenBlob
        if (window.navigator && window.navigator.msSaveOrOpenBlob) {
            window.navigator.msSaveOrOpenBlob(newBlob);
            return;
        }

        // For other browsers:
        // Create a link pointing to the ObjectURL containing the blob.
        const data = window.URL.createObjectURL(newBlob);
        const link = document.createElement('a');
        link.href = data;
        link.download="Worksheet.pdf";
        link.click();
        setTimeout(function(){
            // For Firefox it is necessary to delay revoking the ObjectURL
            window.URL.revokeObjectURL(data);
        }, 100);
    };

    handleOptionsSubmit = (n, lang) => {
        //https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
        fetch('/get-document', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "video_id": this.state.video_id,
                "n": n,
                "lang": lang,
                "url": this.state.url
            }),
        }).then(response => response.blob())
            .then(this.showFile)
            .catch((error) => {
                this.setState({error: error, showLanguageOptions: false});
                console.error('Error:', error);
            });
    };

    submitValidLink = () => fetch('/check-video-id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"video_id": this.state.video_id}),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            this.setState({
                showLanguageOptions: true,
                languageOptions: data.langs
            })
        })
        .catch((error) => {
            this.setState({error: error, showLanguageOptions: false});
            console.error('Error:', error);
        });

    handleLinkSubmit = (url) => {
        //https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
        const regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        const match = url.match(regExp);
        if (match && match[2].length === 11) {
            console.log(match[2]);
            this.setState({video_id: match[2], url: url, error: null}, this.submitValidLink);
        } else {
            this.setState({
                error: "Invalid url :(",
                showLanguageOptions: false
            });
            console.log(this.state.error);
        }

    };

    // handleClose = () => {
    //     this.setState({show: false});
    // };

    render() {
        return (
            <>
                <LinkForm handleLinkSubmit={this.handleLinkSubmit}/>
                { this.state.error &&
                <p className="error"> { this.state.error } </p> }
                <OptionsForm show={this.state.showLanguageOptions}
                             languageOptions={this.state.languageOptions}
                             handleOptionsSubmit={this.handleOptionsSubmit}
                />
            </>);

    }
}

export {InputWrapper};