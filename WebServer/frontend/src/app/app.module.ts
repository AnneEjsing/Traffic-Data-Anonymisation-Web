import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from "@angular/forms";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { HomepageComponent } from './homepage/homepage.component';
import { LoginComponent } from './login/login.component';
import { VideoplayerComponent } from './videoplayer/videoplayer.component';
import { VgCoreModule, VgControlsModule, VgStreamingModule, VgOverlayPlayModule, VgBufferingModule } from 'ngx-videogular';
import { ProfileService } from './_services/profile.service';
import { HttpClientModule } from "@angular/common/http";
import { RecordService } from './_services/record.service';
import { SidemenuComponent } from './sidemenu/sidemenu.component';
import { StreamMessageService } from './_services/streamMessage.service';
import { AppComponent } from './app.component';
import { DemoMaterialModule } from './material-module';
import { LoginDialog } from "./login/loginDialog.component";
import { MatDialogModule } from '@angular/material/dialog';
import { LoginService } from './_services/login.service';

@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    LoginComponent,
    VideoplayerComponent,
    HomepageComponent,
    SidemenuComponent,
    LoginDialog
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    DemoMaterialModule,
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
    LoginService,
    RecordService,
    StreamMessageService,
  ],
  bootstrap: [
    HomepageComponent,
    MatDialogModule, //IDK why this needs to be explicit imported when part of DemoMatherialModule, the rest does not
    AppComponent,
  ],
})
export class AppModule { }
