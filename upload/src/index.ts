import Repo from "./repo.js";
import fs from "fs";
import path from "path";

const repo = new Repo("cch137", "113-recordings");

(async () => {
  const assets = fs.readdirSync("../assets");

  for (const asset of assets) {
    const [subject, ..._name] = asset.split(" ");
    const gitFp = `assets/${subject}/${_name.join(" ")}`;
    const fsFp = path.resolve("../assets", asset);
    console.log("uploading...", gitFp);
    await repo.upload(gitFp, fs.readFileSync(fsFp));
    await new Promise((r) => setTimeout(r, 10000));
    throw new Error("stop");
  }

  console.log("DONE");
})();
