import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import * as global from "./dispatcherConnection.service";

@Injectable({
  providedIn: 'root'
})
export class RecordService {
readonly dispatcherUrl = global.dispatcherUrl;
  constructor(private http: HttpClient) { }

  async postRecordInfo(url: string, seconds: string, userId: string, cameraId: string) {
    var data: any = {
      "url": url,
      "length": seconds,
      "user_id": userId,
      "camera_id": cameraId,
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
