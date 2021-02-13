import React from "react";
import {Link} from "react-router-dom";
import TimeAgo from "react-timeago";
import LikeButton from "./LikeButton";
import LikeDetailsButton from "./LikeDetailsButton";
import CommentButton from "./CommentButton";
import Comments from "./Comments";
import {Appreciation as AppreciationType} from "../../lib/api";
import {useToggle} from "../../hooks/use-toggle";

export default function Appreciation(props: AppreciationType) {

  const {id, content, mentions, likeCount, commentCount, viewerLike, createdAt, createdBy} = props;

  const [showComments, toggleShowComments] = useToggle(true);

  return (
    <article className="appreciation media">
      <figure className="media-left is-flex">
        <div className="participants-avatar image is-48x48">
          <img alt={`Avatar of ${createdBy?.name}`}
               title={createdBy?.name}
               className="is-rounded" src={createdBy?.profilePic}/>
        </div>
        <div className="participants-avatar image is-48x48">
          {mentions?.map((mention, index) =>
            <img key={index} alt={`Avatar of ${mention.user.username}`}
                 title={mention.user.name}
                 className="is-rounded" src={mention.user.profilePic}/>
          )}
        </div>
      </figure>
      <div className="media-content">
        <div className="content">
          <div>
            <Link to={`/profile/${createdBy?.username}`}>
              <strong>
                {createdBy?.name}
              </strong>
            </Link>
            <small className="ml-2">
              <TimeAgo date={createdAt}/>
            </small>
          </div>
          <div className="mt-2">
            {/*TODO: Need to add mentions */}
            {content}
          </div>
        </div>
        <nav className="level is-mobile">
          <div className="level-left">
            <div className="level-item">
              <LikeButton like={viewerLike}/>
              <LikeDetailsButton count={likeCount} appreciationId={id}/>
            </div>
            <CommentButton onClick={toggleShowComments} count={commentCount}/>
          </div>
        </nav>
        <Comments appreciationId={id} hidden={showComments}/>
      </div>
    </article>);
}
