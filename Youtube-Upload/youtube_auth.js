const fs = require("fs");
const readline = require("readline");
const { google } = require("googleapis");
const OAuth2 = google.auth.OAuth2;
const uploadVideo = require("./uploadVideo");
const path = require("path");
const ytdl = require("ytdl-core");

var SCOPES = [
  "https://www.googleapis.com/auth/youtube.readonly",
  "https://www.googleapis.com/auth/youtube.upload",
  "https://www.googleapis.com/auth/youtube.force-ssl"
];

const str_checker = process.argv[2];

const TOKEN_DIR =
  (process.env.HOME || process.env.HOMEPATH || process.env.USERPROFILE) +
  "/.credentials/";
const TOKEN_PATH = TOKEN_DIR + "youtube-nodejs-quickstart.json";

const CLIENT_SECRETS_PATH = path.join(__dirname, "../client_secret.json");

// Load client secrets from a local file.
fs.readFile(CLIENT_SECRETS_PATH, function processClientSecrets(err, content) {
  if (err) {
    console.log("Error loading client secret file: " + err);
    return;
  }
  authorize(JSON.parse(content), handleAuthorization);
});

function authorize(credentials, callback) {
  const clientSecret = credentials.web.client_secret;
  const clientId = credentials.web.client_id;
  const redirectUrl = credentials.web.redirect_uris[0];
  const oauth2Client = new OAuth2(clientId, clientSecret, redirectUrl);

  fs.readFile(TOKEN_PATH, function (err, token) {
    if (err) {
      getNewToken(oauth2Client, callback);
    } else {
      oauth2Client.credentials = JSON.parse(token);
      callback(oauth2Client);
    }
  });
}

function getNewToken(oauth2Client, callback) {
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: "offline",
    scope: SCOPES,
  });
  console.log("Authorize this app by visiting this url: ", authUrl);
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  rl.question("Enter the code from that page here: ", function (code) {
    rl.close();
    oauth2Client.getToken(code, function (err, token) {
      if (err) {
        console.log("Error while trying to retrieve access token", err);
        return;
      }
      oauth2Client.credentials = token;
      storeToken(token);
      callback(oauth2Client);
    });
  });
}

function storeToken(token) {
  try {
    fs.mkdirSync(TOKEN_DIR);
  } catch (err) {
    if (err.code != "EEXIST") {
      throw err;
    }
  }
  fs.writeFile(TOKEN_PATH, JSON.stringify(token), (err) => {
    if (err) throw err;
    console.log("Token stored to " + TOKEN_PATH);
  });
}

function handleAuthorization(auth) {
  if (str_checker === "1") {
    listAndDownloadVideos(auth);
  } else {
    uploadVideo(auth);
  }
}

function listAndDownloadVideos(auth) {
  const service = google.youtube("v3");

  // List the user's videos
  service.channels.list(
    {
      auth: auth,
      part: "contentDetails",
      mine: true,
    },
    function (err, response) {
      if (err) {
        console.log("The API returned an error: " + err);
        return;
      }
      const channels = response.data.items;
      if (channels.length == 0) {
        console.log("No channel found.");
      } else {
        const uploadPlaylistId = channels[0].contentDetails.relatedPlaylists.uploads;

        // List videos in the user's uploads playlist
        service.playlistItems.list(
          {
            auth: auth,
            part: "snippet",
            playlistId: uploadPlaylistId,
            maxResults: 50, // You can adjust the number of videos to retrieve
          },
          function (err, response) {
            if (err) {
              console.log("The API returned an error: " + err);
              return;
            }
            const videos = response.data.items;
            if (videos.length == 0) {
              console.log("No videos found in the uploads playlist.");
            } else {
              console.log("List of uploaded videos:");

              // Display video titles and provide the option to download
              videos.forEach((video, index) => {
                console.log(`${index + 1}. ${video.snippet.title}`);
                console.log(`   Video ID: ${video.snippet.resourceId.videoId}`);
                const downloadOption = `Download (Press ${index + 1})`;
                console.log(`   ${downloadOption}`);
              });

              // Prompt the user for video download choice
              const rl = readline.createInterface({
                input: process.stdin,
                output: process.stdout,
              });
              rl.question("Enter the number of the video to download: ", (choice) => {
                rl.close();
                const videoIndex = parseInt(choice) - 1;
                if (isNaN(videoIndex) || videoIndex < 0 || videoIndex >= videos.length) {
                  console.log("Invalid choice. Please enter a valid number.");
                } else {
                  const selectedVideo = videos[videoIndex];
                  const videoId = selectedVideo.snippet.resourceId.videoId;

                  // Call the download function with videoId and downloadDir
                  downloadPrivateVideo(auth, `https://www.youtube.com/watch?v=${videoId}`);
                }
              });
            }
          }
        );
      }
    }
  );
}

function downloadPrivateVideo(auth, videoUrl) {
  if (!videoUrl) {
    console.error("Invalid video URL.");
    return;
  }
  const downloadDir = path.join(__dirname,"downloads");

  const videoId = ytdl.getURLVideoID(videoUrl);
  const videoFilePath = path.join(downloadDir, `${videoId}.mp4`);

  // Use the provided auth object for authorization
  const oauth2Client = auth;

  // Create a YouTube Data API client
  const service = google.youtube("v3");

  // Check if the video is private
  service.videos.list(
    {
      auth: oauth2Client,
      part: "status",
      id: videoId,
    },
    function (err, response) {
      if (err) {
        console.error("Error checking video status:", err);
        return;
      }

      if (response.data.items.length === 0) {
        console.error("Video not found.");
        return;
      }

      const videoStatus = response.data.items[0].status;
      if (videoStatus.privacyStatus === "private") {
        console.error("This is a private video. You do not have access to it.");
        return;
      }

      // The video is not private, proceed with downloading
      const videoStream = ytdl(videoUrl, { quality: "highest" });

      videoStream
        .pipe(fs.createWriteStream(videoFilePath))
        .on("finish", () => {
          console.log(`Video downloaded and saved to: ${videoFilePath}`);
        })
        .on("error", (error) => {
          console.error("Error downloading video:", error);
        });
    }
  );
}
