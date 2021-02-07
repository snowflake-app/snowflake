import React from "react";
import Navbar from "./header/Navbar";
import {Redirect, Route, Switch} from "react-router-dom";
import FeedPage from "./feed/FeedPage";
import styles from './Snowflake.module.css';
import OneOnOnesPage from "./one-on-ones/OneOnOnesPage";
import ProfilePage from "./profile/ProfilePage";

export default function Snowflake() {
  return (
    <>
      <Navbar/>
      <div className={styles.container}>
        <Switch>
          <Route path="/" exact={true}>
            <Redirect to="/feed"/>
          </Route>
          <Route path="/feed" component={FeedPage}/>
          <Route path="/1-on-1s" component={OneOnOnesPage}/>
          <Route path="/profile/:username" component={ProfilePage}/>
        </Switch>
      </div>
    </>
  )
}
