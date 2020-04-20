import { Component, AfterViewInit, ViewChild, ChangeDetectionStrategy, OnInit } from "@angular/core";
import { VgHLS, BitrateOption, VgAPI } from "ngx-videogular";
import { Subscription, timer } from "rxjs";
import { StreamMessageService, IMediaStream } from "../_services/streamMessage.service";
import { AuthService } from '../_services/auth.service';
import { VideoService } from '../_services/video.service';
import { videoSettings } from '../_models/video';
import { FormControl } from '@angular/forms';

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

  role: string;
  ctrl = new FormControl('', (control: FormControl) => {
    const value = control.value;

    if (!value) {
      return null;
    }

    return null;
  });

  constructor(
    private streamService: StreamMessageService,
    private auth: AuthService,
    private videoService: VideoService,
  ) {
    this.auth.getRole().subscribe(role => {
      this.role = role;
    });
  }

  ngOnInit() { }

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
    this.vgHls.setBitrate(option);
  }

  SetRecordingLimit() {
    var newSettings: videoSettings = {
      recording_limit: (((this.ctrl.value.hour * 60) + this.ctrl.value.minute) * 60) + this.ctrl.value.second
    }

    this.videoService.updateSettings(newSettings).then(response => { });
  }
}
