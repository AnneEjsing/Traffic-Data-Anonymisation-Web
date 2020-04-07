import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component'

const routes: Routes = [
  {
    path: "",
    children: [
      { path: "", component: HomepageComponent },
    ]
  },
  { path: "**", redirectTo: "" }
];



@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
