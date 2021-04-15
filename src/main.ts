import { app, BrowserWindow } from "electron";
import * as path from "path";
const { ipcMain } = require('electron');
import { DolphinConnection, Ports, ConnectionEvent, ConnectionStatus } from '@slippi/slippi-js';

var dolphinConnection = new DolphinConnection();
var mainWindow: any = null

function playClip(clip: string) {
  mainWindow.webContents.send('play-clip', clip);
}

dolphinConnection.on(ConnectionEvent.STATUS_CHANGE, status => {
  // Disconnect from Slippi server when we disconnect from Dolphin
  if (status === ConnectionStatus.DISCONNECTED) {
    mainWindow.webContents.send('disconnected-event', 'disconnected');
  }
  if (status === ConnectionStatus.CONNECTED) {
    mainWindow.webContents.send('connected-event', 'connected');
    playClip('clips/combos/big/huge_damage.ogg');
  }
});

dolphinConnection.on(ConnectionEvent.MESSAGE, (message) => {
  // this._handleGameData();
});

dolphinConnection.on(ConnectionEvent.ERROR, (err) => {
  // Log the error messages we get from Dolphin
  console.log("Dolphin connection error", err);
});

function createWindow() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      worldSafeExecuteJavaScript: true,
      contextIsolation: true,
    },
    width: 800,
  });

  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, "../index.html"));

  // Open the DevTools.
  mainWindow.webContents.openDevTools();

  mainWindow.webContents.once('dom-ready', () => {
    // Make the disconnected label appear first
    mainWindow.webContents.send('disconnected-event', 'disconnected');
    if (dolphinConnection.getStatus() === ConnectionStatus.DISCONNECTED)
    {
      // Now try connect to our local Dolphin instance
      dolphinConnection.connect(
        '127.0.0.1',
        Ports.DEFAULT
      );
    }
  });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", () => {
  createWindow();

  app.on("activate", function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

// In this file you can include the rest of your app"s specific main process
// code. You can also put them in separate files and require them here.
ipcMain.on('ipc', (event, arg) => {
  // Command to connect to Dolphin
  if (arg === "connectDolphin") {
    if (dolphinConnection.getStatus() === ConnectionStatus.DISCONNECTED)
    {
      // Now try connect to our local Dolphin instance
      dolphinConnection.connect(
        '127.0.0.1',
        Ports.DEFAULT
      );
    }
  }
})
