import React from "react";
import OneOnOneList from "./OneOnOnesList";
import OneOnOneDetail from "./OneOnOneDetail";
import {Route, Switch} from "react-router-dom";


export default function OneOnOnesPage() {
  return (
    <div className="container">
      <div className="columns">
        <div className="column is-one-fifth">
          <OneOnOneList/>
        </div>
        <div className="column is-four-fifths">
          <Switch>
            <Route path="/1-on-1s/:id">
              <OneOnOneDetail/>
            </Route>
          </Switch>
        </div>
      </div>
    </div>)
}
