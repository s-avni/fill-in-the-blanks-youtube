import React from 'react';
import logo from './logo.svg';
import './App.css';

import 'bootstrap/dist/css/bootstrap.min.css';
import { PageHeader } from './components/PageHeader/PageHeader';
import {InputWrapper} from "./components/InputWrapper/InputWrapper";

function App() {
  return (
    <div className="App">
      <PageHeader/>
        <div className="container">
            <div className="row align-items-center">
                <div className="col col-md-6 offset-md-3">
                    <InputWrapper/>
                </div>
            </div>
        </div>
    </div>
  );
}

export default App;
