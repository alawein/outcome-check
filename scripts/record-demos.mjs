import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import { execFileSync } from 'node:child_process';
const browser=await chromium.launch({headless:true});
await fs.mkdir('assets/demos',{recursive:true});
for(const vibe of ['cartoon','calm','pixel','lab']){
  const context=await browser.newContext({viewport:{width:1000,height:760},recordVideo:{dir:'build/video',size:{width:1000,height:760}}});
  await context.route(/https?:\/\//,route=>route.abort());
  const page=await context.newPage();await page.goto(pathToFileURL(path.resolve('site/state.html')).href);
  await page.selectOption('#vibe',vibe);await page.reload();await page.waitForTimeout(1000);
  await page.click('#replay');
  await page.locator('h2').first().scrollIntoViewIfNeeded();await page.waitForTimeout(700);
  await page.selectOption('#verdict-filter','contradicted');await page.waitForTimeout(600);
  await page.selectOption('#verdict-filter','all');await page.waitForTimeout(500);
  const video=page.video();await context.close();
  execFileSync('ffmpeg',['-nostdin','-y','-i',await video.path(),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',`assets/demos/${vibe}.mp4`],{stdio:'ignore'});
}
await browser.close();console.log('PASS: four real offline viewer recordings');
