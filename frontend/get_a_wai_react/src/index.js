import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css'
import "bootstrap/dist/js/bootstrap.bundle.min"
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import Main from './main'
library.add(fas)

//import './index.css';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <Main/>
);
