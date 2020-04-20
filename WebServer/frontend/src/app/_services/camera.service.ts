import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import * as global from "./dispatcherConnection.service";
import { CameraData } from "../add-camera/add-camera.component";
import { IMediaStream } from './streamMessage.service';

@Injectable()
export class CameraService {
    constructor(private http: HttpClient) { }

    readonly dispatcherUrl = global.dispatcherUrl;

    async createCamera(camera: CameraData) {
        const headers = this.constructHttpHeader();
        return await this.http.post(this.dispatcherUrl + "camera/create", camera, {headers, responseType: 'text'}).toPromise().then(
            data => { return 200; },
            error => { return error.status; }
        );
    }

    async putCamera(camera: CameraData) {
        const headers = this.constructHttpHeader();
        return await this.http.put(this.dispatcherUrl + "camera/update", camera, {headers, responseType: 'text'}).toPromise().then(
            data => { return 200; },
            error => { return error.status; }
        );
    }

    async deleteCamera(camera: IMediaStream) {
        const headers = this.constructHttpHeader();
        const id = "?id=" + camera.camera_id;
        return await this.http.delete(this.dispatcherUrl + "camera/delete"+id, {headers}).toPromise().then(
            data => { return 200; },
            error => { return error.status; }
        );
    }

    async getCamera(camera: IMediaStream)
    {
        const headers = this.constructHttpHeader();
        const id = "?id=" + camera.camera_id;
        return await this.http.get<CameraData>(this.dispatcherUrl + "camera/get" + id, { headers, responseType: 'json' }).toPromise();
    }

    async createAccessRights(data: any)
    {
        console.log(data)
        const headers = this.constructHttpHeader();
        return await this.http.post(this.dispatcherUrl + "access/create", data, {headers, responseType: 'text'}).toPromise().then(
            data => { return 200; },
            error => { console.log(error); return error.status; }
        );
    }

    constructHttpHeader() {
        const httpHeader = new HttpHeaders({
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('session_token'),
        });

        return httpHeader;
    }
}
