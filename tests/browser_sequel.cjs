const fs=require('node:fs'),vm=require('node:vm');
const elements=new Map();const context=new Proxy({},{get:()=>()=>{},set:()=>true});function el(){return{style:{},hidden:false,textContent:'',append(){},replaceChildren(){},addEventListener(){},setPointerCapture(){},getBoundingClientRect(){return{left:0,width:960}},getContext(){return context}};}
const document={hidden:false,getElementById(id){if(!elements.has(id))elements.set(id,el());return elements.get(id)},createElement:el,addEventListener(){}};
const sandbox={document,window:{addEventListener(){}},localStorage:{getItem(){return'{}'},setItem(){}},Image:class{set src(s){this.complete=true;this.naturalWidth=64;this.onload?.();}},requestAnimationFrame(){},console,Math,Promise};vm.createContext(sandbox);
const html=fs.readFileSync('Backroom_Bratzz_2_Boss_Shift.html','utf8');vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],sandbox);
vm.runInContext(`
start('Alex');shoot();if(shots.length!==1)throw Error('shoot');
start('Riley-L');specialUntil=7;shoot();if(shots.length!==3)throw Error('pizza spread');
const j={kind:'jaxon',x:200,y:200,hp:1};enemies=[j];hitManager(j);if(!unlocked)throw Error('ninja unlock');
start('Ninja');shoot();if(character!=='Ninja'||!shots.length)throw Error('ninja');
start('Alex');for(let i=0;i<3;i++){const r={kind:'rea_rae',x:200,y:200,hp:1};enemies=[r];hitManager(r);}update(.01);if(mode!=='ended'||warnings!==3)throw Error('warnings');
start('Alex');returns=[{x:480,y:534,vx:0,vy:0}];score=200;update(.01);if(score!==100)throw Error('return fire');
start('Alex');for(let i=0;i<3;i++){pickups=[{kind:'pizza',x:480,y:534}];update(.01);}if(specialUntil<=gameTime||pizzas)throw Error('pizza pickup');
start('Alex');enemies=[{kind:'jazzy',x:200,y:200,hp:4,speed:1,phase:0,shotClock:100}];update(.01);if(eventMode!=='jazzy')throw Error('jazzy event');
for(let i=0;i<100;i++)spawn();if(enemies.filter(e=>['jazzy','riley_not_l'].includes(e.kind)).length!==1)throw Error('simultaneous special managers');
start('Alex');pause();const t=elapsed;update(1);if(t!==elapsed||mode!=='paused')throw Error('pause');pause();
for(let i=0;i<3;i++){enemies=[];returns=[];score=LEVELS[i].target_score;elapsed=LEVELS[i].duration;update(.01);if(i<2&&levelIndex!==i+1)throw Error('level advancement');}if(mode!=='ended')throw Error('shift win');
start('Alex');elapsed=45;update(.01);if(mode!=='ended')throw Error('quota loss');
start('Alex');for(let i=0;i<500;i++)update(.016);draw();if(!Number.isFinite(player.x)||!Number.isFinite(score))throw Error('simulation');
`,sandbox);console.log('PASS: shooting, spread, Ninja, warnings, return fire, pizza, special events, pause, levels, win/loss and renderer');
