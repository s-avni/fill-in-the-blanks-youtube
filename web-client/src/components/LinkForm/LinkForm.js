import React from "react";
import {Form, Button, Row, Col} from "react-bootstrap";
import './LinkForm.css';

class LinkForm extends React.Component {
    state = {link: ""};

    handleChange = (event) =>  {
        this.setState({link:event.target.value});
    };


    //You may call setState() immediately in componentDidMount(). It will trigger an extra rendering, but it will happen before the browser updates the screen. This guarantees that even though the render() will be called twice in this case, the user won’t see the intermediate state. Use this pattern with caution because it often causes performance issues. In most cases, you should be able to assign the initial state in the constructor() instead. It can, however, be necessary for cases like modals and tooltips when you need to measure a DOM node before rendering something that depends on its size or position.

    componentDidMount() {
        const link = localStorage.getItem('link') ? localStorage.getItem('link') : "";
        this.setState({ link });
    }

    isASCII = (str) => {
        return /^[\x00-\x7F]*$/.test(str);
    };

    handleSubmit = () => {
        if (this.state.link.trim().length === 0) {
            return;
        }
        else if (!this.isASCII(this.state.link)) {
            this.props.handleLinkError("Please enter English characters only.")
        } else {
            this.props.handleLinkSubmit(this.state.link);
            console.log(this.state.link)
        }
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
                </Form.Group>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>);
    }
}

export {LinkForm};







