import {Link, useParams} from "react-router-dom";
import React, {useCallback} from "react";
import {oneOnOneById} from "../../lib/api";
import {useAsync} from "../../hooks/use-async";
import {useAuth} from "../../hooks/use-auth";
import Loading from "../Loading";
import {isCreatedByUser} from "../../lib/utils";
import ScheduleMeetingButton from "./ScheduleMeetingButton";

type OneOnOneDetailRouterParams = {
  id: string
}

export default function OneOnOneDetail() {
  const {id} = useParams<OneOnOneDetailRouterParams>();
  const loadOneOnOneById = useCallback(() => oneOnOneById(id), [id]);
  const {value: oneOnOne, status} = useAsync(loadOneOnOneById);
  const {user} = useAuth();

  return (
    <div className="container p-6">
      {status === "pending" && <Loading/>}
      {oneOnOne && (
        <article className="appreciation media">
          <figure className="media-left is-flex">
            <div className="participants-avatar image is-48x48">
              <img alt={oneOnOne.createdBy.name} className="is-rounded"
                   src={oneOnOne.createdBy.profilePic}/>
            </div>
            <div className="participants-avatar image is-48x48">
              <img alt={oneOnOne.user.name} className="is-rounded"
                   src={oneOnOne.user.profilePic}/>
            </div>
          </figure>
          <div className="media-content">
            <div className="content">
              <div className="block is-flex">
                <h1 className="title is-flex-grow-1">
                  {isCreatedByUser(oneOnOne, user) ?
                    `Your 1:1 with ${oneOnOne.user.name}` :
                    `${oneOnOne.createdBy.name}}'s 1:1 with you`}
                </h1>
                <ScheduleMeetingButton
                  title={`${oneOnOne.createdBy.name} 1:1 with ${oneOnOne.user.name}`}/>
              </div>
              <div className="block">
                <h3>Action items</h3>
                <ul className="action-items">
                  {oneOnOne.actionItems.map(actionItem => (
                    <li key={actionItem.id} className="block is-flex align-items-center">
                      <button className="clear-button mr-1 is-clickable">
                        {actionItem.state ? (
                          <span className="icon has-text-success">
                            <ion-icon size="large" name="checkmark-circle"/>
                          </span>
                        ) : (
                          <span className="icon">
                            <ion-icon size="large" name="checkmark-circle-outline"/>
                          </span>
                        )}
                      </button>
                      <span className="image is-24x24 mx-1">
                      <img alt={`Created by ${actionItem.createdBy.name}`} className="is-rounded"
                           src={actionItem.createdBy.profilePic}/>
                    </span>
                      <Link className="mr-1" to={`/profile/${actionItem.createdBy.username}`}>
                        {actionItem.createdBy.name}
                      </Link>
                      <span>
                      {actionItem.content}
                        {/*TODO: add_mentions */}
                    </span>
                    </li>
                  ))}
                </ul>
                <form className="block field">
                  <div className="control has-icons-left">
                    <input className="input" type="text" placeholder="Add action item..."/>
                    <span className="icon is-left">
                      <ion-icon name="add-circle-outline"/>
                    </span>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </article>)}
    </div>);
}
