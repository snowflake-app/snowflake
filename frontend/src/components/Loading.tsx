import React from "react";

import styles from './Loading.module.css'
import loader from "../images/loader.svg";

export default function Loading() {
  return (
    <div className="viewport">
      <img src={loader} alt="Loading..." className={styles.loader}/>
    </div>);

}
