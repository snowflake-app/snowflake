import React, {useCallback} from "react";
import {Link, Route, Switch, useParams, useRouteMatch} from "react-router-dom";
import UserInfo from "../UserInfo";
import {useAsync} from "../../hooks/use-async";
import {userByUsername} from "../../lib/api";
import Loading from "../Loading";
import styles from './ProfilePage.module.css';

type ProfilePageRouteParams = {
  username: string
}

type TabItemProps = React.ComponentPropsWithoutRef<any> & {
  path: string
}

function TabItem({path, children}: TabItemProps) {
  const match = useRouteMatch(path);

  const classes = [];

  if (match && match.path === path && match.isExact) {
    classes.push('is-active')
  }

  return (
    <li className={classes.join(' ')}>{children}</li>
  )
}

export default function ProfilePage() {
  const {username} = useParams<ProfilePageRouteParams>();

  const loadUserInfo = useCallback(() => userByUsername(username), [username]);
  const {value: user, status} = useAsync(loadUserInfo);

  const {path, url} = useRouteMatch();

  return (
    <div className={`container ${styles.container}`}>
      {status === "pending" && <Loading/>}
      {user && <UserInfo {...user} />}
      {status === "success" && (
        <div className="box">
          <Switch>
            <div className="tabs is-fullwidth is-medium">
              <ul>
                <TabItem path={path}>
                  <Link to={url}>
                    <span className="icon">
                        <ion-icon name="information-circle-outline"/>
                    </span>
                    <span>About</span>
                  </Link>
                </TabItem>
                <TabItem path={`${path}/mentions`}>
                  <Link to={`${url}/mentions`}>
                    <span className="icon is-medium">
                        <ion-icon name="at-outline"/>
                    </span>
                    <span>Mentions</span>
                  </Link>
                </TabItem>
                <TabItem path={`${path}/personal-objectives`}>
                  <Link to={`${url}/personal-objectives`}>
                    <span className="icon is-medium">
                        <ion-icon name="rocket-outline"/>
                    </span>
                    <span>Personal Objectives</span>
                  </Link>
                </TabItem>
              </ul>
            </div>
            <Route path={path}/>
            <Route path={`${path}/mentions`}/>
            <Route path={`${path}/personal-objectives`}/>
          </Switch>
        </div>)}
    </div>
  );
}
