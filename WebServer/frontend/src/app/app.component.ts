import { Component } from '@angular/core';

export const projectTitle = 'ICU';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = projectTitle;
}
