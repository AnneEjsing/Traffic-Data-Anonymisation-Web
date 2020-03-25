import { Component, OnInit, ViewChild } from "@angular/core";
import { VgHLS, BitrateOption, VgAPI } from "ngx-videogular";
import { Subscription, timer } from "rxjs";
import { RecordService } from "../_services/record.service";

export interface IMediaStream {
  type: "vod" | "hls";
  source: string;
  label: string;
}

@Component({
  selector: "app-videoplayer",
  templateUrl: "./videoplayer.component.html",
  styleUrls: ["./videoplayer.component.scss"]
})
export class VideoplayerComponent implements OnInit {
  @ViewChild(VgHLS) vgHls: VgHLS;

  currentStream: IMediaStream;
  api: VgAPI;
  pausePlayText: String = "pause";
  isPaused: boolean = false;

  bitrates: BitrateOption[];

  streams: IMediaStream[] = [
    {
      type: "hls",
      label: "Camera 1",
      /*source: 'http://192.168.1.107:8080/hls/stream.m3u8'*/
      source:
        "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8"
    },
    {
      type: "hls",
      label: "Camera 2",
      source:
        "https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8"
    },
    {
      type: "hls",
      label: "Camera 3",
      source:
        "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8"
    },
    {
      type: "hls",
      label: "Camera 4",
      source:
        "https://mnmedias.api.telequebec.tv/m3u8/29880.m3u8"
    }
  ];

  constructor(private recordService: RecordService) {}

  onPlayerReady(api: VgAPI) {
    this.api = api;
  }

  ngOnInit() {
    this.currentStream = this.streams[0];
      this.api = api;

      //Whenever we play after a pause, we go to 100% time, so always live.
      //If not showing livestream dont have this.
      this.api.getDefaultMedia().subscriptions.play.subscribe(
        () => {
          this.api.seekTime(100, true);
        }
      )
  }

  setBitrate(option: BitrateOption) {
    if (this.currentStream.type == "hls") this.vgHls.setBitrate(option);
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

  async startRecord(time: string) {
    let res = await this.recordService.postRecordInfo(
      this.currentStream.source,
      time
    );
    if (res === 200) console.log("success");
    else console.log("error");
  }
}
