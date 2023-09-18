const ytdl = require("ytdl-core");
const fs = require("fs");
const path = require("path");

function downloadPrivateVideo(auth, videoUrl, outputDir) {
  if (!videoUrl || !outputDir) {
    console.error("Invalid video URL or output directory.");
    return;
  }
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
  }
  ytdl.getInfo(videoUrl, { auth: auth }, (err, info) => {
    if (err) {
      console.error("Error fetching video info:", err);
      return;
    }

    const videoId = info.video_id;
    const videoFilePath = path.join(outputDir, `${videoId}.mp4`);

    const videoStream = ytdl(videoUrl, { quality: "highest", auth: auth });

    videoStream
      .pipe(fs.createWriteStream(videoFilePath))
      .on("finish", () => {
        console.log(`Video downloaded and saved to: ${videoFilePath}`);
      })
      .on("error", (error) => {
        console.error("Error downloading video:", error);
      });
  });
}

module.exports = downloadPrivateVideo;