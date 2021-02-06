import {Link} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {notificationCount} from "../../lib/api";
import styles from './Notifications.module.css';

export function Notifications() {
  const [count, setCount] = useState(0);

  const loadCount = async () => {
    setCount(await notificationCount())
  };

  useEffect(() => {
    (async () => await loadCount())();
    const intervalId = setInterval(async () => await loadCount(), 30000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <Link to="/" className="navbar-item tagged">
      <div className={styles.tagged}>
        {count > 0 && <span className={`${styles.count} tag is-small is-primary is-rounded`}>{count}</span>}
        <span className="icon is-medium">
          <ion-icon class="is-size-4" name="notifications-outline"/>
        </span>
      </div>
    </Link>);
}
