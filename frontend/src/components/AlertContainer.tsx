import React from "react";
import {useAlerts} from "../hooks/use-alerts";
import styles from './AlertContainer.module.css';

export default function AlertContainer() {
  const {alerts, removeAlert} = useAlerts();
  return (
    <div className={styles.container}>
      {alerts.map(alert =>
        <div className={`alert notification is-${alert.category || 'primary'}`}>
          <button className="delete" onClick={() => removeAlert(alert.id)}/>
          <p>{alert.content}</p>
        </div>)}
    </div>
  );
}
