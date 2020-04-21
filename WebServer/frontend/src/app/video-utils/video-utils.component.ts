import { Component, OnInit, Input } from '@angular/core';
import { RecordService } from "../_services/record.service";
import { AuthService } from '../_services/auth.service';
import { IMediaStream } from "../_services/streamMessage.service";

@Component({
  selector: 'app-video-utils',
  templateUrl: './video-utils.component.html',
  styleUrls: ['./video-utils.component.scss']
})
export class VideoUtilsComponent implements OnInit {
  @Input() stream: IMediaStream;
  fileToUpload: File = null;
  canUpload: Boolean = false;

  constructor(
    private recordService: RecordService, 
    private auth: AuthService,
    ) { }

  ngOnInit(): void {
  }

  async startRecord(time: string) {
    this.auth.getId().toPromise().then(async userId => {
      if (userId) {
        let res = await this.recordService.postRecordInfo(
          this.stream.source,
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
