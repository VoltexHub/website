export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).send({ error: 'Method not allowed' });
  }

  try {
    const { placeId, features, amount } = req.body;

    if (!placeId || !features) {
      return res.status(400).send({ error: 'Place ID and Features are required' });
    }

    // Discord webhook (keep secret here!)
    const webhookUrl = process.env.DISCORD_WEBHOOK;

    await fetch(webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        embeds: [
          {
            title: "New Request",
            color: 0x00eeff,
            fields: [
              { name: "Features", value: features, inline: false },
              { name: "Place ID", value: placeId, inline: true },
              { name: "Amount", value: amount + "$", inline: true }
            ],
            timestamp: new Date().toISOString()
          }
        ]
      })
    });

    res.status(200).send({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).send({ error: 'Failed to send request' });
  }
}
