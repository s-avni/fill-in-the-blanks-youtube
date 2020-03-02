import React from "react";
import {Form, Button, Row, Col} from "react-bootstrap";
import './LinkForm.css';

class LinkForm extends React.Component {
    state = {link: "https://www.youtube.com/watch?v=MKlx1DLa9EA"};

    handleChange = (event) =>  {
        this.setState({link:event.target.value});
    };

    handleSubmit = () => {
        this.props.handleLinkSubmit(this.state.link);
        console.log(this.state.link)
    };

    // https://reactjs.org/docs/forms.html - state must be source of truth
    render() {
        return (
            //todo: is this ok?
            <Form onSubmit={e => {e.preventDefault(); this.handleSubmit()}}>
                <Form.Group controlId="formYTLink">
                    <Form.Control className="text-center" autoFocus={true}
                                  type="text"
                                  placeholder="Enter youtube link"
                                  value={this.state.link}
                                  spellCheck={false}
                                  onChange={this.handleChange}/>
                    <Button variant="primary" type="submit">
                        Submit
                    </Button>
                </Form.Group>
            </Form>);
    }
}

export {LinkForm};







