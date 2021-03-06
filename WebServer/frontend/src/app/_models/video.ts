export class videoSettings {
    recording_limit: number;
    keep_days: number;
}

export class recording_info {
    camera_id: string;
    user_id: string;
    start_time: Date;
    recording_time: number;
    recording_intervals: number;
}

export class recorded_video {
    label: string;
    video_id: string;
    save_time: Date;
    camera_id: string;
}
