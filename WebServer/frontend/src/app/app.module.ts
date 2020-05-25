import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { HomepageComponent } from './homepage/homepage.component';
import { VideoplayerComponent } from './videoplayer/videoplayer.component';
import { VgCoreModule, VgControlsModule, VgStreamingModule, VgOverlayPlayModule, VgBufferingModule } from 'ngx-videogular';
import { ProfileService } from './_services/profile.service';
import { HttpClientModule } from "@angular/common/http";
import { HttpModule } from '@angular/http';
import { RecordService } from './_services/record.service';
import { SidemenuComponent } from './sidemenu/sidemenu.component';
import { StreamMessageService } from './_services/streamMessage.service';
import { VideoUtilsComponent } from './video-utils/video-utils.component';
import { AppComponent } from './app.component';
import { DemoMaterialModule } from './material-module';
import { LoginDialog } from "./login/loginDialog.component";
import { MatDialogModule } from '@angular/material/dialog';
import { LoginService } from './_services/login.service';
import { JwtHelperService, JWT_OPTIONS } from '@auth0/angular-jwt';
import { AuthService } from './_services/auth.service';
import { VideoService } from './_services/video.service';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { TopbarComponent } from './topbar/topbar.component';
import { AboutComponent } from './about/about.component';
import { CameraDialog } from './add-camera/add-camera.component';
import { CameraService } from './_services/camera.service'
import { MenuListItemComponent } from './menu-list-item/menu-list-item.component';
import { ShareStreamComponent } from './share-stream/share-stream.component';
import { ModelChangerComponent } from './model-changer/model-changer.component'
import { SettingsDialog } from './settings.dialog.component/settings.dialog.component';

@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    VideoplayerComponent,
    SidemenuComponent,
    VideoUtilsComponent,
    LoginDialog,
    SettingsDialog,
    TopbarComponent,
    AboutComponent,
    CameraDialog,
    MenuListItemComponent,
    ShareStreamComponent,
    ModelChangerComponent
  ],
  imports: [
    MatDialogModule,
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
    HttpModule
  ],
  providers: [
    ProfileService,
    LoginService,
    RecordService,
    StreamMessageService,
    JwtHelperService,
    AuthService,
    VideoService,
    CameraService,
    { provide: JWT_OPTIONS, useValue: JWT_OPTIONS },
  ],
  bootstrap: [
    AppComponent,
  ],
})
export class AppModule { }
