import { Component, OnInit, ViewChild, ChangeDetectionStrategy } from "@angular/core";
import { VgHLS, BitrateOption, VgAPI } from "ngx-videogular";
import { Subscription, timer } from "rxjs";
import { RecordService } from "../_services/record.service";
import {StreamMessageService, IMediaStream} from "../_services/streamMessage.service"

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: "app-videoplayer",
  templateUrl: "./videoplayer.component.html",
  styleUrls: ["./videoplayer.component.scss"]
})
export class VideoplayerComponent implements OnInit {
  @ViewChild(VgHLS) vgHls: VgHLS;

  currentStream: IMediaStream;
  api: VgAPI;
  bitrates: BitrateOption[];


  constructor(private recordService: RecordService, private streamService: StreamMessageService) {}

  onPlayerReady(api: VgAPI) {
    this.api = api;

    //Whenever we play after a pause, we go to 100% time, so always live.
    //If not showing livestream dont have this.
    this.api.getDefaultMedia().subscriptions.play.subscribe(
      () => {
        if(this.api.isLive){
          this.api.seekTime(100, true);
        }
      }
    )
    // //If not a live video just start playing asap
    // //If live this will make it a few seconds behind idk why so you have to manually press play.
    // this.api.getDefaultMedia().subscriptions.canPlay.subscribe(
    //   () => {
    //     if(!this.api.isLive){
    //       this.api.play();
    //     }
    //   }
    // )

  }

  ngOnInit() {
    this.streamService.selectedStream.subscribe(
      selectedStream => 
      {
        this.currentStream = selectedStream;
    })
  }

  setBitrate(option: BitrateOption) {
    if (this.currentStream.type == "hls") this.vgHls.setBitrate(option);
  }

  // onClickStream(stream: IMediaStream) {
  //     this.api.pause();
  //     this.bitrates = null;

  //     let t: Subscription = timer(0, 10).subscribe(
  //         () => {
  //             this.currentStream = stream;
  //             t.unsubscribe();
  //         }
  //     );
  //     this.api.getDefaultMedia().play();
  // }

  async startRecord(time: string) {
    let res = await this.recordService.postRecordInfo(
      this.currentStream.source,
      time
    );
    if (res === 200) console.log("success");
    else console.log("error");
  }
}
