// All of the Node.js APIs are available in the preload process.
// It has the same sandbox as a Chrome extension.
const { ipcRenderer } = require('electron');

window.addEventListener("DOMContentLoaded", () => {
  const replaceText = (selector: string, text: string) => {
    const element = document.getElementById(selector);
    if (element) {
      element.innerText = text;
    }
  };
});

ipcRenderer.on('disconnected-event', (event, ...args) => {
  document.getElementById("connected-label").style.visibility= 'hidden';
  document.getElementById("disconnected-label").style.visibility= 'visible';

});

ipcRenderer.on('connected-event', (event, ...args) => {
  document.getElementById("connected-label").style.visibility= 'visible';
  document.getElementById("disconnected-label").style.visibility= 'hidden';
});

ipcRenderer.on('play-clip', (event, ...args) => {
  window.postMessage(args, "file://");
});
