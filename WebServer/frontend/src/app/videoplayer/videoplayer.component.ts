import { Component, OnInit, ViewChild } from "@angular/core";
import { VgHLS, VgDASH, IDRMLicenseServer, BitrateOption, VgAPI } from 'ngx-videogular';
import { Subscription, timer } from 'rxjs';

export interface IMediaStream {
  type: 'vod' | 'hls';
  source: string;
  label: string;
}

@Component({
  selector: 'app-videoplayer',
  templateUrl: './videoplayer.component.html',
  styleUrls: ['./videoplayer.component.scss']
})

export class VideoplayerComponent implements OnInit {
  @ViewChild(VgDASH) vgDash: VgDASH;
  @ViewChild(VgHLS) vgHls: VgHLS;

  currentStream: IMediaStream;
  api: VgAPI;

  bitrates: BitrateOption[];

  streams: IMediaStream[] = [
      {
          type: 'hls',
          label: 'HLS: Streaming',
          /*source: 'http://192.168.1.107:8080/hls/stream.m3u8'*/
          source: 'https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8'
      },
      {
        type: 'hls',
        label: 'HLS: Streaming',
        source: 'https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8'
    },
  ];

  constructor() {
  }

  onPlayerReady(api: VgAPI) {
      this.api = api;
  }

  ngOnInit() {
      this.currentStream = this.streams[0];
  }

  setBitrate(option: BitrateOption) {
    if(this.currentStream.type == 'hls')
      this.vgHls.setBitrate(option);
  }

  onClickStream(stream: IMediaStream) {
      this.api.pause();
      this.bitrates = null;

      let t: Subscription = timer(0, 10).subscribe(
          () => {
              this.currentStream = stream;
              t.unsubscribe();
          }
      );
  }
}