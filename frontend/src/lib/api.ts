import axios from "axios";
import {authorizationHeaders} from "./utils";
import {User} from "./auth";

export type Like = {
  user: User;
  id: number
}

export type Comment = {
  createdAt: string;
  id: number,
  content: string,
  user: User
}

export type Appreciation = {
  id: number,
  content: string,
  createdBy: User,
  commentCount: number,
  createdAt: string,
  likeCount: number,
  mentions: { user: User }[],
  viewerLike: Like
}

export type OneOnOne = {
  id: number,
  user: User,
  createdAt: string,
  createdBy: User
}

export type OneOnOneActionItem = {
  id: number,
  state: boolean
  content: string
  createdBy: User
}

export type OneOnOneDetail = OneOnOne & {
  actionItems: OneOnOneActionItem[]
}

async function get<T>(url: string): Promise<T> {
  const response = await axios.get(url, {
    headers: authorizationHeaders()
  });

  return response.data
}

export function appreciations(): Promise<Appreciation[]> {
  return get("/api/appreciations");
}

export function notificationCount(): Promise<number> {
  return get("/api/notifications/_count");
}

export function appreciationComments(id: number): Promise<Comment[]> {
  return get(`/api/appreciations/${id}/comments`);
}

export function appreciationLikes(id: number): Promise<Like[]> {
  return get(`/api/appreciations/${id}/likes`);
}

export function oneOnOnes(): Promise<OneOnOne[]> {
  return get("/api/one_on_ones")
}

export function oneOnOneById(id: number | string): Promise<OneOnOneDetail> {
  return get(`/api/one_on_ones/${id}`)
}

export function userByUsername(username: string): Promise<User> {
  return get(`/api/users/${username}`)
}
