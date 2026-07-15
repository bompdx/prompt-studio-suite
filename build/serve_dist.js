// Tiny static server for dist/, used only for local verification.
const http = require("http");
const fs = require("fs");
const path = require("path");
const ROOT = path.join(__dirname, "..", "dist");
const TYPES = { ".html": "text/html", ".json": "application/json" };
http.createServer((req, res) => {
  const urlPath = decodeURIComponent(req.url.split("?")[0]);
  let file = path.join(ROOT, urlPath === "/" ? "index.html" : urlPath);
  if (!file.startsWith(ROOT)) { res.writeHead(403); res.end(); return; }
  fs.readFile(file, (err, data) => {
    if (err) {
      if (urlPath === "/") {
        fs.readdir(ROOT, (e2, names) => {
          const links = (names || []).map(n => `<li><a href="/${n}">${n}</a></li>`).join("");
          res.writeHead(200, { "Content-Type": "text/html" });
          res.end(`<ul>${links}</ul>`);
        });
        return;
      }
      res.writeHead(404); res.end("not found"); return;
    }
    res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "text/plain" });
    res.end(data);
  });
}).listen(8741);
console.log("serving dist on http://localhost:8741");
