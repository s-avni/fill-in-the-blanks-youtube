import React from 'react';
import logo from './logo.svg';
import './App.css';

import 'bootstrap/dist/css/bootstrap.min.css';
import { PageHeader } from './components/PageHeader/PageHeader';
import {YTForm} from "./components/YTForm/YTForm";
import {Explanation} from "./components/Explanation/Explanation";

function App() {
  return (
    <div className="App">
      <PageHeader/>
        <div className="container">
            <div className="row align-items-center">
                <div className="col col-md-6 offset-md-3">
                    <YTForm/>
                </div>
            </div>
        </div>
    </div>
  );
}

export default App;
