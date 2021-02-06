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

async function get<T>(url: string): Promise<T> {
  const response = await axios.get(url, {
    headers: authorizationHeaders()
  });

  return response.data
}

export async function appreciations(): Promise<Appreciation[]> {
  return get("/api/appreciations");
}

export async function notificationCount(): Promise<number> {
  return get("/api/notifications/_count");
}

export async function appreciationComments(id: number): Promise<Comment[]> {
  return get(`/api/appreciations/${id}/comments`);
}

export async function appreciationLikes(id: number): Promise<Like[]> {
  return get(`/api/appreciations/${id}/likes`);
}
