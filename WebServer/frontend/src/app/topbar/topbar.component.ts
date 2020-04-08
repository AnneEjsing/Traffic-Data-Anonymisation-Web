import { Component, OnInit, HostListener } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';


@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss']
})
export class TopbarComponent implements OnInit {

  constructor(
    private snackBar: MatSnackBar,
    private router: Router,
  ) { }

  ngOnInit() {
  }

  // @HostListener('window:scroll', ['$event'])

  // onWindowScroll(e) {
  //   let element = document.querySelector('.navbar');
  //   if (window.pageYOffset > element.clientHeight) {
  //     this.isScrolled = true;
  //     element.classList.add('navbar-inverse');
  //   } else {
  //     this.isScrolled = false;
  //     element.classList.remove('navbar-inverse');
  //   }
  // }
}
