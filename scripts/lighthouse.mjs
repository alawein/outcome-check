import fs from 'node:fs/promises';
import http from 'node:http';
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';
import { chromium } from 'playwright';

await fs.mkdir('build/browser',{recursive:true});
const bytes=await fs.readFile('site/state.html');
const server=http.createServer((request,response)=>{response.setHeader('Content-Type','text/html');response.end(bytes)});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const chrome=await chromeLauncher.launch({chromePath:chromium.executablePath(),chromeFlags:['--headless','--no-sandbox']});
try{
  const result=await lighthouse(`http://127.0.0.1:${server.address().port}`,{port:chrome.port,output:'json',onlyCategories:['performance','accessibility'],formFactor:'desktop',screenEmulation:{mobile:false,width:1280,height:800,deviceScaleFactor:1,disabled:false}});
  await fs.writeFile('build/browser/lighthouse.json',result.report);
  const summary={performance:result.lhr.categories.performance.score,accessibility:result.lhr.categories.accessibility.score,lcp:result.lhr.audits['largest-contentful-paint'].numericValue,tbt:result.lhr.audits['total-blocking-time'].numericValue,inp:'Unavailable: Lighthouse navigation does not measure field INP.'};
  await fs.writeFile('build/browser/lighthouse-summary.json',JSON.stringify(summary,null,2)+'\n');
  console.log(JSON.stringify(summary));
  if(summary.lcp>=2500)throw Error('LCP budget exceeded');
  if(summary.accessibility<1)throw Error('Lighthouse accessibility findings');
}finally{await chrome.kill();await new Promise(resolve=>server.close(resolve))}
