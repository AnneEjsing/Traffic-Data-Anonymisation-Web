import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import * as global from "./disptacher-connection.service"

@Injectable({
  providedIn: "root"
})

export class FileuploadService {
  readonly dispatcherUrl = global.dispatcherUrl;
  constructor(private http: HttpClient) {}

  async postFile(file: File, cameraUrl: string) {
    console.log(file)
    let formData:FormData = new FormData();
    formData.append('file', file, file.name);
    formData.append('url', cameraUrl);
    formData.forEach((value,key) => {
      console.log(key+" "+value)
    });
    
    var endpoint: string = this.dispatcherUrl + "model/upload"

    let res = await this.http
      .post(endpoint, formData, { headers: new HttpHeaders(), responseType: "text" })
      .toPromise()
      .then(
        data => { return '200'; },
        error => { return error.status; }
      );

    return res;
  }
}
