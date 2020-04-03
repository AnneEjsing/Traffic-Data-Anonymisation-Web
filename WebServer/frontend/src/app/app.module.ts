import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from "@angular/forms";

import { AppRoutingModule } from './app-routing.module';
import { HomepageComponent } from './homepage/homepage.component';
import { LoginComponent } from './login/login.component';
import { VideoplayerComponent } from './videoplayer/videoplayer.component';
import { VgCoreModule, VgControlsModule, VgStreamingModule, VgOverlayPlayModule, VgBufferingModule } from 'ngx-videogular';
import { ProfileService } from './_services/profile.service';
import { HttpClientModule } from "@angular/common/http";
import { LoginService } from './_services/login.service';

@NgModule({
  declarations: [
    HomepageComponent,
    LoginComponent,
    VideoplayerComponent,
    HomepageComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    VgCoreModule,
    VgControlsModule,
    VgOverlayPlayModule,
    VgBufferingModule,
    VgStreamingModule,
    HttpClientModule,
  ],
  providers: [
    ProfileService,
    LoginService
  ],
  bootstrap: [HomepageComponent]
})
export class AppModule { }
