// /api/request.js
import fetch from 'node-fetch';

export default async function handler(req, res){
    if(req.method !== 'POST') return res.status(405).send('Method not allowed');

    const { placeId, features, amount } = req.body;
    if(!placeId || !features) return res.status(400).send('Missing fields');

    const webhookUrl = "https://discord.com/api/webhooks/1414766856308260874/V4JwhFOEO_0a0XW1Ulr8cGLsQlQc2r1tTkd4_XDHi1HzQaFPiLET4oyXm_Dgwn6Uvp5U"

    try {
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

        res.status(200).send('OK');
    } catch(e){
        res.status(500).send('Backend error');
    }
}
