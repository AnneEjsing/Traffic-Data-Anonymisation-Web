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
  pausePlayText: String = "pause";
  isPaused: boolean = false;

  bitrates: BitrateOption[];

  streams: IMediaStream[] = [
      {
          type: 'hls',
          label: 'HLS: Streaming',
          /*source: 'http://192.168.1.107:8080/hls/stream.m3u8'*/
          source: 'https://d2zihajmogu5jn.cloudfront.net/bipbop-advanced/bipbop_16x9_variant.m3u8'
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

      //Whenever we play after a pause, we go to 100% time, so always live.
      //If not showing livestream dont have this.
      this.api.getDefaultMedia().subscriptions.play.subscribe(
        () => {
          this.api.seekTime(100, true);
        }
      )
  }

  ngOnInit() {
      this.currentStream = this.streams[0];
      this.api.getDefaultMedia().play();
  }

  setBitrate(option: BitrateOption) {
    if(this.currentStream.type == 'hls')
      this.vgHls.setBitrate(option);
  }

  onClickStream(stream: IMediaStream) {

      this.bitrates = null;

      let t: Subscription = timer(0, 10).subscribe(
          () => {
              this.currentStream = stream;
              t.unsubscribe();
          }
      );
      this.api.getDefaultMedia().play();
  }
  onClickPausePlay(){
    if(this.isPaused){
      this.api.getDefaultMedia().play();
      this.pausePlayText = "pause";
      this.isPaused = false;
    }
    else{
      this.api.getDefaultMedia().pause();
      this.pausePlayText = "play";
      this.isPaused = true;
    }
  }
}