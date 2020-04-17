import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import * as global from "./dispatcherConnection.service";
import { CameraData } from "../add-camera/add-camera.component";

@Injectable()
export class CameraService {
    constructor(private http: HttpClient) { }

    readonly dispatcherUrl = global.dispatcherUrl;

    async createCamera(camera: CameraData) {
        const headers = this.constructHttpHeader();
        return await this.http.post(this.dispatcherUrl + "camera/create", camera, {headers, responseType: 'text'}).toPromise().then(
            data => { console.log("success"); return 200; },
            error => { console.log(error.status); return error.status; }
        );
    }

    constructHttpHeader() {
        const httpHeader = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('session_token'),
        });

        return httpHeader;
    }

    constructJson(camera: CameraData) {
        return "{\"source\":\""+camera.source+"\", \"ip\":\""+camera.ip+"\",\"label\":\""+camera.label+"\",\"description\":\""+camera.description+"\"";
    }

}
