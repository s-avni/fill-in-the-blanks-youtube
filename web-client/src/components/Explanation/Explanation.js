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

// function InstructionListCollapsable() {
//     const [open, setOpen] = useState(false);
//
//     return (
//         <>
//             <Button
//                 onClick={() => setOpen(!open)}
//                 aria-controls="instruction-text"
//                 aria-expanded={open}
//             >
//                 Instructions
//             </Button>
//             <Collapse in={open}>
//                 <ol className="text-left" id="instruction-text">
//                     <li>Choose the video you want to use for your
//                         exercise.
//                     </li>
//                     <li>Copy video's URL.</li>
//                     <li>Paste it above and press continue.</li>
//                     <li>Choose the language you want to practice.</li>
//                     <li>Download the PDF.</li>
//                     <li>While watching the video on YouTube, try to fill in
//                         the missing words!
//                     </li>
//                 </ol>
//             </Collapse>
//         </>
//     );
// }

export const Explanation = () => <>
    <InstructionButton/>
    <ModalImageButton src="/Example_Sheet.png"
                      alt="example exercise sheet image"/>

    {/*<Accordion defaultActiveKey="">*/}
    {/*    <Card>*/}
    {/*        <Accordion.Toggle as={Card.Header}*/}
    {/*                          className="btn btn-primary accordion-toggle"*/}
    {/*                          variant="link" eventKey="0">*/}
    {/*            Instructions*/}
    {/*        </Accordion.Toggle>*/}
    {/*        <Accordion.Collapse className="btn btn-primary" eventKey="0">*/}
    {/*            <Card.Body>*/}
    {/*                <ol className="text-left">*/}
    {/*                    <li>Choose the video you want to use for your*/}
    {/*                        exercise.*/}
    {/*                    </li>*/}
    {/*                    <li>Copy video's URL.</li>*/}
    {/*                    <li>Paste it above and press continue.</li>*/}
    {/*                    <li>Choose the language you want to practice.</li>*/}
    {/*                    <li>Download the PDF.</li>*/}
    {/*                    <li>While watching the video on YouTube, try to fill in*/}
    {/*                        the missing words!*/}
    {/*                    </li>*/}
    {/*                </ol>*/}
    {/*            </Card.Body>*/}
    {/*        </Accordion.Collapse>*/}
    {/*    </Card>*/}
    {/*    <Card>*/}
    {/*        <Accordion.Toggle as={Card.Header} className="accordion-toggle"*/}
    {/*                          variant="link" eventKey="1"*/}
    {/*                          onClick={console.log("clicked")}>*/}
    {/*            Example Output Screenshot*/}
    {/*        </Accordion.Toggle>*/}
    {/*    </Card>*/}
    {/*<Card>*/}
    {/*    <Accordion.Toggle as={Card.Header} className="accordion-toggle"*/}
    {/*                      variant="link" eventKey="1">*/}
    {/*        Example Output*/}
    {/*    </Accordion.Toggle>*/}
    {/*    <Accordion.Collapse eventKey="1">*/}
    {/*        <Card.Body>*/}
    {/*            <ModalImage src="/Example_Sheet.png" alt="example exercise sheet image"></ModalImage>*/}
    {/*            /!*todo: moshe - not hardcoded sizes*!/*/}
    {/*            /!*<Image src="/Example_Sheet.png" rounded width={500} height={300} mode='fit'*!/*/}
    {/*            /!*       alt="example exercise sheet image"*!/*/}
    {/*            /!*       onClick={}/>*!/*/}
    {/*            <div className="caption text-center">*/}
    {/*                <p><i>*/}
    {/*                    <small>example worksheet: the first page is an*/}
    {/*                        exercise sheet; the second is the*/}
    {/*                        solution.*/}
    {/*                    </small>*/}
    {/*                </i></p>*/}
    {/*            </div>*/}
    {/*        </Card.Body>*/}
    {/*    </Accordion.Collapse>*/}
    {/*</Card>*/}
    {/*</Accordion>*/}
</>;







