const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
await pg.goto('file://'+process.cwd()+'/'+process.argv[2]);await pg.evaluate(()=>document.fonts.ready);await pg.waitForFunction(()=>[...document.images,window.IMG,...(window.IMGS||[])].filter(Boolean).every(img=>img.complete&&img.naturalWidth>0),{timeout:10000});await pg.waitForTimeout(300);
for(const t of process.argv.slice(3)){await pg.evaluate(t=>draw(+t),t);await pg.locator('canvas').screenshot({path:`shot_${t}.jpg`,quality:80});}
await b.close();})();
