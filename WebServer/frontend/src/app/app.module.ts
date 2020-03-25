import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from "@angular/forms";
import { AppRoutingModule } from './app-routing.module';
import { HomepageComponent } from './homepage/homepage.component';
import { LoginComponent } from './login/login.component';
import { VideoplayerComponent } from './videoplayer/videoplayer.component';
import { VgCoreModule, VgControlsModule, VgStreamingModule, VgOverlayPlayModule, VgBufferingModule} from 'ngx-videogular';
import { RecordService } from './_services/record.service';
import { HttpClientModule } from "@angular/common/http";

@NgModule({
  declarations: [
    HomepageComponent,
    LoginComponent,
    VideoplayerComponent
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
    HttpClientModule
  ],
  providers: [
    RecordService
  ],
  bootstrap: [HomepageComponent]
})
export class AppModule { }
