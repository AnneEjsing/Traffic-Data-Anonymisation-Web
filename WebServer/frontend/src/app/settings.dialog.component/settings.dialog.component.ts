import { Component } from "@angular/core";
import { MatDialogRef } from '@angular/material/dialog';
import { VideoService } from '../_services/video.service';
import { FormControl } from '@angular/forms';
import { videoSettings } from '../_models/video';

@Component({
    selector: 'settings-dialog',
    templateUrl: './settings.dialog.component.html',
    styleUrls: ['./settings.dialog.component.scss'],
})

export class SettingsDialog {
    settings: videoSettings;
    error: boolean;
    ctrl = new FormControl('', (control: FormControl) => {
        const value = control.value;

        if (!value) {
            return null;
        }

        return null;
    });

    constructor(
        public dialogRef: MatDialogRef<SettingsDialog>,
        public videoService: VideoService,
    ) {
        this.videoService.getSettings().then(settings => {
            this.settings = settings;
            var secounds = settings.recording_limit;
            this.ctrl.setValue({
                hour: Math.floor(secounds / 3600),
                minute: Math.floor(secounds % 3600 / 60),
                second: Math.floor(secounds % 3600 % 60)
            });
        });
    }

    onClose(): void {
        this.dialogRef.close();
    }

    days_change(event) {
        this.settings.keep_days = event.srcElement.valueAsNumber;
    }

    updateSettings() {
        this.settings.recording_limit = (((this.ctrl.value.hour * 60) + this.ctrl.value.minute) * 60) + this.ctrl.value.second;
        this.videoService.updateSettings(this.settings).then(response => {
            this.dialogRef.close(this.settings);
        }).catch(error => {
            this.error = true;
        });
    }
}