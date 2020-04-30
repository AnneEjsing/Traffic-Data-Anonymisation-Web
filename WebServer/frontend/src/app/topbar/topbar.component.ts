import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from '../_services/auth.service';
import { ProfileService } from '../_services/profile.service';
import { MatDialog } from '@angular/material/dialog';
import { LoginDialog } from '../login/loginDialog.component'

@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss']
})
export class TopbarComponent implements OnInit {
  isHomepage: boolean = true;
  isLoggedIn: boolean;
  isAdmin: boolean;
  public email: string;

  constructor(
    private snackBar: MatSnackBar,
    private router: Router,
    public authService: AuthService,
    private profileService: ProfileService,
    public dialog: MatDialog,
  ) { }

  ngOnInit() {
    if (this.router.url.includes('about'))
      this.isHomepage = false;

    if (localStorage.getItem('session_token')) {
      this.profileService.getUser().then(user => {
        this.isLoggedIn = true;
        this.email = user.email;
        this.isAdmin = user.rights == "admin";
      });
    }
  }

  doToggleAbout(): void {
    if (this.isHomepage) {
      this.router.navigateByUrl("/about");
    }
    else {
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
          window.location.reload();
        }
      });
    });
  }
  logout() {
    this.openSnackBar("You are now logged out", "OK");
    localStorage.clear();
    this.isLoggedIn = false;
    this.isAdmin = false;
    window.location.reload();
  }

  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: 2000,
    });
  }
}
