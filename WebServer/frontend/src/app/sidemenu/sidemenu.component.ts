import { Component, OnInit } from '@angular/core';
import { Subscription, timer } from "rxjs";
import { StreamMessageService, IMediaStream } from "../_services/streamMessage.service"
import { MatDialog } from '@angular/material/dialog';
import { AuthService } from '../_services/auth.service';
import { ProfileService } from '../_services/profile.service';
import { Rights } from "../_models/user";
import { SettingsDialog } from '../settings.dialog.component/settings.dialog.component';
import { CameraDialog } from '../add-camera/add-camera.component';
import { recording_info } from '../_models/video';
import { RecordService } from '../_services/record.service';

@Component({
  selector: 'app-sidemenu',
  templateUrl: './sidemenu.component.html',
  styleUrls: ['./sidemenu.component.scss']
})


export class SidemenuComponent implements OnInit {
  currentStream: IMediaStream;
  streams: IMediaStream[];
  role: string;
  loggedIn: boolean = false;
  email: string;
  recordings: Array<recording_info> = [];

  constructor(
    public dialog: MatDialog,
    private streamService: StreamMessageService,
    private profileService: ProfileService,
    private recordService: RecordService,
    private auth: AuthService,
  ) { }

  ngOnInit() {

    if (localStorage.getItem('session_token')) {
      this.profileService.listStreams().then(response => {
        this.streams = response;
        if (this.streams.length == 0)
          this.currentStream = this.streamService.defaultStream;
        else {
          this.streamService.changeStream(this.streams[0])
          this.streamService.selectedStream.subscribe(selectedStream => this.currentStream = selectedStream)
        }
      }).catch(error => { });

      this.auth.getRole().toPromise().then(rights => {
        if (rights) {
          this.loggedIn = true;
          this.role = rights;

          this.profileService.getUser().then(user => {
            this.email = user.email;
            this.recordService.listRecordings(user.user_id).then(recordings => {
              this.recordings = recordings;
            });
          });
        }
      });
    }
  }

  openSettings() {
    this.dialog.open(SettingsDialog);
  }

  isRecording(camera_id) {
    return this.recordings.some(recording => recording.camera_id == camera_id);
  }

  onClickStream(stream: IMediaStream) {
    let t: Subscription = timer(0, 10).subscribe(
      () => {
        this.streamService.changeStream(stream);
        t.unsubscribe();
      }
    );
  }


  openCameraDialog(): void {
    this.dialog.open(CameraDialog, {
      data: { label: "", source: "", description: "", ip: "" }
    });
  }
}