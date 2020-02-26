import React from "react";
import {Form, Button, Row, Col} from "react-bootstrap";
import './YTForm.css';


export const YTForm = () =>
    <Form>
        <Form.Group controlId="formYTLink">
            {/*<Form.Label>Youtube link</Form.Label>*/}
            <Form.Control className="text-center" autoFocus={true} type="text"
                          placeholder="Enter youtube link" value="https://www.youtube.com/watch?v=MKlx1DLa9EA" spellCheck={false}/>
            <Form.Text className="text-muted">
                {/*We'll never share your email with anyone else.*/}
            </Form.Text>
        </Form.Group>

        <Button variant="primary" type="submit">
            Submit
        </Button>
    </Form>





