export interface User {
  id: string;
  displayName: string;
  createdAt: Date;
}

export interface CurrentUser {
  id: string;
  email: string;
  displayName: string;
  createdAt: Date;
  updatedAt: Date;
}
