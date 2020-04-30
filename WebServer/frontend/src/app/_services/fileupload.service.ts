import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import * as global from "./dispatcherConnection.service";

@Injectable({
  providedIn: "root"
})

export class FileuploadService {
  readonly dispatcherUrl = global.dispatcherUrl;
  constructor(private http: HttpClient) {}

  async postFile(file: File, camera_id:string): Promise<number> {
    let formData:FormData = new FormData();
    formData.append('file', file, file.name);
    formData.append('camera_id', camera_id);
    
    var endpoint: string = this.dispatcherUrl + "model/upload"
    let res = await this.http.post(
      endpoint,
      formData,
      this.constructHttpOptions())
      .toPromise().then(
        data => { return 200 },
        error => { return error.status }
      )
    return res;
  }

  constructHttpOptions() {
    const httpOptions = {
      headers: new HttpHeaders({
        'Authorization': 'Bearer ' + localStorage.getItem('session_token'),
      })
    };

    return httpOptions;
  }
}
