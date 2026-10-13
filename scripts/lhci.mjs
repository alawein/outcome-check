import { spawn } from 'node:child_process';
import path from 'node:path';
import { chromium } from 'playwright';
const cli=path.resolve('node_modules/@lhci/cli/src/cli.js');
function run(args){return new Promise((resolve,reject)=>{
 const child=spawn(process.execPath,[cli,...args],{stdio:'inherit',env:{...process.env,CHROME_PATH:chromium.executablePath()}});
 child.on('error',reject);child.on('exit',code=>code===0?resolve():reject(Error(`LHCI exited ${code}`)));
})}
await run(['collect']);await run(['assert']);
