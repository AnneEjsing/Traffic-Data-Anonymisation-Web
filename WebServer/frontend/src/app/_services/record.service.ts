import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import * as global from "./dispatcherConnection.service";

@Injectable({
  providedIn: 'root'
})
export class RecordService {

  constructor(private http: HttpClient) { }

  async postRecordInfo(url: string, seconds: string) {
    var obj: any = {
      "url": url,
      "length": seconds
    };

    let res = await this.http.post(
      global.dispatcherUrl + "/record/interval",
      obj,
      {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }), responseType: 'text'
      })
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
      })
    };

    return httpOptions;
  }
}
