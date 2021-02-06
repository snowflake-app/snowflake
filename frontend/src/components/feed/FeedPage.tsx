import React from "react";
import AppreciationForm from "./AppreciationForm";
import CurrentUserInfo from "./CurrentUserInfo";
import MostAppreciatedUsers from "./MostAppreciatedUsers";
import styles from './FeedPage.module.css';
import {Appreciations} from "./Appreciations";

export default function FeedPage() {
  return (
    <div className="container">
      <div className="columns">
        <div className="column is-two-thirds">
          <div className="box">
            <AppreciationForm/>
            <hr/>
            <Appreciations/>
          </div>
        </div>
        <div className="column is-one-third">
          <div className={styles.rightSidebar}>
            <CurrentUserInfo/>
            <MostAppreciatedUsers/>
          </div>
        </div>
      </div>
    </div>
  );
}
