import React from "react";
import {Button, Form} from "react-bootstrap";

class OptionsForm extends React.Component {
    state = {n: 3, lang: null};

    handleNChange = (event) => {
        this.setState({n: event.target.value});
    };

    handleLangChange = (event) => {
        this.setState({lang: event.target.value});
    };

    handleSubmit = () => {
        const lang = this.state.lang ? this.state.lang : this.props.languageOptions[0];
        this.props.handleOptionsSubmit(this.state.n, lang);
    };

    render() {
        if (!this.props.languageOptions) {
            return null;
        }
        const numbers = [3, 4, 5, 6, 7, 8, 9, 10];
        let langs = [...this.props.languageOptions];
        langs.sort();
        return (this.props.show &&
            <Form onSubmit={e => {
                e.preventDefault();
                this.handleSubmit()
            }}>
                <Form.Group>
                    <Form.Label>Skip every n</Form.Label>
                    <Form.Control as="select" value={this.state.n}
                                  onChange={this.handleNChange}>
                        {numbers.map((num) => <option key={num}
                                                      value={num}>{num}</option>)}
                    </Form.Control>
                </Form.Group>
                <Form.Group>
                    <Form.Label>Select language</Form.Label>
                    <Form.Control as="select"
                                  defaultValue={this.props.languageOptions[0]}
                                  onChange={this.handleLangChange}>
                        {langs.map((language) => <option key={language}
                                                         value={language}>{language}</option>)}
                    </Form.Control>
                </Form.Group>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        );
    }
}

export default OptionsForm;

// todo: https://reactjs.org/docs/forms.html