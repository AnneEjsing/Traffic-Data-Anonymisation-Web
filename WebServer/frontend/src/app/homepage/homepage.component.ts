import { Component, OnInit } from '@angular/core';
import { user } from '../_models/user';
import { ProfileService } from '../_services/profile.service';
import { LoginService } from '../_services/login.service';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent implements OnInit {
  userList: string;

  constructor(
    private profileService: ProfileService,
    private loginService: LoginService,
  ) { }

  ngOnInit(): void {

  }

  listUsers() {
    this.profileService.listUsers().then(users => {
      console.log(users);
      this.userList = users;
    }).catch(error => {
      this.userList = "An error occurred";
      console.log("An error occurred");
    });
  }

  signup() {
    this.profileService.signupUser('great@email.com', '1234').then(x => {
      console.log(x);
    }).catch(error => {
      console.log("Error");
      console.log(error);
    });
  }

  login() {
    this.loginService.login('casper', '1234').then(x => {
      console.log(x);
    }).catch(error => {
      console.log(error);
    })
  }
}
