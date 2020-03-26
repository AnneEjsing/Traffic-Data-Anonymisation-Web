import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface IMediaStream {
    type: "vod" | "hls";
    source: string;
    label: string;
  }
  
@Injectable()
export class StreamMessageService {
  defaultStream:IMediaStream =
  {
    type: "hls",
    label: "Camera 1",
    /*source: 'http://192.168.1.107:8080/hls/stream.m3u8'*/
    source:
    "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8"
  }
  private streamSource = new BehaviorSubject( this.defaultStream
    );
  selectedStream = this.streamSource.asObservable();

  constructor() { }

  changeStream(stream: IMediaStream) {
    this.streamSource.next(stream)
  }

}
