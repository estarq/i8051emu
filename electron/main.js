const { app, BrowserWindow } = require('electron/main');
const server = require('./server');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 750
  });

  mainWindow.loadURL('http://localhost:3000');
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', createWindow);

app.on('resize', (e, x, y) => {
  mainWindow.setSize(x, y);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin')
    app.quit();
});

app.on('activate', () => {
  if (mainWindow === null)
    createWindow();
});
