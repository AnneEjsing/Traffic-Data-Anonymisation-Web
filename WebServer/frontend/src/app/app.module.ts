import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
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
import { JwtHelperService, JWT_OPTIONS } from '@auth0/angular-jwt';
import { AuthService } from './_services/auth.service';
import { VideoService } from './_services/video.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    LoginComponent,
    VideoplayerComponent,
    SidemenuComponent,
    LoginDialog,
  ],
  imports: [
    MatDialogModule, //IDK why this needs to be explicit imported when part of DemoMatherialModule, the rest does not
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    DemoMaterialModule,
    AppRoutingModule,
    VgCoreModule,
    VgControlsModule,
    VgOverlayPlayModule,
    VgBufferingModule,
    VgStreamingModule,
    HttpClientModule,
    NgbModule,
  ],
  providers: [
    ProfileService,
    LoginService,
    RecordService,
    StreamMessageService,
    JwtHelperService,
    AuthService,
    VideoService,
    { provide: JWT_OPTIONS, useValue: JWT_OPTIONS },
  ],
  bootstrap: [
    AppComponent,
  ],
})
export class AppModule { }
