import { Component, OnInit, Input } from '@angular/core';
import { RecordService } from "../_services/record.service";
import { FileuploadService } from "../_services/fileupload.service"
import { AuthService } from '../_services/auth.service';
import { IMediaStream } from "../_services/streamMessage.service";
import { MatSnackBar } from '@angular/material/snack-bar';
import { FormControl } from '@angular/forms';
import { VideoService } from '../_services/video.service';
import { videoSettings } from '../_models/video';

@Component({
  selector: 'app-video-utils',
  templateUrl: './video-utils.component.html',
  styleUrls: ['./video-utils.component.scss']
})
export class VideoUtilsComponent implements OnInit {
  @Input() stream: IMediaStream;
  fileToUpload: File = null;
  canUpload: Boolean = false;
  settings: videoSettings;

  constructor(
    private snackBar: MatSnackBar,
    private recordService: RecordService,
    private fileUploadService: FileuploadService,
    private auth: AuthService,
    private videoService: VideoService,
  ) {
    this.settings = <videoSettings>{};
    this.ctrl.setValue({ hour: 1, minute: 0, second: 0 });
  }

  ngOnInit(): void {
    this.getSettings();
  }

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
    this.canUpload = files.length > 0;
  }

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

  async uploadFile() {
    let res = await this.fileUploadService.postFile(this.fileToUpload, this.stream.ip);
    if (res === 200) {
      this.canUpload = false;
    }
    else this.openSnackBar("An error occured. Try again later", "OK");
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
    var time = (((this.ctrl.value.hour * 60) + this.ctrl.value.minute) * 60) + this.ctrl.value.second;

    this.auth.getId().toPromise().then(async userId => {
      if (userId) {
        let res = await this.recordService.postRecordInfo(
          this.stream.source,
          time,
          userId,
          "blabla", // TODO: Add a real camera ID
          3600,
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

  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: 5000,
    });
  }
}
