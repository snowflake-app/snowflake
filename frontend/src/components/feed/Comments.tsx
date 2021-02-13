import React, {useEffect, useState} from "react";
import {appreciationComments, Comment} from "../../lib/api";
import TimeAgo from "react-timeago";
import {Link} from "react-router-dom";
import Loading from "../Loading";
import styles from './Comments.module.css';

type CommentsProps = {
  appreciationId: number,
  hidden: boolean
};

export default function Comments({appreciationId, hidden}: CommentsProps) {

  const [status, setStatus] = useState('idle');
  const [comments, setComments] = useState<Comment[]>([]);

  useEffect(() => {
    if (hidden) {
      return
    }
    appreciationComments(appreciationId)
      .then((result) => {
        setComments(result);
        setStatus('success')
      }).catch(() => {
      setStatus('error');
    });

  }, [appreciationId, hidden]);

  return (
    <div className={`block is-clipped ${hidden ? styles.hide : ''}`}>
      <form>
        <div className="field is-grouped">
          <label className=" is-sr-only">Write a comment</label>
          <div className="control is-expanded">
            <textarea name="content" rows={2} className=" textarea"/>
          </div>
          <div className=" control">
            <button className="button is-primary" type="submit">Comment</button>
          </div>
        </div>
      </form>
      {status === "pending" && <Loading/>}
      {status === "success" && comments?.map(({content, createdAt, user}) => (
        <div className="comment">
          <div>
            <Link to={`/profile/${user.username}`}><strong>{user.name}</strong></Link>
            <small>
              <TimeAgo date={createdAt}/>
            </small>
          </div>
          <p>{content}</p>
        </div>))}
    </div>
  );
}
