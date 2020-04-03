import { Component, OnInit, Input } from '@angular/core';
import { RecordService } from "../_services/record.service";
import { FileuploadService } from "../_services/fileupload.service"

@Component({
  selector: 'app-video-utils',
  templateUrl: './video-utils.component.html',
  styleUrls: ['./video-utils.component.scss']
})
export class VideoUtilsComponent implements OnInit {
  @Input() source:string;
  fileToUpload: File = null;
  canUpload: Boolean = false;

  constructor(private recordService: RecordService, private fileUploadService: FileuploadService) { }

  ngOnInit(): void {
  }

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
    this.canUpload = true;
  }

  async uploadFileToActivity() {
    console.log(this.fileToUpload)
    let res = await this.fileUploadService.postFile(this.fileToUpload, this.source);
    console.log(res)
    if (res === 200) { this.canUpload = false; console.log("success");}
    else console.log("error");

  }

  async startRecord(time: string) {
    let res = await this.recordService.postRecordInfo(
      this.source,
      time
    );
    if (res === '200') console.log("success");
    else console.log("error");
  }

}
