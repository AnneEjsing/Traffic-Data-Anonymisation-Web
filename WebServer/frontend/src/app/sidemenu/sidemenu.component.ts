import { Component, OnInit, Inject } from '@angular/core';
import { Subscription, timer } from "rxjs";
import { StreamMessageService, IMediaStream } from "../_services/streamMessage.service";
import { ProfileService } from "../_services/profile.service"

@Component({
  selector: 'app-sidemenu',
  templateUrl: './sidemenu.component.html',
  styleUrls: ['./sidemenu.component.scss']
})


export class SidemenuComponent implements OnInit {
  currentStream: IMediaStream;

  //Change this to something that fetches it from a microservice.
  streams: IMediaStream[];

  loggedIn: boolean = false;
  email: string;

  constructor(
    private streamService: StreamMessageService,
    private profileService: ProfileService,
    ) { }
    
  ngOnInit() {
    this.profileService.listStreams().then(
      response => {
        this.streams = response;
        this.streamService.changeStream(this.streams[0])
        this.streamService.selectedStream.subscribe(selectedStream => this.currentStream = selectedStream)
    },
    error => {console.log("TODO: Lav route til login")})
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