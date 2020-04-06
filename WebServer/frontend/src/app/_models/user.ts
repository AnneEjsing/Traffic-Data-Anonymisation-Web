export class user {
    id: string;
    email: string;
    rights: Rights;
}

export enum Rights {
    "admin" = "admin",
    "user" = "user",
}
