import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

function controller(){
 const page=fs.readFileSync('site/state.html','utf8');
 const scripts=[...page.matchAll(/<script type="text\/javascript">([\s\S]*?)<\/script>/g)];
 const elements=new Map();const listeners=new Map();
 function element(id){if(elements.has(id))return elements.get(id);
   const item={id,value:'calm',dataset:{},textContent:'',animations:[],handlers:new Map(),
     addEventListener(event,fn){const rows=this.handlers.get(event)||[];rows.push(fn);this.handlers.set(event,rows)},
     setAttribute(){},getAnimations(){return this.animations},
     animate(){const a={playState:'running',cancel(){this.playState='idle'}};this.animations.push(a);return a}};
   elements.set(id,item);return item;
 }
 const classes=new Set();const root={dataset:{},classList:{contains:k=>classes.has(k),
   toggle(k){if(classes.has(k)){classes.delete(k);return false}classes.add(k);return true}}};
 const event=element('event');event.dataset.status='confirmed';
 const reduced={matches:false,addEventListener(k,fn){listeners.set('reduced',fn)}};
 const document={documentElement:root,hidden:false,getElementById:element,
   querySelectorAll:()=>[event,element('evidence-field')],
   addEventListener(k,fn){listeners.set(k,fn)}};
 const context={document,localStorage:{getItem(){return null},setItem(){}},
   matchMedia:()=>reduced,getComputedStyle:()=>({getPropertyValue(){return 'ease'}}),
   window:{addEventListener(k,fn){listeners.set(k,fn)}}};
 vm.runInNewContext(scripts.at(-1)[1],context);
 function click(id){for(const fn of element(id).handlers.get('click')||[])fn()}
 return {event,reduced,listeners,click};
}

test('pause immediately cancels active Web Animations',()=>{
 const ui=controller();ui.click('replay');
 assert.ok(ui.event.animations.some(a=>a.playState==='running'));
 ui.click('pause-motion');
 assert.ok(ui.event.animations.every(a=>a.playState!=='running'));
});

test('switching reduced motion cancels active Web Animations',()=>{
 const ui=controller();ui.click('replay');ui.reduced.matches=true;ui.listeners.get('reduced')();
 assert.ok(ui.event.animations.every(a=>a.playState!=='running'));
});
