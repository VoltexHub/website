import express from "express";
import fetch from "node-fetch";
const app = express();

// Proxy DDG HTML results
app.get("/search", async (req, res) => {
    const q = req.query.q || "";
    const url = `https://duckduckgo.com/html/?q=${encodeURIComponent(q)}`;

    try {
        const r = await fetch(url, {
            headers: {
                "User-Agent": "Mozilla/5.0",
            }
        });

        const html = await r.text();
        res.send(html);
    } catch (err) {
        res.status(500).send("Backend error.");
    }
});

app.listen(3000, () => console.log("Backend running on port 3000"));
