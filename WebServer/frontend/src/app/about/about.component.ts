import { Component, OnInit } from '@angular/core';
import { projectTitle } from '../app.component';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss']
})
export class AboutComponent implements OnInit {
  title = projectTitle;
  
  constructor() { }

  ngOnInit() {
  }

}
