import React from "react";
import Navbar from "./header/Navbar";
import {Route, Switch} from "react-router-dom";
import FeedPage from "./feed/FeedPage";
import styles from './Snowflake.module.css';

export default function Snowflake() {
  return (
    <>
      <Navbar/>
      <div className={styles.container}>
        <Switch>
          <Route path="/" component={FeedPage}/>
        </Switch>
      </div>
    </>
  )
}
