import { Component, Inject, Optional } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { CameraService } from "../_services/camera.service";

export interface CameraData {
  label: string;
  source: string;
  description: string;
  ip: string;
}

@Component({
  selector: "app-add-camera",
  templateUrl: "./add-camera.component.html",
})
export class CameraDialog {
  requesting: boolean = false;
  error: boolean = false;

  constructor(
    public dialogRef: MatDialogRef<CameraDialog>,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: CameraData,
    public cameraService: CameraService
  ) {}

  ngOnInit(): void { }

  close() {
    this.dialogRef.close();
  }

  async save() {
    this.requesting = true;
    const res = await this.cameraService.createCamera(this.data);
    this.requesting = false;

    if (res == 200) {
      this.dialogRef.close();
      window.location.reload();
    } else {
      this.error = true;
    }
  }
}
