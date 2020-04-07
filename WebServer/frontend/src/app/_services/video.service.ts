import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import * as global from "./dispatcherConnection.service";
import { videoSettings } from '../_models/video';

@Injectable()
export class VideoService {
    constructor(
        private http: HttpClient,
    ) { }

    readonly dispatcherUrl = global.dispatcherUrl;

    async getSettings(): Promise<videoSettings> {
        return this.http.get<videoSettings>(this.dispatcherUrl + "settings/get", this.constructHttpOptions()).toPromise();
    }

    async updateSettings(newSettings: videoSettings): Promise<any> {
        return this.http.post<any>(this.dispatcherUrl + "settings/update", newSettings, this.constructHttpOptions()).toPromise();
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