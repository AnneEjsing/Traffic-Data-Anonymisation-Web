import { Component, OnInit, Inject } from '@angular/core';
import { Subscription, timer } from "rxjs";
import { StreamMessageService, IMediaStream } from "../_services/streamMessage.service";
import { ProfileService } from "../_services/profile.service"
import { CameraDialog } from '../add-camera/add-camera.component'
import { MatDialog } from '@angular/material/dialog';


@Component({
  selector: 'app-sidemenu',
  templateUrl: './sidemenu.component.html',
  styleUrls: ['./sidemenu.component.scss']
})


export class SidemenuComponent implements OnInit {
  currentStream: IMediaStream;
  streams: IMediaStream[];

  loggedIn: boolean = false;
  email: string;

  constructor(
    public dialog: MatDialog,
    private streamService: StreamMessageService,
    private profileService: ProfileService
    ) { }
    
  ngOnInit() {
    if (localStorage.getItem('session_token'))
    {
        this.profileService.listStreams().then(
          response => {
            this.streams = response;
            this.streamService.changeStream(this.streams[0])
            this.streamService.selectedStream.subscribe(selectedStream => this.currentStream = selectedStream)
        },
        error => {})
    }
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