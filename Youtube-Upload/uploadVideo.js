// uploadVideo.js

const fs = require("fs");
const { google } = require("googleapis");
const progressStream = require("progress-stream");
const service = google.youtube("v3");
const path = require("path");
const {title,description,tags} = require("../Youtube-Upload/shared");

const uploadVideo = (auth) => {
  const videoPath = path.join(__dirname, "../encoded_video.mp4");
  const fileSize = fs.statSync(videoPath).size;

  const progress = progressStream({
    length: fileSize,
    time: 500,
  });

  progress.on("progress", (progress) => {
    const percentage = Math.floor(progress.percentage);
    process.stdout.clearLine();
    process.stdout.cursorTo(0);
    process.stdout.write(`Uploading: ${percentage}%`);
  });

  const media = {
    body: fs.createReadStream(videoPath).pipe(progress),
  };

  service.videos.insert(
    {
      auth: auth,
      part: "snippet,contentDetails,status",
      resource: {
        snippet: {
          title: title,
          description: description,
          tags: tags,
        },
        status: {
          privacyStatus: "private",
        },
      },
      media: media,
    },
    (error, data) => {
      if (error) {
        console.error("Error uploading video:", error);
        return;
      }
      console.log("\nVideo uploaded successfully. Video ID: " + data.data.id);
      console.log(
        "You can view the video at: https://www.youtube.com/watch?v=" +
          data.data.id
      );
    }
  );
};

module.exports = uploadVideo;
