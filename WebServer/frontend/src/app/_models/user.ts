export class user {
    user_id: string;
    email: string;
    rights: Rights;
}

export enum Rights {
    "admin" = "admin",
    "user" = "user",
}
