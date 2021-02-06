import React from "react";
import {useAsync} from "../../hooks/use-async";
import {appreciationLikes} from "../../lib/api";
import Loading from "../Loading";
import {useEventListener} from "../../hooks/use-event-listener";

type LikesProps = { appreciationId: number, onCloseRequested: () => void };

export default function Likes({appreciationId, onCloseRequested}: LikesProps) {

  useEventListener('keyup', event => {
    const {key} = event as KeyboardEvent;
    if (key === 'Escape' || key === 'Esc') {
      onCloseRequested();
    }
  });

  const {value: likes, status} = useAsync(() => appreciationLikes(appreciationId));

  return (
    <div className="modal">
      <div className=" modal-background"/>
      <div className=" modal-content">
        <div className=" box">
          <h2 className=" is-size-4">Likes</h2>
          {status === "pending" && <Loading/>}
          {status === "success" && (
            <div className=" menu mt-4">
              <ul className=" menu-list">
                {likes?.map(like => (
                  <li className=" is-flex pb-2">
                    <figure className=" media-left is-flex">
                      <div className=" participants-avatar image is-48x48">
                        <img alt=" Avatar of {{like.user.name}}"
                             title="{{like.user.name}}"
                             className=" is-rounded"
                             src={like.user.profilePic}/>
                      </div>
                    </figure>
                    <div className=" content">
                      <h3 className=" is-size-5 has-font-weight-bold mb-0">{like.user.name}</h3>
                      <p className=" help">{like.user.designation}</p>
                    </div>
                  </li>))}
                {likes?.length === 0 && (
                  <li className=" is-flex pb-2">
                    <div className=" content">
                      <h3 className=" is-size-5 mb-0 text-center">
                        No likes yet
                      </h3>
                    </div>
                  </li>)}
              </ul>
            </div>)}
        </div>
      </div>
      <button className="modal-close is-large" onClick={onCloseRequested}/>
    </div>
  )
}
