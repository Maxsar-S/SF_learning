import * as React from "react";
import {createRoot} from "react-dom/client";
import 'bootstrap/dist/css/bootstrap.min.css';

import App from "./components/App";


const rootElement = document.getElementById('root');
const root = createRoot(rootElement);

root.render(
        <App />
);
// import React from "react";
// import { render } from "react-dom":
// import 'bootstrap/dist/css/bootstrap.min.css';
//
// import App from "./components/App";
//
// render(<App/>, document.getElementById("root"));