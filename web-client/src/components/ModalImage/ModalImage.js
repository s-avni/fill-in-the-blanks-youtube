import React, {useState} from "react";
import {Modal, Button, Accordion, Card, Image, Collapse} from "react-bootstrap";

export default class ModalImageButton extends React.Component {
    state = {show: false};

    handleShow = () => {
        this.setState({show: true});
    };

    handleClose = () => {
        this.setState({show: false});
    };

    render() {
        return (
            <>
                <Button variant="primary" onClick={this.handleShow}>
                    Example Output Screenshot
                </Button>

                <Modal show={this.state.show} onHide={this.handleClose}
                       animation={false} centered size="lg">
                    <Modal.Body>
                        <Image src="/Example_Sheet.png"
                               alt="example exercise sheet image"
                               rounded fluid
                        />
                        <br/>
                        <p>Example worksheet:<br/> The first page is the
                            exercise sheet; the second is the solution
                            containing the complete text.
                        </p>
                    </Modal.Body>
                </Modal>
            </>
        );
    }
}

