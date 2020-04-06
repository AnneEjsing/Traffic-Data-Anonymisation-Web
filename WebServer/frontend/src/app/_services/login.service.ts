import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";


@Injectable()
export class LoginService {
    constructor(private http: HttpClient) { }

    //readonly dispatcherUrl = global.dispatcherUrl;
    readonly ProfileServiceUrl = "http://192.168.99.100:1338/"
    async login(email: string, password: string) {
        const headers = this.constructHttpHeader(email, password);
        let res = await this.http.post(this.ProfileServiceUrl + "login",
            { "email": email, "password": password },
            { headers, responseType: 'text' }
        ).toPromise().then(
            data => {
                localStorage.setItem('session_token', data);
                localStorage.setItem('email', email);
                return 200;
            },
            error => {
                const status = error.status;
                return status;
            }
        );

        return res;
    }

    constructHttpHeader(email: string, password: string) {
        const httpHeader = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + btoa(email + ':' + password),
        });

        return httpHeader;
    }

}
