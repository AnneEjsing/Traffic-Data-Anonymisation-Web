import { Component, Inject, Optional } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { LoginService } from "../_services/login.service";

export interface DialogData {
  email: string;
  password: string;
}

@Component({
  selector: 'login-dialog',
  templateUrl: './loginDialog.component.html',
})
export class LoginDialog {
  requesting: boolean = false;
  failedLogin: boolean = false;
  constructor(
    public dialogRef: MatDialogRef<LoginDialog>,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: DialogData,
    public loginService: LoginService,
  ) { }

  onNoClick(): void {
    this.dialogRef.close();
  }

  async awaitLogin() {
    this.requesting = true;
    const res = await this.loginService.login(this.data.email, this.data.password);
    this.requesting = false;

    if (res == 200) {
      this.dialogRef.close(this.data.email);
    }
    else {
      this.failedLogin = true;
    }
  }
}