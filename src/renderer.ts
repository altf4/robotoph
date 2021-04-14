// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process unless
// nodeIntegration is set to true in webPreferences.
// Use preload.js to selectively enable features
// needed in the renderer process.
// import { Howl } from 'howler';
// const {Howl, Howler} = require('howler');

declare var Howl: any;

const testButton = document.getElementById("testbutton");
if (testButton !== null) {
  console.log("here");
  testButton.onclick = playAudio;
}

async function playAudio() {
  console.log("nice");
  window.postMessage("WOOOOO", '*');

  var sound = new Howl({
    src: ["clips/character_specific/marth/monster_tipper/monster_tipper.ogg"],
    onend: function() {
      console.log('Finished!');
    },
    onplayerror: function() {
      console.log('Play error!');
    },
    onloaderror: function(id: any, error: any) {
      console.log('Load error!' + id + ": " + error);
    }
  });
  sound.play();
}

playAudio()
