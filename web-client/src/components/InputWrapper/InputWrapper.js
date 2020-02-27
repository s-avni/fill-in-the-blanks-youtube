import React from "react";
import {LinkForm} from "../LinkForm/LinkForm";
import OptionsForm from "../OptionsForm/OptionsForm";

class InputWrapper extends React.Component {
    state = {showLanguageOptions: false,
             error: null
            };

    handleLinkSubmit = (link) => {
        console.log("HELLLO");
        fetch('/check-link', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({"link" : link}),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('Success:', data);
            })
            .catch((error) => {
                this.setState({error});
                console.error('Error:', error);
            });
    };

    handleClose = () => {
        this.setState({show: false});
    };

    render() {
        return (
            <>
                <LinkForm handleLinkSubmit={this.handleLinkSubmit}/>
                {/*{ this.state.error &&*/}
                {/*<h3 className="error"> { this.state.error } </h3> }*/}
                <OptionsForm/></>);

    }
}

export {InputWrapper};