import { Component, HostBinding, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { IMediaStream } from '../_services/streamMessage.service'
import { CameraService } from '../_services/camera.service'
import { CameraDialog } from "../add-camera/add-camera.component";
import { MatDialog } from "@angular/material/dialog";
import { ShareStreamComponent } from "../share-stream/share-stream.component";
import { AuthService } from "../_services/auth.service";
import { ModelChangerComponent } from '../model-changer/model-changer.component';

@Component({
  selector: 'app-menu-list-item',
  templateUrl: './menu-list-item.component.html',
  styleUrls: ['./menu-list-item.component.scss'],
  animations: [
    trigger('indicatorRotate', [
      state('collapsed', style({ transform: 'rotate(0deg)' })),
      state('expanded', style({ transform: 'rotate(180deg)' })),
      transition('expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4,0.0,0.2,1)')
      ),
    ])
  ]
})
export class MenuListItemComponent implements OnInit {
  expanded: boolean;
  admin: boolean;
  @HostBinding("attr.aria-expanded") ariaExpanded = this.expanded;
  @Input() item: IMediaStream;
  @Input() isRecording: Boolean;
  @Output() changeStream: EventEmitter<IMediaStream> = new EventEmitter<IMediaStream>();


  constructor(
    public dialog: MatDialog,
    public cameraService: CameraService,
    public authService: AuthService
  ) {

  }

  ngOnInit() {
    this.authService.isAuthenticatedAdmin().toPromise().then(
      (data) => {
        this.admin = data;
      },
      (error) => { }
    );
  }



  onItemSelected() {
    this.expanded = !this.expanded;
  }

  public streamClick() {
    this.changeStream.emit(this.item);
  }

  async delete() {
    if (confirm("Are you sure to delete " + this.item.label)) {
      await this.cameraService.deleteCamera(this.item);
      window.location.reload();
    }
  }

  async edit() {
    let data = await this.cameraService.getCamera(this.item);
    this.dialog.open(CameraDialog, { data: data });
  }

  async share() {
    this.dialog.open(ShareStreamComponent, {
      data: { camera_id: this.item.camera_id, email: "" },
    });
  }

  async change() {
    this.dialog.open(ModelChangerComponent, {
      data: { camera_id: this.item.camera_id },
    });
  }
}
