import { Component, AfterViewInit, ViewChild, ChangeDetectionStrategy, OnInit } from "@angular/core";
import { VgHLS, BitrateOption, VgAPI } from "ngx-videogular";
import { Subscription, timer } from "rxjs";
import { RecordService } from "../_services/record.service";
import { StreamMessageService, IMediaStream } from "../_services/streamMessage.service";
import { AuthService } from '../_services/auth.service';
import { VideoService } from '../_services/video.service';
import { videoSettings } from '../_models/video';

@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  selector: "app-videoplayer",
  templateUrl: "./videoplayer.component.html",
  styleUrls: ["./videoplayer.component.scss"]
})
export class VideoplayerComponent implements AfterViewInit, OnInit {
  @ViewChild(VgHLS) vgHls: VgHLS;

  //Needs to be inizialised to something or it break...
  currentStream: IMediaStream = this.streamService.defaultStream;

  api: VgAPI;
  bitrates: BitrateOption[];
  settings: videoSettings;

  constructor(
    private recordService: RecordService,
    private streamService: StreamMessageService,
    private auth: AuthService,
    private videoService: VideoService,
  ) { }

  ngOnInit() {
    this.getSettings();
  }

  onPlayerReady(api: VgAPI) {
    this.api = api;

    //Whenever we play after a pause, we go to 100% time, so always live.
    //If not showing livestream dont have this.
    this.api.getDefaultMedia().subscriptions.play.subscribe(
      () => {
        if (this.api.isLive) {
          this.api.seekTime(100, true);
        }
      }
    )
  }

  ngAfterViewInit() {
    this.streamService.selectedStream.subscribe(
      selectedStream => {
        this.api.pause();
        this.bitrates = null;

        //IDK why we need this Subscription thingy, but the buffer breaks if not...
        let t: Subscription = timer(0, 10).subscribe(
          () => {
            this.currentStream = selectedStream;
            t.unsubscribe();
          }
        );
      })
  }

  setBitrate(option: BitrateOption) {
    if (this.currentStream.type == "hls") this.vgHls.setBitrate(option);
  }

  getSettings() {
    this.videoService.getSettings().then(settings => {
      this.settings = settings;
    });
  }

  async startRecord(time: string) {
    this.auth.getId().toPromise().then(async userId => {
      if (userId) {
        let res = await this.recordService.postRecordInfo(
          this.currentStream.source,
          time,
          userId,
          "blabla" // TODO: Add a real camera ID
        );

        // TODO: Something...
        if (res === 200) console.log("success");
        else console.log("error");
      }
      else {
        // TODO: Error handling
        console.log("error: unautherised")
      }
    })
  }
}
