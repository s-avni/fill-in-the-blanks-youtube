import React from "react";

class OptionsForm extends React.Component {
    handleShow = () => {
        this.setState({show: true});
    };

    handleClose = () => {
        this.setState({show: false});
    };

    render() {
        return (
            <>
                <p>TODO: Options Form</p>
            {/*    Language options; skip every N option*/}
            </>);
    }
}

export default OptionsForm;

// todo: https://reactjs.org/docs/forms.html