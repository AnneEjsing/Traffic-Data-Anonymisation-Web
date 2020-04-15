import { Component, OnInit, Input } from '@angular/core';
import { RecordService } from "../_services/record.service";
import { FileuploadService } from "../_services/fileupload.service"
import { AuthService } from '../_services/auth.service';
import { IMediaStream } from "../_services/streamMessage.service";
import { MatSnackBar } from '@angular/material/snack-bar';

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
    private snackBar: MatSnackBar,
    private recordService: RecordService, 
    private fileUploadService: FileuploadService,
    private auth: AuthService,
    ) { }

  ngOnInit(): void {
  }

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
    this.canUpload = files.length > 0;
  }

  async uploadFile() {
    let res = await this.fileUploadService.postFile(this.fileToUpload);
    if (res === 200) { 
      this.canUpload = false; 
    }
    else this.openSnackBar("An error occured. Try again later", "OK");
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

  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: 5000,
    });
  }
}
