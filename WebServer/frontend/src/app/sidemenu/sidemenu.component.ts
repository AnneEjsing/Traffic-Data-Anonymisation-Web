import { Component, OnInit, Inject } from '@angular/core';
import { Subscription, timer } from "rxjs";
import { StreamMessageService, IMediaStream } from "../_services/streamMessage.service"
import { Router } from '@angular/router';
import { LoginDialog, DialogData } from "../login/loginDialog.component";
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { AuthService } from '../_services/auth.service';
import { ProfileService } from '../_services/profile.service';
import { Rights } from "../_models/user";
import { VideoService } from '../_services/video.service';
import { videoSettings, recording_info } from '../_models/video';
import { RecordService } from '../_services/record.service';
import { ThrowStmt } from '@angular/compiler';

@Component({
  selector: 'app-sidemenu',
  templateUrl: './sidemenu.component.html',
  styleUrls: ['./sidemenu.component.scss']
})


export class SidemenuComponent implements OnInit {
  currentStream: IMediaStream;

  //Change this to something that fetches it from a microservice.
  streams: IMediaStream[] = [
    {
      label: "LiveCamera 1",
      /*source: 'http://192.168.1.107:8080/hls/stream.m3u8'*/
      source:
        "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8",
      ip: "localhost"
    },
    {
      label: "NotLiveCamera 2",
      source:
        "https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8",
      ip: "localhost"
    },
    {
      label: "NotLiveCamera 3",
      source:
        "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8",
      ip: "localhost"
    },
    {
      label: "NotLiveCamera 4",
      source:
        "https://mnmedias.api.telequebec.tv/m3u8/29880.m3u8",
      ip: "localhost"
    }
  ];

  loggedIn: boolean = false;
  email: string;
  recordings: Array<recording_info> = [];

  constructor(
    private streamService: StreamMessageService,
    public dialog: MatDialog,
    private auth: AuthService,
    private recordService: RecordService,
  ) { }

  ngOnInit(): void {
    this.streamService.changeStream(this.streams[0])
    this.streamService.selectedStream.subscribe(selectedStream => this.currentStream = selectedStream)

    this.auth.getId().subscribe(id => {
      if (id) {
        this.recordService.listRecordings(id).then(recordings => {
          this.recordings = recordings;
        });
      }
    });
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
}