import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import * as global from "./disptacher-connection.service"

@Injectable({
  providedIn: 'root'
})
export class RecordService {
readonly dispatcherUrl = global.dispatcherUrl;
  constructor(private http: HttpClient) { }

  async postRecordInfo(url: string, seconds: string) {
      var obj: any = { "url": url, "length": seconds };
      //var endpoint: string = this.dispatcherUrl + "video/record";
      var endpoint: string = "http://videodownloader:1336/record/interval"

      let res = await this.http.post( endpoint, obj,
          { headers: new HttpHeaders({
                  'Content-Type': 'application/json',
              }), responseType: 'text' })
          .toPromise().then(
              data => { return '200' },
              error => { return error.status }
          )

      return res;
  }
}
