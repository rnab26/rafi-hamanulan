// Rend les illustrations des guides (_build/ill/*.svg) en public/img/ill-*.webp (800x600). Lancer : node _build/ill/render.js
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execSync}=require('child_process');
(async()=>{const dir=__dirname;const out=path.join(dir,'../../public/img');const b=await chromium.launch();const p=await b.newPage({viewport:{width:800,height:600}});
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.svg'))){const tmp=path.join(dir,'_tmp.html');fs.writeFileSync(tmp,`<style>@font-face{font-family:Rubik;font-weight:400 900;src:url(../../public/fonts/rubik-hebrew.woff2)}body{margin:0}</style>${fs.readFileSync(path.join(dir,f),'utf8')}`);await p.goto('file://'+tmp);await p.evaluate(()=>document.fonts.ready);fs.unlinkSync(tmp);
const png=path.join('/tmp',f+'.png');await p.screenshot({path:png});
execSync(`python3 -c "from PIL import Image;Image.open('${png}').convert('RGB').save('${path.join(out,'ill-'+f.replace('.svg','.webp'))}','WEBP',quality=88)"`);fs.unlinkSync(png);}
await b.close()})();
