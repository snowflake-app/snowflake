import axios from "axios";

export type User = {
  readonly name: string,
  readonly designation: string,
  readonly team_name: string,
  readonly email: string,
  readonly profile_pic: string,
  readonly username: string,
}

type Session = {
  readonly token: string,
  readonly user: User
}

let currentSession: Session;

export async function authenticate(token: string) {
  const {data: session} = await axios.post('/api/tokens', {
    'token': token
  });

  currentSession = session;

  return session;
}

export function isLoggedIn() {
  return !!currentSession;
}

export function currentUser() {
  return currentSession?.user;
}

export function token() {
  return currentSession?.token;
}

export function logout() {
}
