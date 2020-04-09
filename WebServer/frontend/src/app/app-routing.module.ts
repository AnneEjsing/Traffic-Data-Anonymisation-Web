import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component'
import { LoginComponent } from './login/login.component'
import { AboutComponent } from './about/about.component';

const routes: Routes = [
  {
    path: "",
    children: [
      { path: "", component: HomepageComponent },
      { path: "login", component: LoginComponent },
      { path: "about", component: AboutComponent },
    ]
  },
  { path: "**", redirectTo: "" }
];



@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
