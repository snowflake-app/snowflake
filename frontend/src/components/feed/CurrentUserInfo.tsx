import {useAuth} from "../../hooks/use-auth";
import {Link} from "react-router-dom";
import React from "react";

export default function CurrentUserInfo() {
  const auth = useAuth();
  const {name, profilePic: avatar, username, designation, teamName} = auth.user!;

  return (
    <div className="box block">
      <div className="header pb-0 p-4 has-text-centered">
        <figure className="avatar m-auto image mb-3 is-128x128">
          <img alt={name}
               title={name} className="is-rounded" src={avatar}/>
        </figure>
        <h1 className="is-size-4">
          <Link to={`/profile/${username}`}>
            {name}
          </Link>
        </h1>
        <p>
          {designation} @ {teamName}
        </p>
      </div>
      <hr/>
      <div className="block summary pt-0 p-4 is-flex is-justify-content-space-around">
        <div className="is-flex is-flex-direction-column is-align-items-center">
                    <span className="given-count has-text-weight-bold is-size-4">
                      {/*{{appreciations_given}}*/}
                    </span>
          <span className="is-uppercase">Given</span>
        </div>
        <div className="is-flex is-flex-direction-column is-align-items-center">
                    <span className="received-count has-text-weight-bold is-size-4">
                      {/*{{appreciations_received}}*/}
                    </span>
          <span className="is-uppercase">Received</span>
        </div>
      </div>
    </div>);
}
