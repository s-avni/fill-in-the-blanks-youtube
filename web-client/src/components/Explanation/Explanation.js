import React from "react";
import {Button, Collapse, Card, Image, Modal} from "react-bootstrap";
import {useState} from 'react';
import ModalImageButton from "../ModalImage/ModalImage";

// import './Explanation.css';

class InstructionButton extends React.Component {
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
                    Instructions
                </Button>

                <Modal show={this.state.show} onHide={this.handleClose}
                       animation={false} centered>
                    {/*<Modal.Header closeButton>*/}
                    {/*    <Modal.Title>Modal heading</Modal.Title>*/}
                    {/*</Modal.Header>*/}
                    <Modal.Body>
                        <ol className="text-left" id="instruction-text">
                            <li>Choose the video you want to use for your
                                exercise.
                            </li>
                            <li>Copy video's URL.</li>
                            <li>Paste it above and press continue.</li>
                            <li>Choose the language you want to practice.</li>
                            <li>Download the PDF.</li>
                            <li>While watching the video on YouTube, try to fill
                                in
                                the missing words!
                            </li>
                        </ol>
                    </Modal.Body>
                    {/*<Modal.Footer>*/}
                    {/*</Modal.Footer>*/}
                </Modal>
            </>
        );
    }
}


export const Explanation = () => <>
    <InstructionButton/>
    <ModalImageButton src="/Example_Sheet.png"
                      alt="example exercise sheet image"/>
</>;






