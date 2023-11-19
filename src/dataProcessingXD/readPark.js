import fs from "fs";

import data from "./park.json" assert { type: "json" };

console.log(data);

fs.writeFile("parkData.json", JSON.stringify(data, null, "\t"), (err) => {
  if (err) {
    console.error("Error writing file:", err);
  } else {
    console.log("File 'parkData.json' has been written successfully.");
  }
});
