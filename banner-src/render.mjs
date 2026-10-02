import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import satori from 'satori'
import { html } from 'satori-html'
import sharp from 'sharp'

const here = path.dirname(fileURLToPath(import.meta.url))
const out = path.resolve(here, '../assets/banner.svg')
const photoSource = '/Users/jordy/projects/portfolio/src/assets/images/jordy.webp'

const WIDTH = 1200
const HEIGHT = 480
const PHOTO_HEIGHT = 455

const photo = await sharp(photoSource)
  .extract({ left: 0, top: 0, width: 1200, height: 1290 })
  .resize({ height: Math.round(PHOTO_HEIGHT * 1.6) })
  .png({ compressionLevel: 9, palette: true, quality: 80 })
  .toBuffer()
const photoMeta = await sharp(photo).metadata()
const photoWidth = Math.round((photoMeta.width / photoMeta.height) * PHOTO_HEIGHT)
const photoUri = `data:image/png;base64,${photo.toString('base64')}`

const trendingUp = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/></svg>`
const dot = `<div style="display:flex;width:8px;height:8px;border-radius:9999px;background:#14b8a6;margin-right:10px"></div>`
const divider = `<div style="display:flex;width:1px;height:22px;background:#374151;margin:0 13px"></div>`

const markup = html(`
<div style="display:flex;width:${WIDTH}px;height:${HEIGHT}px;position:relative;font-family:'DM Sans';background:linear-gradient(135deg,#111827 0%,#030712 55%,#000000 100%);border-radius:24px;overflow:hidden">
  <div style="display:flex;position:absolute;top:0;left:0;width:${WIDTH}px;height:${HEIGHT}px;background:radial-gradient(circle at 100% 0%, rgba(20,184,166,0.10) 0%, rgba(20,184,166,0) 38%)"></div>
  <div style="display:flex;position:absolute;top:0;left:0;width:${WIDTH}px;height:${HEIGHT}px;background:radial-gradient(circle at 0% 100%, rgba(59,130,246,0.10) 0%, rgba(59,130,246,0) 38%)"></div>

  <div style="display:flex;flex-direction:column;justify-content:center;padding:0 0 0 64px;width:${WIDTH - photoWidth - 24}px;height:${HEIGHT}px">
    <div style="display:flex;font-size:68px;font-weight:600;color:#f3f4f6;letter-spacing:-1.5px;line-height:1">Jordy van Vorselen</div>
    <div style="display:flex;font-size:32px;font-weight:300;color:#d1d5db;margin-top:14px">Freelance Lead Engineer</div>

    <div style="display:flex;flex-wrap:wrap;font-size:21px;color:#d1d5db;margin-top:34px;line-height:1.55">
      <span style="margin-right:6px">I make software teams</span><span style="font-weight:700;color:#ffffff">ship faster</span><span>. Measured, not vibes.</span>
    </div>
    <div style="display:flex;flex-wrap:wrap;font-size:21px;color:#d1d5db;line-height:1.55">
      <span style="margin-right:6px">Ten years in teams building</span><span style="font-weight:700;color:#ffffff">mission-critical software</span><span>:</span>
    </div>
    <div style="display:flex;font-size:21px;color:#d1d5db;line-height:1.55">Fire Safety, Semiconductors and SaaS.</div>

    <div style="display:flex;align-items:center;font-size:15.5px;color:#9ca3af;margin-top:40px;white-space:nowrap">
      <div style="display:flex;margin-right:10px">${trendingUp}</div>
      <span style="flex-shrink:0">10 years TDD and CD</span>
      ${divider}
      ${dot}<span style="flex-shrink:0">Led teams of up to 9 engineers</span>
      ${divider}
      ${dot}<span style="flex-shrink:0">20+ engineers mentored</span>
    </div>
  </div>

  <img src="${photoUri}" style="position:absolute;right:0px;bottom:0;width:${photoWidth}px;height:${PHOTO_HEIGHT}px" />
  <div style="display:flex;position:absolute;left:0;bottom:0;width:${WIDTH}px;height:90px;background:linear-gradient(to top, rgba(3,7,18,1) 0%, rgba(3,7,18,0) 100%)"></div>
</div>
`)

const font = (weight) => ({ name: 'DM Sans', weight, style: 'normal', data: fs.readFileSync(path.join(here, `dm-${weight}.woff`)) })
const svg = await satori(markup, { width: WIDTH, height: HEIGHT, fonts: [300, 400, 600, 700].map(font) })
fs.writeFileSync(out, svg)
console.log('banner.svg', Math.round(svg.length / 1024), 'KB, photo width', photoWidth)
