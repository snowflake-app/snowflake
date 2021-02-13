import React from "react";
import {User} from "../lib/auth";
import {Link} from "react-router-dom";

export default function UserInfo(props: User) {
  const {name, profilePic, username, designation, teamName} = props;
  return (
    <div className="box block">
      <div className="header pb-0 p-4 has-text-centered">
        <figure className="avatar m-auto image mb-3 is-128x128">
          <img alt={name}
               title={name} className="is-rounded" src={profilePic}/>
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
