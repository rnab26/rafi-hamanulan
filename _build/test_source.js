const fs=require('fs');const h=fs.readFileSync('public/index.html','utf8');
const m=h.match(/var S=\(function\(\)\{[\s\S]*?\}\)\(\);try\{var s0=[\s\S]*?catch\(e\)\{\}/);if(!m){console.log('SNIPPET ABSENT');process.exit(1)}
const nt=h.match(/body:m\+' – '\+document\.title\.split\('\|'\)\[0\]\.trim\(\)\+' · מקור: '\+S/);console.log('message avec source:',!!nt);
function run(search,ref,store){const location={search,hostname:'rafihamanulan.co.il'};const document={referrer:ref};const sessionStorage={d:store||{},getItem(k){return this.d[k]||null},setItem(k,v){this.d[k]=v}};return eval(m[0]+';S')}
const cases=[['?gclid=abc','https://www.google.com/','מודעה בגוגל'],['','https://www.google.co.il/','גוגל (חיפוש רגיל/מפות)'],['?utm_source=gbp','','פרופיל העסק בגוגל'],['','https://www.b144.co.il/x','אתר אחר: www.b144.co.il'],['','','ישיר / קישור'],['','https://rafihamanulan.co.il/netanya.html','ישיר / קישור']];
let ok=true;for(const [s,r,e] of cases){const g=run(s,r);if(g!==e){ok=false;console.log('ECHEC',s,r,'=>',g)}}
const st={};run('?gclid=1','https://www.google.com/',st);const g2=run('','https://rafihamanulan.co.il/a.html',st);if(g2!=='מודעה בגוגל'){ok=false;console.log('ECHEC memoire',g2)}
console.log(ok?'TESTS OK ('+(cases.length+1)+')':'TESTS KO')