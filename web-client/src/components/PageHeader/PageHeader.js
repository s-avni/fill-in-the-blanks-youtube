import React from "react";
import {Jumbotron, Container, Button} from "react-bootstrap";
import './PageHeader.css';
import {Explanation} from "../Explanation/Explanation";


export const PageHeader = () => <Jumbotron fluid>
    <div className="upper-left-corner">
    <Explanation/>
    </div>
    <Container>
        <h1>fill in the blanks YouTube generator</h1>
        <p className="lead">This website offers a uniquely easy way to practice a new
            language.</p>
        <p>Generate a
            <span className="color-1"> fill-in the-blank worksheet </span>
            from a
            <span className="color-2"> YouTube video </span>
            of your
            choosing. <br/>
            Then, practice your listening comprehension skills by filling in the missing words while watching the video.
        </p>
        <p className="small">*The website does not yet support right-to-left languages :(</p>
    </Container>
</Jumbotron>



