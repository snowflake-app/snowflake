import {useAsync} from "../../hooks/use-async";
import {oneOnOnes} from "../../lib/api";
import {useAuth} from "../../hooks/use-auth";
import Loading from "../Loading";
import {isCreatedByUser} from "../../lib/utils";
import React from "react";
import { Link } from "react-router-dom";

export default function OneOnOneList() {

    const {value: oneOnOneList, status} = useAsync(oneOnOnes);
    const {user} = useAuth();

    return (
        <div className="menu">
            <p className="menu-label is-flex">
                <span className="is-flex-grow-1 is-size-6">People</span>
                <button title="Schedule new" id="launch-one-on-one-form" className="clear-button">
        <span className="icon is-medium">
            <ion-icon class="is-size-4" name="add-circle-outline"/>
        </span>
                </button>
            </p>
            {status === "pending" && <Loading/>}
            <ul className="menu-list">
                {oneOnOneList?.map(oneOnOne => (
                    <li key={oneOnOne.id} >
                        <Link className="is-flex" to={`/1-on-1s/${(oneOnOne.id)}`}>
                            <figure className="media-left is-flex">
                                <div className="participants-avatar image is-48x48">
                                    <img alt="Avatar of {{ o.created_by.name }}"
                                         title={oneOnOne.createdBy.name}
                                         className="is-rounded" src={oneOnOne.createdBy.profilePic}/>
                                </div>
                                <div className="participants-avatar image is-48x48">
                                    <img alt="Avatar of {{ o.user.name }}"
                                         title={oneOnOne.user.name}
                                         className="is-rounded" src={oneOnOne.user.profilePic}/>
                                </div>
                            </figure>
                            <div className="content">
                                <h3 className="is-size-5 has-font-weight-bold">
                                    {isCreatedByUser(oneOnOne, user) ? oneOnOne.user.name : oneOnOne.createdBy.name}
                                </h3>
                                <p className="help">
                                    {isCreatedByUser(oneOnOne, user) ? oneOnOne.user.designation : oneOnOne.createdBy.designation}
                                </p>
                            </div>
                        </Link>
                    </li>
                ))}
            </ul>
        </div>);
}
