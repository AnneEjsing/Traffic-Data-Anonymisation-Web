import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { user } from '../_models/user';
import { rejects } from 'assert';
import * as global from "./dispatcherConnection.service";
import { IMediaStream } from "./streamMessage.service"

@Injectable()
export class ProfileService {
    constructor(
        private http: HttpClient,
    ) { }

    readonly dispatcherUrl = global.dispatcherUrl;

    async getUser(): Promise<user> {
        return this.http.get<user>(this.dispatcherUrl + 'get/user', { headers: this.constructHttpOptions() }).toPromise();
    }

    async listUsers(): Promise<string> {
        return this.http.get<string>(this.dispatcherUrl + "user/list").toPromise();
    }

    async listStreams(): Promise<Array<IMediaStream>> {
        const headers = this.constructHttpOptions();
        return this.http.get<Array<IMediaStream>>(this.dispatcherUrl + "camera/list", { headers, responseType: 'json' }).toPromise();
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
        const httpOptions = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('session_token')
        });

        return httpOptions;
    }

    constructHttpHeaders() {
        const httpHeader = new HttpHeaders({
            'Content-Type': 'application/json',
        });

        return httpHeader;
    }
}