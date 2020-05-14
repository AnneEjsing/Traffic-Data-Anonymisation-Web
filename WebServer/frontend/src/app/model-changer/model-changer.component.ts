import { Component, OnInit, Inject, Optional } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FileuploadService } from '../_services/fileupload.service';
import { MatSnackBar } from '@angular/material/snack-bar';


@Component({
  selector: 'app-model-changer',
  templateUrl: './model-changer.component.html',
  styleUrls: ['./model-changer.component.scss']
})
export class ModelChangerComponent implements OnInit {
  requesting: boolean;
  fileToUpload: File = null;
  canUpload: boolean = false;
  type: string = "face";

  constructor(
    public dialogRef: MatDialogRef<string>,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: any,
    private fileUploadService: FileuploadService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {

  }

  handleFileInput(files: FileList) {
    this.fileToUpload = files.item(0);
    this.canUpload = files.length > 0;
  }

  async save() {
    this.requesting = true;
    let res = await this.fileUploadService.postFile(this.fileToUpload, this.data['camera_id'], this.type);
    this.requesting = false;

    if (res === 200) {
      this.canUpload = false;
      var result = {
        type: this.type,
        name: this.fileToUpload.name
      }
      this.dialogRef.close(result);
    }
    else this.openSnackBar("An error occured. Try again later", "OK");
  }

  choseType(event) {
    var type = event.target.value;
    if (type == "Face") {
      this.type = "face";
    }
    else if (type == "License plate") {
      this.type = "license_plate";
    }
  }

  close() {
    this.dialogRef.close(null);
  }

  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: 5000,
    });
  }

}
