// /api/request.js
import fetch from 'node-fetch';

export default async function handler(req, res){
    if(req.method !== 'POST') return res.status(405).send('Method not allowed');

    const { placeId, features, amount } = req.body;
    if(!placeId || !features) return res.status(400).send('Missing fields');

    const webhookUrl = process.env.DISCORD_WEBHOOK; // store safely in Vercel environment

    try {
        await fetch(webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                embeds: [{
                    title: 'New Script Request',
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

        res.status(200).send('OK');
    } catch(e){
        res.status(500).send('Backend error');
    }
}
