import { Component, Inject, Optional } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { CameraService } from "../_services/camera.service";

@Component({
  selector: "app-share-stream",
  templateUrl: "./share-stream.component.html",
  styleUrls: ["./share-stream.component.scss"],
})
export class ShareStreamComponent {
  requesting: boolean = false;
  failed: boolean = false;

  constructor(
    public dialogRef: MatDialogRef<string>,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: any,
    public cameraService: CameraService
  ) {}

  async save() {
    this.requesting = true;
    let res = await this.cameraService.createAccessRights(this.data);
    this.requesting = false;

    if (res == 200) {
      this.dialogRef.close();
      window.location.reload();
    } else if (res == 500){
      this.failed = true;
    }
     else {
    }
  }

  close() {
    this.dialogRef.close();
  }
}
