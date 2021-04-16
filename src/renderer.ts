// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process unless
// nodeIntegration is set to true in webPreferences.
// Use preload.js to selectively enable features
// needed in the renderer process.

declare var Howl: any;

// Are we in the middle of playing a clip now?
var playingClip = false;

window.addEventListener("message", (event) => {
  playClip(event.data.toString());
});

async function playClip(clip: string) {
  if (!playingClip) {
    console.log("Playing clip: " + clip);
    var sound = new Howl({
      src: [clip],
      onend: function() {
        console.log('Finished clip');
        playingClip = false;
      },
      onplayerror: function() {
        console.log('Play error! ');
        playingClip = false;
      },
      onloaderror: function(id: any, error: any) {
        console.log('Load error! ' + id + ": " + error);
        playingClip = false;
      }
    });
    playingClip = true;
    sound.play();
  }
}
