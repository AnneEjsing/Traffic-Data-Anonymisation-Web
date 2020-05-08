import { Component, OnInit } from '@angular/core';
import { Subscription, timer } from "rxjs";
import { StreamMessageService, IMediaStream } from "../_services/streamMessage.service"
import { MatDialog } from '@angular/material/dialog';
import { AuthService } from '../_services/auth.service';
import { ProfileService } from '../_services/profile.service';
import { recording_info, recorded_video } from '../_models/video';
import { RecordService } from '../_services/record.service';
import { CameraDialog } from '../add-camera/add-camera.component'
import { VideoService } from '../_services/video.service';
import { SettingsDialog } from '../settings.dialog.component/settings.dialog.component';
import { animate, state, style, transition, trigger } from '@angular/animations';
import * as fileSaver from 'file-saver';

@Component({
  selector: 'app-sidemenu',
  templateUrl: './sidemenu.component.html',
  styleUrls: ['./sidemenu.component.scss'],
  animations: [
    trigger('indicatorRotate', [
      state('collapsed', style({ transform: 'rotate(0deg)' })),
      state('expanded', style({ transform: 'rotate(180deg)' })),
      transition('expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4,0.0,0.2,1)')
      ),
    ])
  ]
})


export class SidemenuComponent implements OnInit {
  currentStream: IMediaStream;
  streams: IMediaStream[];
  recorded_videos: recorded_video[];
  showRecordings: boolean = false;

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
    private videoService: VideoService,
  ) { }

  ngOnInit() {
    this.videoService.list_recorded_videos().then(result => {
      this.recorded_videos = result;
    });

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

      this.auth.getRole().toPromise().then(role => {
        if (role) {
          this.loggedIn = true;
          this.role = role;

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

  list_recordings() {
    this.showRecordings = !this.showRecordings;
  }

  toShortDate(date: Date) {
    return new Date(date).toDateString();
  }

  downloadVideo(video: recorded_video) {
    this.videoService.downloadFile(video.video_id).subscribe(response => {
      let blob: any = new Blob([response.blob()], { type: 'video/mp4' });
      var file_name = video.label + "-" + this.toShortDate(video.save_time);
      fileSaver.saveAs(blob, file_name);
    }), error => console.log('Error downloading the file');

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