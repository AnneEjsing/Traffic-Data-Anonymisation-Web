import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { user } from '../_models/user';
import { rejects } from 'assert';


@Injectable()
export class ProfileService {
    constructor(
        private http: HttpClient,
    ) { }

    readonly dispatcherUrl = "http://localhost:443/";

    async getUser(): Promise<user> {
        return this.http.get<user>(this.dispatcherUrl + 'get/user', this.constructHttpOptions()).toPromise();
    }

    async getAdmin(): Promise<user> {
        return this.http.get<user>(this.dispatcherUrl + 'get/admin', this.constructHttpOptions()).toPromise();
    }

    async listUsers(): Promise<string> {
        return this.http.get<string>(this.dispatcherUrl + "user/list").toPromise();
    }

    async signupUser(email: String, password: String) {
        const headers = this.constructHttpHeaders();
        var newUser = {
            email: email,
            password: password,
            rights: 'user',
        }

        let res = await this.http.post(this.dispatcherUrl + "signup/user", newUser, { headers, responseType: 'text' }).toPromise().then(
            data => 200,
            error => error.status
        )

        return res;
    }

    constructHttpOptions() {
        const httpOptions = {
            headers: new HttpHeaders({
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('session_token'),
            })
        };

        return httpOptions;
    }

    constructHttpHeaders() {
        const httpHeader = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return httpHeader;
    }
}