import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import * as global from "./dispatcherConnection.service";
import { recording_info } from '../_models/video';

@Injectable({
  providedIn: 'root'
})
export class RecordService {
  readonly dispatcherUrl = global.dispatcherUrl;
  constructor(private http: HttpClient) { }

  async postRecordInfo(url: string, seconds: number, userId: string, cameraId: string, recording_intervals: number) {
    var data: any = {
      "url": url,
      "length": seconds,
      "user_id": userId,
      "camera_id": cameraId,
      "recording_intervals": recording_intervals,
    };

    let endpoint = global.dispatcherUrl + "record/interval";

    let res = await this.http.post(
      endpoint,
      data,
      this.constructHttpOptions())
      .toPromise().then(
        data => { return '200' },
        error => { return error.status }
      )

    return res;
  }

  async getRecordingInfo(camera_id: string, user_id: string) {
    var data = {
      "camera_id": camera_id,
      "user_id": user_id
    }

    let endpoint = global.dispatcherUrl + "get/recording";

    let res = await this.http.post(
      endpoint,
      data,
      this.constructHttpOptions())
      .toPromise().then(
        data => { return data },
        error => { return error.status }
      )

    return res;
  }

  async listRecordings(user_id: string) {
    var data = {
      "user_id": user_id
    }

    let endpoint = global.dispatcherUrl + "recordings/list/user_id";

    let res = await this.http.post(
      endpoint,
      data,
      this.constructHttpOptions())
      .toPromise().then(
        data => { return data },
        error => { return error.status }
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
}
