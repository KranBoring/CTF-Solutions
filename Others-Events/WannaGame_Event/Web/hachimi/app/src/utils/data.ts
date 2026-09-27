import characters from "./bulk";

export interface User {
  id: number;
  username: string;
  password: string;
}

export interface Character {
  name: string;
  height: number;
  image: string;
}

export function getCharacters(): Character[] {
  return characters;
}

export function getCharacter(name: string): Character | undefined {
  return characters.find((c) => c.name === name);
}

export function getUsers(): User[] {
  return [...users.values()];
}

const users = new Map<number, User>();
let nextId = 1;

export function addUser(username: string, password: string): User {
  const user = { id: nextId++, username, password };
  users.set(user.id, user);
  return user;
}

export function getUser(id: number): User | undefined {
  return users.get(id);
}

export function findUser(username: string): User | undefined {
  for (const user of users.values()) {
    if (user.username === username) return user;
  }
}

export function userExists(username: string): boolean {
  return findUser(username) !== undefined;
}
