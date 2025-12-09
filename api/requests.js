// /api/requests.js
export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const body = await new Promise((resolve, reject) => {
            let data = '';
            req.on('data', chunk => data += chunk);
            req.on('end', () => resolve(JSON.parse(data)));
            req.on('error', err => reject(err));
        });

        const { placeId, features, amount } = body;

        if (!placeId || !features) {
            return res.status(400).json({ error: 'Missing fields' });
        }

        const webhookUrl = process.env.DISCORD_WEBHOOK || 
            "https://discord.com/api/webhooks/1414766856308260874/V4JwhFOEO_0a0XW1Ulr8cGLsQlQc2r1tTkd4_XDHi1HzQaFPiLET4oyXm_Dgwn6Uvp5U";

        await fetch(webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                embeds: [{
                    title: 'Script Request',
                    color: 0x00eeff,
                    fields: [
                        { name: 'Features', value: features, inline: false },
                        { name: 'Place ID', value: placeId, inline: true },
                        { name: 'Amount', value: amount + '$', inline: true }
                    ],
                    timestamp: new Date().toISOString()
                }]
            })
        });

        return res.status(200).json({ status: 'ok' });

    } catch (err) {
        console.error(err);
        return res.status(500).json({ error: 'Backend error' });
    }
}
