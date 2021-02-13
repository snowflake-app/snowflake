import React from "react";

export default function MostAppreciatedUsers() {
  return (
    <div className="panel is-primary block">
      <p className="panel-heading has-text-centered">
        Most appreciated
      </p>
      {/*{% for entry in most_appreciated %}*/}
      <a href="/profile/{{entry.user.username}}" className="panel-block p-3 is-active is-align-items-center">
        <figure className="image is-24x24 mr-1">
          <img alt="{{ entry.user.name }}"
               title="{{ entry.user.name }}" className="is-rounded" src="{{entry.user.profile_pic}}"/>
        </figure>
        <span>
                  {/*{{entry.user.name}}*/}
                </span>
        <span className="is-flex-grow-1"/>
        <span className="has-text-weight-bold">
                  {/*{{entry.count}}*/}
                </span>
      </a>
      {/*{% endfor %}*/}
    </div>);
}
