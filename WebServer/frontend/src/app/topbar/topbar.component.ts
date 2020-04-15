import { Component, OnInit, HostListener } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import {AuthService} from '../_services/auth.service';
import { ProfileService } from '../_services/profile.service';
import { Rights } from "../_models/user";
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import {LoginDialog} from '../login/loginDialog.component'

@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss']
})
export class TopbarComponent implements OnInit {
  isHomepage:boolean = true;
  isLoggedIn:boolean;
  isAdmin:boolean;
  email:string;
  
  constructor(
    private snackBar: MatSnackBar,
    private router: Router,
    public authService: AuthService,
    private profileService: ProfileService,
    public dialog: MatDialog,
  ) { }

  ngOnInit() {
    if(this.router.url.includes('about'))
      this.isHomepage = false;
    
      this.authService.getRole().toPromise().then(rights => {
        if (rights) {
          this.isLoggedIn = true;
  
          if (rights == Rights.user) {
            this.profileService.getUser().then(user => {
              this.email = user.email;
              this.isAdmin = false;
            });
          }
          else if (rights = Rights.admin) {
            this.profileService.getAdmin().then(admin => {
              this.email = admin.email;
              this.isAdmin = true;
            })
          }
        }
      });

  }

  doToggleAbout():void{
    if(this.isHomepage){
      this.router.navigateByUrl("/about");
    }
    else{
      this.router.navigateByUrl("");
    }
    this.isHomepage = !this.isHomepage;
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(LoginDialog, {
      width: '250px',
      data: { email: "", password: "" }
    });

    dialogRef.afterClosed().subscribe(data => {
      this.authService.isAuthenticated().toPromise().then(response => {
        if (response) {
          this.isLoggedIn = true;
          this.email = data;
        }
      });
    });
  }
  logout() {
    this.openSnackBar("You are now logged out", "OK");
    localStorage.clear();
    this.isLoggedIn = false;
    this.isAdmin = false;
  }

  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: 2000,
    });
  }
}
