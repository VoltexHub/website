export default async function handler(req, res) {
  const q = req.query.q || "";
  if (!q) {
    res.status(400).send("Missing query");
    return;
  }

  const url = `https://duckduckgo.com/html/?q=${encodeURIComponent(q)}`;

  try {
    // Use native fetch
    const r = await fetch(url, {
      headers: {
        "User-Agent": "Mozilla/5.0"
      }
    });

    const html = await r.text();

    res.setHeader("Content-Type", "text/html");
    res.status(200).send(html);

  } catch (err) {
    console.error(err);
    res.status(500).send("Backend error");
  }
}
