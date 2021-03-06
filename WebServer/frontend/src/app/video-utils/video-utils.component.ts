import { Component, OnInit, Input } from '@angular/core';
import { RecordService } from "../_services/record.service";
import { AuthService } from '../_services/auth.service';
import { IMediaStream } from "../_services/streamMessage.service";
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormControl } from '@angular/forms';
import { VideoService } from '../_services/video.service';
import { videoSettings, recording_info } from '../_models/video';

@Component({
  selector: 'app-video-utils',
  templateUrl: './video-utils.component.html',
  styleUrls: ['./video-utils.component.scss']
})
export class VideoUtilsComponent implements OnInit {
  @Input() stream: IMediaStream;
  @Input() recording: recording_info;
  fileToUpload: File = null;
  canUpload: boolean = false;
  settings: videoSettings;

  ctrl = new FormControl('', (control: FormControl) => {
    const value = control.value;

    if (!value) {
      return null;
    }
    else if ((((value.hour * 60) + value.minute) * 60) + value.second > this.settings.recording_limit) {
      return { exceededMax: true };
    }

    return null;
  });


  constructor(
    private snackBar: MatSnackBar,
    private recordService: RecordService,
    private auth: AuthService,
    private videoService: VideoService,
  ) {
    this.settings = <videoSettings>{};
    this.ctrl.setValue({ hour: 1, minute: 0, second: 0 });
  }

  ngOnInit(): void {
    this.getSettings();
  }

  getSettings() {
    this.videoService.getSettings().then(settings => {
      this.settings = settings;
      var secounds = this.settings.recording_limit;
      this.ctrl.setValue({
        hour: Math.floor(secounds / 3600),
        minute: Math.floor(secounds % 3600 / 60),
        second: Math.floor(secounds % 3600 % 60)
      });
    });
  }

  async startRecord() {
    if (this.ctrl.valid) {
      var time = (((this.ctrl.value.hour * 60) + this.ctrl.value.minute) * 60) + this.ctrl.value.second;

      this.auth.getId().toPromise().then(async userId => {
        if (userId) {
          let res = await this.recordService.postRecordInfo(
            this.stream.source,
            time,
            userId,
            this.stream.camera_id,
            3600,
          );

          this.recordService.getRecordingInfo(this.stream.camera_id, userId).then(recording => {
            this.recording = recording;
          });

          if (res == 200) {
            this.openSnackBar("Recording started", "OK");
            window.location.reload();
          }
          else {
            this.openSnackBar("Recording failed", "OK");
          }
        }
        else {
          this.openSnackBar("You must be logged in to start a recording!", "OK");
        }
      })
    }
  }

  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: 2000,
    });
  }
}
