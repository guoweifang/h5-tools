export enum AudioKeys {
    bgm = 'bgm/bgm',
    knocking_an_iron_door1 = 'sfx/knocking_an_iron_door1',
}

export const audioSettings: IAudioSetting[] = [
    { loaderName: 'test', path: AudioKeys.bgm, group: 'bgm' },
    { loaderName: 'test', path: AudioKeys.knocking_an_iron_door1, group: 'sfx' },
];
