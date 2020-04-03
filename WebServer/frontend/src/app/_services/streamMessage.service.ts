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
    label: "NotLiveCamera 2",
    source:
      "https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8"
  };

  //use defaultStream to learn type and set default, i think..
  private streamSource = new BehaviorSubject( this.defaultStream );
  selectedStream = this.streamSource.asObservable();

  constructor() { }

  changeStream(stream: IMediaStream) {
    this.streamSource.next(stream)
  }

}
