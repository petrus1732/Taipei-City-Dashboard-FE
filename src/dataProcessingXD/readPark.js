const data = require("./data.json");
const fs = require("fs");
console.log(data);
fs.writeFile("parsed2.json", JSON.stringify(data, null, "\t"));